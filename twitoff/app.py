"""
Main application and routing logic for SocialMarketer
"""

from decouple import config
from flask import Flask, request, render_template, redirect, url_for
from .models import DB, Company
from .predict import partial_fit, update_estimates
from sqlalchemy import and_
from .twitter import *


def create_app():
    """
    Create and configure an instance of the flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qkqmtneglkrfts:acbb2730a7df0a599cbdac2b4e1db6cfa1578d2d0b47d5e2503d66e176e81fa8@ec2-75-101-133-29.compute-1.amazonaws.com:5432/de619u90jj7ocb;'#config('DATABASE_URL')
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
            company_id = Company.query.filter_by(name=name).first().id
            if company_id:
                tweets = DB.session.query(Tweet).filter(
                    and_(
                        Tweet.company_id == company_id,
                        Tweet.converted == None
                    )
                ).order_by(Tweet.likelihood.desc())
            else:
                tweets = []
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

    @app.route('/update/<name>')
    def update(name):
        company = Company.query.filter_by(name=name).first()
        add_or_update_company(name, company.competitor)
        return redirect(url_for('company', name=name))

    @app.route('/converted/<id>')
    def converted(id):
        update_conversion(id, 1)
        partial_fit(id)
        company_id = DB.session.query(Tweet).filter(Tweet.id == id).first().company_id
        update_estimates(company_id)
        company_name = DB.session.query(Company).filter(Company.id == company_id).first().name
        return redirect(url_for('company', name=company_name))

    @app.route('/failed/<id>')
    def failed(id):
        update_conversion(id, 0)
        partial_fit(id)
        company_id = DB.session.query(Tweet).filter(Tweet.id == id).first().company_id
        update_estimates(company_id)
        company_name = DB.session.query(Company).filter(Company.id == company_id).first().name
        return redirect(url_for('company', name=company_name))

    return app
