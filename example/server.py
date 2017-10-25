from flask import Flask
from flask_opentracing import FlaskTracer
from .tracer import jaeger as get_tracer
import opentracing


app = Flask(__name__)


tracer = FlaskTracer(lambda: get_tracer('example server'), True, app, ["url_rule"])


@app.route("/simple")
def simple_response():
    '''
    This request will be automatically traced.
    '''
    return "Hello, world!"


@app.route("/childspan")
def create_child_span():
    '''
    This request will also be automatically traced.

    This is a more complicated example of accessing the current
    request from within a handler and creating new spans manually.
    '''
    parent_span = tracer.get_span()
    child_span = opentracing.tracer.start_span("inside create_child_span", child_of=parent_span)
    ans = calculate_some_stuff()
    child_span.finish()
    return str(ans)


def calculate_some_stuff():
    two = 1 + 1
    return two
