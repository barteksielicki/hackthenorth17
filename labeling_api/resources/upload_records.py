import os
import uuid

from flask import request

from ..db import models
from ..flask_restful_extensions import Resource


class UploadRecords(Resource):
    STORAGE_PATH = './images'
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
                    items:
                      type: file
                  records_type:
                    type: string
                required:
                - records
                - record_type

        """
        # create new label request
        label_request = models.LabelRequest().save(commit=True)
        # save file to storage and create records
        for file_ in request.files.getlist('records'):
            file_path = self._save_to_storage(file_)
            models.Record(
                label_request_id=label_request.id_,
                record_type=request.args['records_type'],
                record_value=file_path,
            ).save(commit=True)
        return label_request.to_dict()

    def _save_to_storage(self, image_file):
        fpath = os.path.join(
            self.STORAGE_PATH,
            f'{uuid.uuid4().hex}.{image_file.filename.split(".")[-1]}',
        )
        with open(fpath, 'wb') as f:
            f.write(image_file.read())
        return fpath
