import os, sys
sys.path.append(os.getcwd())

from flask import Flask, request
from flask_restful import Resource, Api
from modules.models.collaborative_filtering import CollaborativeFiltering
from modules.models.content_filtering import ContentFiltering

app = Flask(__name__)
api = Api(app)

class SideAContentFilteringResource(Resource):
    def get(self):
        id = request.args.get('id')
        id = int(id)
        
        side_a_content_filter.predict(id)
        return side_a_content_filter.similars

class SideBContentFilteringResource(Resource):
    def get(self):
        id = request.args.get('id')
        id = int(id)
        
        side_b_content_filter.predict(id)
        return side_b_content_filter.similars
        
class CollaborativeFilteringResource(Resource):
    def get(self, origin_entity):
        id = request.args.get('id')
        record_ids = request.args.get('record_ids')

        id = int(id)
        record_ids = list(map(int, record_ids.split(',')))

        collaborative_filter.predict(origin_entity, id, record_ids)

        return collaborative_filter.sorted_ratings

class SideAHybridResource(Resource):
    def get(self):
        id = request.args.get('id')
        id = int(id)
        
        side_a_content_filter.predict(id)
        record_ids = [s[0] for s in side_a_content_filter.similars]
        
        collaborative_filter.predict('side_a', id, record_ids)
        return collaborative_filter.sorted_ratings

class SideBHybridResource(Resource):
    def get(self):
        id = request.args.get('id')
        id = int(id)
        
        side_b_content_filter.predict(id)
        record_ids = [s[0] for s in side_b_content_filter.similars]
        
        collaborative_filter.predict('side_b', id, record_ids)
        return collaborative_filter.sorted_ratings

api.add_resource(SideAContentFilteringResource, '/side_a/similar_to')
api.add_resource(SideBContentFilteringResource, '/side_b/similar_to')
api.add_resource(CollaborativeFilteringResource, '/<origin_entity>/ratings_for')
api.add_resource(SideAHybridResource, '/side_a/similar_to_with_rating')
api.add_resource(SideBHybridResource, '/side_b/similar_to_with_rating')

if __name__ == '__main__':
    side_a_content_filter = ContentFiltering()
    side_a_content_filter.load('ml_models/tfidf/side_a_cosine_sim.joblib')

    side_b_content_filter = ContentFiltering()
    side_b_content_filter.load('ml_models/tfidf/side_b_cosine_sim.joblib')
    
    collaborative_filter = CollaborativeFiltering()
    collaborative_filter.load('ml_models/svd/side_a_svd.joblib',
                              'ml_models/svd/side_b_svd.joblib')

    app.run(debug=False, host='0.0.0.0', port=6000)
