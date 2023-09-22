from flask import Flask, request
from prometheus_client import start_http_server, Counter

app = Flask(__name__)
counter = 0

# Create a Counter metric for request counts
requests_counter = Counter('my_microservice_requests_total', 'Total number of requests received by the microservice')

@app.route('/', methods=['GET', 'POST'])
def counter_service():
    global counter
    
    if request.method == 'POST':
        counter += 1
        # Increment the requests_counter metric when handling a POST request
        requests_counter.inc()
        return 'POST request served. Current count: {}'.format(counter)
    elif request.method == 'GET':
        # Increment the requests_counter metric when handling a GET request
        requests_counter.inc()
        return 'Current count: {}'.format(counter)

if __name__ == '__main__':
    # Start an HTTP server to expose Prometheus metrics on port 8000
    start_http_server(8000)
    
    # Start your Flask app on port 80
    app.run(host='0.0.0.0', port=80)
