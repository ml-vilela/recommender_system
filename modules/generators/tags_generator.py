# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from modules.generators.macros import MIN_TAGS, MAX_TAGS

class TagsGenerator():
    def __init__(self, tags_csv, size, min_tags = MIN_TAGS, max_tags = MAX_TAGS):
        self.tags_csv = tags_csv
        self.size = size
        self.min_tags = min_tags
        self.max_tags = max_tags
        self.records = []

    @property
    def tags_df(self):
        return pd.read_csv(self.tags_csv)

    @property
    def record_tags_df(self):
        return pd.DataFrame(data=self.records,columns=['id','tags']).set_index('id')
        
    def generate_tags(self):
        tags_count = np.random.randint(self.min_tags,high=self.max_tags+1,size=1)[0]
        tags_arr = self.tags_df.sample(tags_count).values.flatten()
        return ' '.join(map(str, tags_arr))
    
    def generate_record_tags(self):
        for record_id in range(self.size + 1):
            self.records.append([record_id, self.generate_tags()])

    def save_to_csv(self, file):
        self.record_tags_df.to_csv(file)

