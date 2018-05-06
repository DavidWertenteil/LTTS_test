from flask import Flask, render_template, request
import json
import os
from config.common import ORDER_FIELDS

app = Flask(__name__)
path_to_order_files = 'order_files/'
cibus_number = ORDER_FIELDS[0]


@app.route('/', methods=['POST', 'GET'])
def ui():
    return render_template('menue.html', order_fields=ORDER_FIELDS)


@app.route('/get_order', methods=['POST'])
def get_order():
    order = {}
    cibus = request.form[cibus_number]
    for field in ORDER_FIELDS:
        order.update({field: request.form[field]})

    order.update({'notes': request.form['notes']})

    file_path = os.path.join(path_to_order_files, '{}.json'.format(cibus))

    if (request.form['submit'] == 'cancel'):
        order_canceled = False
        if (os.path.isfile(file_path)):
            os.remove(file_path)
            order_canceled = True
        return render_template('menue.html', order_fields=ORDER_FIELDS, order_canceled=order_canceled), 201
    else:
        print(order)
        with open(file_path, 'w') as fp:
            json.dump(order, fp, indent=4, sort_keys=True)

    return render_template('menue.html', order_fields=ORDER_FIELDS, order_done=True), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)