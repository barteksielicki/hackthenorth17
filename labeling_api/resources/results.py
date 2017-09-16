from ..flask_restful_extensions import Resource


class GatherResults(Resource):
    endpoint_name = 'results/<int:results_id>'

    def get(self, results_id):
        return {'results_id': results_id}
