class Tag:
    def __init__(self, tag, attr, new_attr_value):
        self.tag = tag
        self.attr = attr
        self.new_attr_value = new_attr_value


class Resourse:
    def __init__(self, resource_url, resource_path):
        self.resource_url = resource_url
        self.resource_path = resource_path
