"""
Houses model updates and predictions
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import Company

def get_model(company_name):
    """
    Returns logistic regression object associated with a company

    :param company_name:
    :return:
    """
    pass

def partial_fit(tweet_id, result, company_name):
    """
    Updates response prediction model given a single tweet and result. Saves new
    weights back into database.

    :param tweet:
    :param result:
    :param company_name:
    :return:
    """
    pass
