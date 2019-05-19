# Social Marketer

A web application for gathering business intelligence using Twitter.

A good company is more than a good product. Technologically advanced distribution 
methods are critical for success.

We allow you to gather data on what people are saying about your competitor's
products and reach out to their disatisfied customers.

## How It Works

[Try it out!](https://social-marketer.herokuapp.com)

![](img/demo.gif)

## Under the Hood

### Modeling

Getting data to identify complaints about a specific entity is difficult.
To solve these challenges, we use a boostrapped semi=supervised approach
to training.

Tweets are filtered and initially ranked based on text sentiment. Any
tweet with a negative sentiment score is identified as a possible complaint.

As part of gathering data, each tweet is provided a 768 dimentional embedding
from basilica.ai. As the user gives feedback, PCA and Logistic Regression
are used to create a classifier based on these embeddings.

### Data Mining

The `tweepy` library is used to search for recent tweets by keyword.

### Infrastructure

The application runs on Heroku and a Heroku Postgres instance.

The web application was written using the Flask framework. The `SQLAlchemy`
library is used as an ORM.