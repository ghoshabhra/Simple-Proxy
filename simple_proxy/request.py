from flask import Response
import requests 
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor 
import simple_proxy.logger as logger

class Request(ABC):
    def __init__(self, value):
        self._curr_obj = {
            'type': value,
            'excluded_headers': ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        }
        self.executor = ThreadPoolExecutor(max_workers=2)
        super().__init__()

    def add_property(self, name, value):
        self._curr_obj[name] = value
        return self

    def respond(self, resp):
        headers = [ (name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in self._curr_obj["excluded_headers"] ]
        return Response(resp.content, resp.status_code, headers)

    def execute(self):
        msg = f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]} {self._curr_obj["type"]}'
        self.executor.submit(logger.getLogger().info , msg)

        response = self.send_request()

        msg = f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]} {self._curr_obj["type"]} {response.status}'
        self.executor.submit(logger.getLogger().info , msg)

        return response

    @abstractmethod    
    def send_request(self):
        pass

class GetRequest(Request):
    def __init__(self):
        super().__init__("GET")

    def send_request(self):
        resp = requests.get(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}', verify= False, headers=self._curr_obj["headers"])
        return self.respond(resp)

class PostRequest(Request):
    def __init__(self):
        super().__init__("POST")

    def send_request(self):
        resp = None
        if 'form_data' in self._curr_obj.keys() :
            resp = requests.post(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}',json=self._curr_obj["form_data"], verify= False, headers=self._curr_obj["headers"])
        elif 'raw_data' in self._curr_obj.keys():
            resp = requests.post(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}',data=self._curr_obj["raw_data"], verify= False, headers=self._curr_obj["headers"])
        return self.respond(resp)

class PutRequest(Request):
    def __init__(self):
        super().__init__("PUT")

    def send_request(self):
        resp = None
        if 'form_data' in self._curr_obj.keys() :
            resp = requests.put(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}',json=self._curr_obj["form_data"], verify= False, headers=self._curr_obj["headers"])
        elif 'raw_data' in self._curr_obj.keys():
            resp = requests.put(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}',data=self._curr_obj["raw_data"], verify= False, headers=self._curr_obj["headers"])
        return self.respond(resp)

class DeleteRequest(Request):
    def __init__(self):
        super().__init__("DELETE")
    
    def send_request(self):
        resp = requests.delete(f'{self._curr_obj["SITE_NAME"]}{self._curr_obj["path"]}', verify= False, headers=self._curr_obj["headers"])
        return self.respond(resp)