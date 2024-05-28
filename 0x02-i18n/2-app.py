#!/usr/bin/env python3
"""
A Basic Flask application with internationalization (i18n) using Flask-Babel.
"""
from flask import Flask, request, render_template
from flask_babel import Babel


class Config:
    """
    Application configuration class.
    """
    LANGUAGES_LIST = ['en', 'fr']
    DEFAULT_LANGUAGE = 'en'
    DEFAULT_TIMEZONE = 'UTC'


my_app = Flask(__name__)
my_app.config.from_object(Config)


babel = Babel(my_app)


@babel.localeselector
def get_locale() -> str:
    """
    Get locale from the request object.
    """
    return request.accept_languages.best_match(my_app.config['LANGUAGES_LIST'])


@my_app.route('/', strict_slashes=False)
def display_index() -> str:
    """
    Render a basic HTML template.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port=5000)
