# -*- coding: utf-8 -*-

import math
from modules.generators.macros import MAX_RATING, MIN_RATING
from joblib import load

class CollaborativeFiltering():
    def __init__(self):
        self.max_rating     = MAX_RATING
        self.min_rating     = MIN_RATING
        self.max_distance   = self.euclidean_distance(self.min_rating, self.min_rating)
        self.ratings        = {}
        self.side_a_svd     = None
        self.side_b_svd     = None

    @property
    def sorted_ratings(self):
        return sorted(self.ratings.items(), key=lambda x:x[1],reverse=True)

    def euclidean_distance(self, x, y):
        return math.sqrt((self.max_rating - x)**2 + (self.max_rating - y)**2)    
    
    def load(self, side_a_svd, side_b_svd):
        self.side_a_svd   = load(side_a_svd)
        self.side_b_svd   = load(side_b_svd)
        
    def other_side(self, side):
        return 'side_b' if side == 'side_a' else 'side_a'
    
    def predict(self, origin_entity, origin_id, target_ids):
        self.ratings = {}
        origin_svd = '{0}_svd'.format(origin_entity)
        target_svd = '{0}_svd'.format(self.other_side(origin_entity))
        
        for target_id in target_ids:
            origin_rating_predict = getattr(self, origin_svd).predict(target_id, origin_id).est
            target_rating_predict = getattr(self, target_svd).predict(origin_id, target_id).est

            rating_distance = self.euclidean_distance(origin_rating_predict, target_rating_predict)
            self.ratings[target_id] = 1 - (rating_distance / self.max_distance)
