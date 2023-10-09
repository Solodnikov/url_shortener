from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.get(custom_id):
            flash(f'Имя {custom_id} уже занято!')
            return render_template('index.html', form=form)

        if not custom_id:
            custom_id = URLMap.get_unique_short_id()

        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        url_map.save()
        return (
            render_template('index.html', form=form, short=custom_id),
            HTTPStatus.OK
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url_object = URLMap.get_or_404(short)
    return redirect(url_object.original)
