"""
Main application and routing logic for TwitOff
"""

from flask import Flask, request, render_template
from .models import DB


def create_app():
    """
    Create and configure an instance of the flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/company/<name>')
    def company(name):
        return render_template('company.html', name=name)

    return app
