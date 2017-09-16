from flask_restful import Api as BaseApi


class Api(BaseApi):
    PREFIX = '/'

    def add_resources(self, registry):
        """Register classes from registry as Api resources.
        """
        for resource_class in registry.values():
            print(resource_class.endpoint_name)
            if resource_class.endpoint_name:
                print(resource_class.endpoint_name)
                self.add_resource(
                    resource_class,
                    self._to_url(resource_class.endpoint_name),
                    endpoint=self._to_name(resource_class.endpoint_name),
                )

    def _to_url(self, endpoint_name):
        if endpoint_name.startswith('/'):
            return self.PREFIX + endpoint_name[1:]
        return self.PREFIX + endpoint_name

    def _to_name(self, endpoint_name):
        return self.PREFIX + endpoint_name.split('<', 1)[0][:-1]
