"""
SQLALchemy models for TwitOff
"""

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

# class User(DB.Model):
#     """
#     Twitter users that we pull and analyze tweets for
#     """
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     name = DB.Column(DB.String(15), nullable=False)
#
#     def __repr__(self):
#         return '<USER {}>'.format(self.name)

class Tweet(DB.Model):
    """
    Tweets
    """
    id = DB.Column(DB.BigInteger, primary_key=True, autoincrement=True)
    text = DB.Column(DB.Unicode(500))
    embedding = DB.Column(DB.PickleType)
    # user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
    #         nullable=False)
    # user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    user = DB.Column(DB.String(15), nullable=False)

    company_id = DB.Column(DB.Integer, DB.ForeignKey('company.id'))

    sentiment = DB.Column(DB.Float)
    likelihood = DB.Column(DB.Float)
    converted = DB.Column(DB.Integer)

    # Tweet(id=1, text='text', embedding=[1.0], user_id=1, company_id=1)

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

    # twt = Tweet(text='this is a test', embedding=[1,1], user='someone', company_id=1, sentiment=1.0, likelihood=1.0, converted=0)
