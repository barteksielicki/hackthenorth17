import enum

from sqlalchemy.ext.hybrid import hybrid_property

from .db import (
    db,
    SerializableMixin,
)


class RecordTypeEnum(enum.Enum):
    PHOTO = 0
    TEXT = 1

    @classmethod
    def get(cls, value, fallback=None):
        return cls.__members__.get(value.upper(), fallback)


class Record(db.Model, SerializableMixin):
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

    label = db.relationship(
        'Label',
        cascade='all, delete-orphan',
        single_parent=True,
    )

    @hybrid_property
    def record_type(self):
        return self._record_type

    @record_type.setter
    def record_type(self, value):
        tmp = RecordTypeEnum.get(value)
        if tmp is None:
            raise ValueError('Bad Record Type!')
        self._record_type = tmp

    @property
    def labels(self):
        return self.label.values


class Label(db.Model, SerializableMixin):
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


class LabelRequest(db.Model, SerializableMixin):
    __tablename__ = 'label_request'

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
