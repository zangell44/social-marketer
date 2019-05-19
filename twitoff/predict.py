"""
Houses model updates and predictions
"""
import numpy as np
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
        try:
            pred = company_model.predict_proba(np.array(twt.embedding).reshape(1, -1))[0][1]
            DB.session.query(Tweet). \
                filter(Tweet.id == twt.id). \
                update({'likelihood': round(pred, 2)})
        except:
            # model not fitted
            break

    DB.session.commit()


def fit(company_id):
    """
    Updates response prediction model for a company

    company_id : int
        Unique identifier of company

    return : None
        Company model is updated in database
    """
    # get the company model object to re-fit
    company_model = DB.session.query(Company).filter(Company.id == company_id).first().model

    # get embeddings and results
    tweets = DB.session.query(Tweet.embedding, Tweet.converted) \
        .filter(Tweet.company_id == company_id,
                Tweet.converted != None).all()

    data = np.array(tweets)
    X = np.stack(data[:, 0], axis=0)
    y = data[:, 1].astype(np.int)

    # fit model and update in db if we have enough
    if X.shape[0] > 10:
        company_model.fit(X, y)

    DB.session.query(Company). \
        filter(Company.id == company_id). \
        update({'model': company_model})
    DB.session.commit()
