# -*- coding: utf-8 -*-

from joblib import load

class ContentFiltering():
    def __init__(self, max_results=10):
        self.cosine_sim = None
        self.max_results = max_results
        self.similars = []
    
    def load(self, model):
        self.cosine_sim = load(model)
        
    def predict(self, record_id):
        sims = list(enumerate(self.cosine_sim[record_id]))
        sorted_sims = sorted(sims, key=lambda x: x[1], reverse=True)
        self.similars = sorted_sims[1:self.max_results+1]

