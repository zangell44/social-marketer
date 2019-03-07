"""
Main application and routing logic for SocialMarketer
"""

from decouple import config
from flask import Flask, request, render_template, redirect, url_for
from .models import DB, Company
from .twitter import *


def create_app():
    """
    Create and configure an instance of the flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['ENV'] = 'debug' # to do, change before deploy

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/company', methods=['POST'])
    @app.route('/company/<name>', methods=['GET'])
    def company(name=None, message=''):
        if request.method == 'GET':
            tweets =  Company.query.filter_by(name=name).first().tweets
            return render_template('company.html', name=name, tweets=tweets)

        # otherwise, try to add a company
        name, competitor = request.values['name'], request.values['competitor']
        try:
            # import pdb; pdb.set_trace()
            add_or_update_company(name, competitor)
            return redirect('/company/' + name)
        except Exception as e:
            return 'An exception occurred, please try again'

    @app.route('/signup/')
    def signup():
        return render_template('signup.html')

    @app.route('/login/')
    def login():
        return render_template('login.html')

    return app
