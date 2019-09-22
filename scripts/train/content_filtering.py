# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from joblib import dump

def train_tfidf_model(entity):
    input_filename = 'datasets/{0}_record_tags.csv'.format(entity)
    output_model = 'ml_models/tfidf/{0}_cosine_sim.joblib'.format(entity)
    
    tags = pd.read_csv(input_filename)

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(tags['tags'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    dump(cosine_sim, output_model)

    del tags
    del cosine_sim

train_tfidf_model('side_a')
train_tfidf_model('side_b')