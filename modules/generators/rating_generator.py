# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from modules.generators.macros import MIN_REVIEWS, MAX_REVIEWS, SIDE_A_COUNT, SIDE_B_COUNT

class RatingGenerator():
    def __init__(self, min_rating, max_rating):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.ratings = []
    
    @property
    def rating_df(self):
        rating_df = pd.DataFrame(data=self.ratings,columns=['side_a_id','side_b_id','side_a_rating','side_b_rating'])
        return rating_df.groupby(['side_a_id','side_b_id']).agg({'side_b_rating':'mean','side_a_rating':'mean'}).reset_index()
        
    @property
    def side_a_df(self):
        return self.rating_df[['side_a_id','side_b_id','side_a_rating']].rename(columns={'side_a_rating':'rating'})
        
    @property
    def side_b_df(self):
        return self.rating_df[['side_b_id','side_a_id','side_b_rating']].rename(columns={'side_b_rating':'rating'})
    
    def ReLU(self, x):
        return max(0, x)
    
    def generate_rating(self):
        return np.random.randint(self.min_rating,high=self.max_rating+1,size=1)[0]

    def generate_rating_dataset(self):
        for side_a in range(SIDE_A_COUNT):
            for side_b in range(SIDE_B_COUNT):
                num_reviews = np.random.randint(MIN_REVIEWS,high=MAX_REVIEWS,size=1)[0]
                num_ratings = self.ReLU(num_reviews)
                for r in range(num_ratings):
                    b_rating = self.generate_rating()
                    a_rating = self.generate_rating()
                    self.ratings.append([side_a, side_b, b_rating, a_rating])
        
    def save_to_csv(self, path):
        self.side_a_df.to_csv(path+'/side_a_ratings.csv')
        self.side_b_df.to_csv(path+'/side_b_ratings.csv')

