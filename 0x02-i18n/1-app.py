#!/usr/bin/env python3
"""
A basic Flask application for internationalization
(i18n) using Flask-Babel.
"""
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config:
    """configurations"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@app.route('/')
def index():
    """render html file"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
