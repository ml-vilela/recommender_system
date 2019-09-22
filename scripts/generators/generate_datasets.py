# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

from modules.generators.rating_generator import RatingGenerator
from modules.generators.tags_generator import TagsGenerator
from modules.generators.macros import MIN_RATING, MAX_RATING, SIDE_A_COUNT, SIDE_B_COUNT

side_a_tags = TagsGenerator('files/side_a_tags.csv',SIDE_A_COUNT)
side_a_tags.generate_record_tags()
side_a_tags.save_to_csv('datasets/side_a_record_tags.csv')

side_b_tags = TagsGenerator('files/side_b_tags.csv',SIDE_B_COUNT)
side_b_tags.generate_record_tags()
side_b_tags.save_to_csv('datasets/side_b_record_tags.csv')


ratings = RatingGenerator(min_rating=MIN_RATING, max_rating=MAX_RATING)
ratings.generate_rating_dataset()
ratings.save_to_csv('datasets')
