import random
import re
from datetime import datetime
from http import HTTPStatus

from flask import url_for

from . import db
from .error_handlers import InvalidAPIUsage
from .settings import (DEFAULT_SHORT_LINK_LENGTH, LETTERS_AND_DIGITS,
                       REG_PATTERN, USER_SHORT_LINK_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, unique=True)
    short = db.Column(
        db.String(USER_SHORT_LINK_LENGTH),
        nullable=False,
        unique=True)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view',
                               short=self.short,
                               _external=True)
        )

    def url_to_dict(self) -> dict[str, str]:
        return dict(url=self.original)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, short_url):
        """получение объекта по короткому адресу"""
        return cls.query.filter_by(
            short=short_url).first()

    @classmethod
    def get_or_404(cls, short_url):
        """получение объекта по короткому адресу,
        при отсутствии вызов исключения"""
        if not cls.get(short_url):
            raise InvalidAPIUsage('Указанный id не найден',
                                  HTTPStatus.NOT_FOUND)
        return cls.get(short_url)

    @classmethod
    def get_unique_short_id(cls) -> str:
        """получение уникальной короткой ссылки"""
        rand_string = ''.join(random.choices(
            population=LETTERS_AND_DIGITS,
            k=DEFAULT_SHORT_LINK_LENGTH)
        )
        # поставил возврат только уникального результата
        # что бы потом не проводить проверку
        # на повторяемость результат функции
        if not cls.get(rand_string):
            return rand_string
        return cls.get_unique_short_id()

    @staticmethod
    def from_dict(data):
        """формирование объекта URLmap из даты.
        возвращает созданныей объект URLmap."""
        if not data.get('custom_id'):
            data['custom_id'] = URLMap.get_unique_short_id()
        else:
            if not re.match(REG_PATTERN, data['custom_id']):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки',
                    HTTPStatus.BAD_REQUEST)
            # проверку ниже не могу убрать, ругается pytest - test_len_short_id_api(client)
            # если при POST-запросе к эндпоинту `/api/id/` поле `short_id` содержит
            # строку длиннее 16 символов - нужно вернуть статус-код 400.
            if len(data['custom_id']) > USER_SHORT_LINK_LENGTH:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки',
                    HTTPStatus.BAD_REQUEST)
            # проверку ниже не могу перенести в get_unique_short_id.
            # get_unique_short_id у меня отвечает только за генерацию уникального short_id,
            # когда не заявлен пользователем.
            # Если убраю проверку для придуманного пользователем short_id, то
            # ругается test_url_already_exists - AssertionError: 'При попытке создания
            # ссылки с коротким именем, которое уже занято - ', 'вызывайте исключение.')
            if URLMap.get(data['custom_id']):
                custom_id = data['custom_id']
                raise InvalidAPIUsage(
                    f'Имя "{custom_id}" уже занято.',
                    HTTPStatus.BAD_REQUEST)
        return URLMap(original=data['url'], short=data['custom_id'])
