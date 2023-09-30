from flask import Flask, request, Response
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CollectorRegistry

app = Flask(__name__)
metrics = PrometheusMetrics(app)

counter = metrics.counter(
    'custom_counter', 'A custom counter metric for the Flask app'
)

@app.route('/', methods=['GET', 'POST'])
def counter_service():
    if request.method == 'POST':
        counter.inc()
        return 'POST request served. Current count: {}'.format(counter.get())
    elif request.method == 'GET':
        return 'Current count: {}'.format(counter.get())

# Add a route for Prometheus metrics
@app.route('/metrics')
def prometheus_metrics():
    registry = CollectorRegistry(auto_describe=True)
    data = generate_latest(registry)
    return Response(data, content_type='text/plain; version=0.0.4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
