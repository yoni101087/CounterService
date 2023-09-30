from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

counter = 0

@app.route('/', methods=['GET', 'POST'])
def counter_service():
    global counter

    if request.method == 'POST':
        counter += 1
        return 'POST request served. Current count: {}'.format(counter)
    elif request.method == 'GET':
        return 'Current count: {}'.format(counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
