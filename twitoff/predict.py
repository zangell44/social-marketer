"""
Houses model updates and predictions
"""
import numpy as np
from sklearn.linear_model import SGDClassifier
from .models import Company, DB, Tweet

def update_estimates(company_id):
    """
    Updates estimated conversion likelihood for a given company id

    company_id : int

    return : None
    """
    company_model = DB.session.query(Company).filter(Company.id == company_id).first().model
    tweets = DB.session.query(Tweet).filter(Tweet.company_id == company_id).all()

    # loop through tweets and update predictions
    for twt in tweets:
        pred = company_model.predict_proba(np.array(twt.embedding).reshape(1, -1))[0][1]
        DB.session.query(Tweet). \
            filter(Tweet.id == twt.id). \
            update({'likelihood' : round(pred,2)})

    DB.session.commit()


def partial_fit(tweet_id):
    """
    Updates response prediction model given a single tweet and result. Saves new
    weights back into database.

    tweet_id : int
        Unique identifier of tweet thats been updated

    return : None
        Company model is updated in database
    """
    # get the company model object to update
    tweet = DB.session.query(Tweet).filter(Tweet.id == tweet_id).first()
    company_id = tweet.company_id
    company_model = DB.session.query(Company).filter(Company.id == company_id).first().model

    # get the embedding and result
    company_model.partial_fit(np.array(tweet.embedding).reshape(1, -1),
                              np.array(tweet.converted).ravel(),
                              classes=[0,1])
    DB.session.query(Company). \
        filter(Company.id == company_id). \
        update({'model': company_model})
    DB.session.commit()

