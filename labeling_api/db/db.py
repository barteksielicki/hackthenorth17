from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SerializableMixin:
    serializable_attrs = []

    def __repr__(self):
        attributes = list()
        # always add id to __repr__ (if present)
        if 'id_' in self.__dict__:
            attributes.append('id={0}'.format(self.id_))
        for attr in self.serializable_attrs:
            if attr == 'id_':
                continue
            attributes.append("{attr_name}={attr_value}".format(
                attr_name=attr,
                attr_value=getattr(self, attr),
            ))
        return '<{class_name} {attributes}>'.format(
            class_name=self.__class__.__name__,
            attributes=', '.join(attributes),
        )

    def to_dict(self):
        attributes = dict()
        for attr in self.serializable_attrs:
            attributes[attr] = getattr(self, attr)
            to_dict_func = getattr(getattr(self, attr), 'to_dict', None)
            if to_dict_func:
                attributes[attr] = getattr(self, attr).to_dict()
        if 'id_' in self.__dict__:
            attributes['id'] = self.id_
        return attributes


class CRUDMixin:
    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def save(self, commit=True, error_handler=None):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
