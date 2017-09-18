from flask_restful import Resource as BaseResource
from flask import request
from flask.views import MethodViewType

from .register import (
    ClassRegister,
    ClassRegisterMeta,
)

API_RESOURCES_REGISTER = ClassRegister()
# store all resource classes in given ClassRegister instance.
ClassRegisterMeta.register = API_RESOURCES_REGISTER


class RedGuardianResourceMeta(ClassRegisterMeta, MethodViewType):
    pass


class Resource(BaseResource, metaclass=RedGuardianResourceMeta):
    endpoint_name = None

    @property
    def request_json(self):
        return request.get_json()
