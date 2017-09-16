from ..flask_restful_extensions import Resource


class UploadRecords(Resource):
    endpoint_name = 'upload'

    def post(self):
        """
        request_args = {'records', 'record_type'}
        parameters:
            - name: json
            in: body
            required: true
            schema:
                type: object
                properties:
                  records:
                    type: array
                    items: {}
                  record_type:
                    type: string
                required:
                - records
                - record_type

        """
        return self.request_json
