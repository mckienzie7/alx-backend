#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, render_template

my_app = Flask(__name__)


@my_app.route('/', strict_slashes=False)
def display_index() -> str:
    """run the app html"""
    return render_template('0-index.html')


if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port=5000)
