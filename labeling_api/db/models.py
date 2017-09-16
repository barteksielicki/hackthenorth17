import enum

from sqlalchemy.ext.hybrid import hybrid_property

from .db import (
    CRUDMixin,
    db,
    SerializableMixin,
)


class RecordTypeEnum(enum.Enum):
    IMAGE = 0
    TEXT = 1

    @classmethod
    def get(cls, value, fallback=None):
        return cls.__members__.get(value.upper(), fallback)

    def to_dict(self):
        return self.name


class Record(db.Model, SerializableMixin, CRUDMixin):
    __tablename__ = 'record'
    serializable_attrs = [
        'record_type',
        'record_value',
        'labels',
    ]

    id_ = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    record_value = db.Column(db.String, nullable=False)
    _record_type = db.Column(db.Enum(RecordTypeEnum), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id_'))
    label_request_id = db.Column(
        db.Integer,
        db.ForeignKey('label_request.id_')
    )

    labels = db.relationship('Label')

    @hybrid_property
    def record_type(self):
        return self._record_type

    @record_type.setter
    def record_type(self, value):
        tmp = RecordTypeEnum.get(value)
        if tmp is None:
            raise ValueError('Bad Record Type!')
        self._record_type = tmp

    def to_dict(self):
        dict_ = super().to_dict()
        dict_['labels'] = self.labels
        return dict_


class Label(db.Model, SerializableMixin, CRUDMixin):
    __tablename__ = 'label'
    serializable_attrs = [
        'values',
    ]

    id_ = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    values = db.Column(db.String, nullable=False)


class LabelRequest(db.Model, SerializableMixin, CRUDMixin):
    __tablename__ = 'label_request'
    serializable_attrs = [
        'records',
    ]

    id_ = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    records = db.relationship(
        'Record',
        single_parent=True,
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    def to_dict(self):
        dict_ = super().to_dict()
        dict_['records'] = [r.to_dict() for r in self.records.all()]
        return dict_
