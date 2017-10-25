from flask import Flask
from flask_opentracing import FlaskTracer
from .tracer import jaeger as get_tracer
import opentracing
import urllib2


app = Flask(__name__)


tracer = None


@app.before_first_request
def init_tracer():
    global tracer
    tracer = FlaskTracer(get_tracer('example client'), True, app, ["url_rule"])


@app.route("/")
def index():
    '''
    Index page, has no tracing.
    '''
    return "Index Page"


@app.route("/request/<script>/<int:numrequests>")
# @opentracing.tracer.trace("url")
def send_multiple_requests(script, numrequests):
    '''
    Traced function that makes a request to the server
    Injects the current span into headers to continue trace
    '''
    span = tracer.get_span()

    def send_request():
        url = "http://localhost:5000/"+str(script)
        request = urllib2.Request(url)
        inject_as_headers(tracer, span, request)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as ue:
            response = ue
        print(response)
    for i in range(numrequests):
        send_request()
    return "Requests sent"


@app.route('/log')
# @opentracing.tracer.trace()
def log_something():
    '''
    Traced function that logs something to the current
    request span.
    '''
    span = tracer.get_span()
    span.log_event("hello world")
    return "Something was logged"


@app.route("/test")
# @opentracing.tracer.trace()
def test_lightstep_tracer():
    '''
    Simple traced function to ensure the tracer works.
    '''
    return "No errors"


def inject_as_headers(tracer, span, request):
    text_carrier = {}
    tracer.inject(span.context, opentracing.Format.TEXT_MAP, text_carrier)
    for k, v in text_carrier.iteritems():
        request.add_header(k, v)
