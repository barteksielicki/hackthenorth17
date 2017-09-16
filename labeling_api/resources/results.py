from ..db import models
from ..flask_restful_extensions import Resource


class GatherResults(Resource):
    endpoint_name = 'results/<int:results_id>'

    def get(self, results_id):
        result = models.LabelRequest.query.filter_by(id_=results_id).first()
        return result or ({'message': 'Invalid record type'}, 404)
