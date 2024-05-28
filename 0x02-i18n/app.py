#!/usr/bin/env python3
"""
A Basic Flask application with internationalization (i18n) and timezone support.
"""
import pytz
import datetime
from typing import Dict, Union

from flask import Flask, g, request, render_template
from flask_babel import Babel, format_datetime

class AppConfig:
    """
    Application configuration class.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

# Instantiate the application object
app = Flask(__name__)
app.config.from_object(AppConfig)

# Wrap the application with Babel for internationalization
babel = Babel(app)

# Dummy user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details.
    Args:
        id (str): user id.
    Returns:
        (Dict): user dictionary if id is valid else None.
    """
    return users.get(int(id), None)

@babel.localeselector
def get_locale() -> str:
    """
    Get the locale from the request object.
    """
    options = [
        request.args.get('locale', '').strip(),
        g.user.get('locale', None) if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        AppConfig.BABEL_DEFAULT_LOCALE
    ]
    for locale in options:
        if locale and locale in AppConfig.LANGUAGES:
            return locale

@babel.timezoneselector
def get_timezone() -> str:
    """
    Get the timezone from the request object.
    """
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user['timezone']
    try:
        tz = pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        tz = app.config['BABEL_DEFAULT_TIMEZONE']
    return tz

@app.before_request
def before_request() -> None:
    """
    Add valid user and current time to the global session object `g`.
    """
    setattr(g, 'user', get_user(request.args.get('login_as', 0)))
    setattr(g, 'time', format_datetime(datetime.datetime.now()))

@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Render a basic HTML template.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Specify host and port for the development server
    app.run(host='0.0.0.0', port=5000)
