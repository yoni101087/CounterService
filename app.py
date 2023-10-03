from flask import Flask, request
from prometheus_client import start_http_server, Counter
import random
import time

app = Flask(__name__)
counter = 0

# Create a Prometheus counter metric to track the number of POST requests
post_request_counter = Counter('post_requests_total', 'Total number of POST requests')

@app.route('/', methods=['GET', 'POST'])
def counter_service():
    global counter

    if request.method == 'POST':
        counter += 1
        # Increment the Prometheus counter metric for POST requests
        post_request_counter.inc()
        return 'POST request served. Current count: {}'.format(counter)
    elif request.method == 'GET':
        return 'Current count: {}'.format(counter)


if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 80 with the /metrics path
    start_http_server(8081)
    app.run(host='0.0.0.0', port=80)
