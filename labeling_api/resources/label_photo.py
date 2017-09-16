from flask_restful import reqparse

from ..flask_restful_extensions import Resource


class RecordLabeling(Resource):
    endpoint_name = 'label/<int:record_id>'

    def post(self, record_id):
        """
        parameters:
            - name: json
            in: body
            required: true
            schema:
                type: object
                properties:
                  labels: {}
                required:
                - labels

        """
        labels = self.request_json.get('labels')
        return {
            'labels': labels,
            'record_id': record_id,
        }
