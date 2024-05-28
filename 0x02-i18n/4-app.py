#!/usr/bin/env python3
"""
A Basic Flask application for internationalization (i18n) using Flask-Babel.
"""
from flask import Flask, request, render_template
from flask_babel import Babel


class AppConfig:
    """
    Application configuration class.
    """
    SUPPORTED_LANGUAGES = ['en', 'fr']
    DEFAULT_LANGUAGE = 'en'
    DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(AppConfig)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Get the locale from the request object or accept header.
    """
    locale = request.args.get('locale', '').strip()
    if locale and locale in app.config['SUPPORTED_LANGUAGES']:
        return locale
    return request.accept_languages.best_match(
        app.config['SUPPORTED_LANGUAGES']
    )


@app.route('/', strict_slashes=False)
def display_index() -> str:
    """
    Render a basic HTML template.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
