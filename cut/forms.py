from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from .settings import DEFAULT_SHORT_LINK_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку для сокращения',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Не является URL адресом'),
        ]
    )
    custom_id = StringField(
        'Предложить свой вариант сокращения',
        validators=[
            Length(1, DEFAULT_SHORT_LINK_LENGTH,
                   message=(
                       f'Длинна ссылки не может превышать'
                       f'{DEFAULT_SHORT_LINK_LENGTH} символов')),
            Optional()
        ]
    )
    submit = SubmitField('Добавить')
