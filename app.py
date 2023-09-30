from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, path='/metrics')  

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
