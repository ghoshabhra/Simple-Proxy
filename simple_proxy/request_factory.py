import json
from simple_proxy.request import GetRequest, PostRequest, PutRequest, DeleteRequest


class request_factory:
    def __init__(self):
        self._current_object = {}


    def add_property(self, name, value):
        self._current_object[name] = value
        return self

    def parse_payload(self):
        if bool(self._current_object.get("request").form.to_dict()) :
            self.rq.add_property("form_data", self._current_object.get("request").get_json())
        else:
            self.rq.add_property("raw_data",  self._current_object.get("request").data)

    def configure(self):
        self.rq = None
        if self._current_object.get("request").method=='GET':
            self.rq = GetRequest()

        elif self._current_object.get("request").method=='POST':
            self.rq = PostRequest()
            self.parse_payload()

        elif self._current_object.get("request").method=='PUT':
            self.rq = PutRequest()
            self.parse_payload()
        
        elif self._current_object.get("request").method=='DELETE':
            self.rq = DeleteRequest()
        
        self.rq.add_property("SITE_NAME", self._current_object.get("SITE_NAME")
                ).add_property("path",  self._current_object.get("path")
                ).add_property("headers", self._current_object.get("request").headers)

        return self.rq

