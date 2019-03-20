"""
SQLALchemy models for TwitOff
"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Tweet(DB.Model):
    """
    Tweets
    """
    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    text = DB.Column(DB.Unicode(500))
    embedding = DB.Column(DB.PickleType)

    user = DB.Column(DB.String(15), nullable=False)

    company_id = DB.Column(DB.Integer, DB.ForeignKey('company.id'))

    sentiment = DB.Column(DB.Float)
    likelihood = DB.Column(DB.Float)
    converted = DB.Column(DB.Integer)

    link = DB.Column(DB.String(75))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)

class Company(DB.Model):
    """
    A company using the platform for marketing
    """
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(30), nullable=False)
    competitor = DB.Column(DB.String(30), nullable=False)
    tweets = DB.relationship('Tweet', backref='company')
    model = DB.Column(DB.PickleType)
