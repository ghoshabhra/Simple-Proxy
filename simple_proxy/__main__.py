
from flask import Flask,request,redirect,Response
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import sys
from simple_proxy.request_factory import request_factory

app = Flask(__name__)
SITE_NAME = ""

@app.route('/simple_proxy/heartbeat/')
def index():
    global SITE_NAME
    print(SITE_NAME)
    return 'SImple Proxy Server is running!'

@app.route('/<path:path>',methods=["GET","POST","DELETE","PUT"])
def proxy(path):
    global SITE_NAME
    rf = request_factory()
    rf.add_property("SITE_NAME", SITE_NAME
        ).add_property("request", request
        ).add_property("path", path)
    simple_proxy_request = rf.configure()
    return simple_proxy_request.execute()

if __name__ == '__main__':
    if len(sys.argv)  != 3:
        print('Incorrect arguments. Usage: python -m simple_proxy.proxy_app <url> <port> ') 
        sys.exit(0)

    validate = URLValidator()
    try:
        validate(sys.argv[1])
        SITE_NAME = sys.argv[1]
        app.run(host="0.0.0.0", port=sys.argv[2], debug=True)
    except ValidationError as e:
        print("please provide a valid url")

    
    