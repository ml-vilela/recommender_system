# -*- coding: utf-8 -*-

import pandas as pd
from surprise import Reader, Dataset, SVD
# Uncomment if you want to evaluate the model first
# from surprise.model_selection.validation import cross_validate
from joblib import dump

def train_svd(entity, target):
    dataset = 'datasets/{0}_ratings.csv'.format(entity)
    model   = 'ml_models/svd/{0}_svd.joblib'.format(entity)
    entity_id = '{0}_id'.format(entity)
    target_id = '{0}_id'.format(target)
    
    df = pd.read_csv(dataset)
    
    reader = Reader()
    data = Dataset.load_from_df(df[[entity_id,target_id,'rating']],reader)
    svd = SVD()
    
    # Uncomment if you want to evaluate the model first
    # cross_validate(worker_svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    
    dump(svd, model)
    del svd
    del df

train_svd('side_a','side_b')
train_svd('side_b','side_a')