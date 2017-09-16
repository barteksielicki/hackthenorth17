from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SerializableMixin:
    serializable_attrs = []

    def __repr__(self):
        attributes = list()
        # always add id to __repr__ (if present)
        if 'id_' in self.__dict__:
            attributes.append('id={0}'.format(self.id))
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
        return {attr: getattr(self, attr)
                for attr in self.serializable_attrs}
