import json

from .db import (
    db,
    models,
)


def populate_db():
    db.session.add_all([
        models.Label(values=json.dumps({'food': True, 'class': 'pasta'})),
        models.Label(values=json.dumps({'food': True, 'class': 'tortilla'})),
        models.LabelRequest(),
    ])
    db.session.commit()
    db.session.add_all([
        models.Record(
            record_value='./images/spaghetti_bolognese.jpeg',
            record_type='image',
            label_id=0,
            label_request_id=0,
        ),
        models.Record(
            record_value='./images/tortilla.jpeg',
            record_type='image',
            label_id=1,
            label_request_id=0,
        ),
    ])
    db.session.commit()
