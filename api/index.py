from flask import Flask, request, jsonify, Response

import api.validators as validators
from api.invoice import invoicegen
from os import getenv
from api.utlis import DBHandle
import logging
import traceback



app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

db = DBHandle()


@app.post("/pdfgen")
def pdfgen():
    try:
        payload = request.get_json()
        # if not validate_payload(payload):
        #     return jsonify({"msg": "Bad Request"}), 400
        print(payload)
        file = invoicegen(
            payload['items'],
            "arjun",
            "908090090",
        )
    except KeyError as e:
        return jsonify({"msg": "Bad Request" + str(e)}), 400
    return Response(file, mimetype="application/pdf", headers={"Content-Disposition": "attachment;filename=report.pdf"})

@app.post('/customer')
def addcustomer():
    try:
        payload = request.get_json()
        print(payload)
        if not validators.customer(payload):
            return jsonify({'msg': "Bad Request"}), 400
        db.add_document(payload, "customers", db.Customer)
        return jsonify({'msg': 'ok'}), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'msg': "Internal Server Error"}), 500


@app.get("/customer")
def getcustomers():
    try:
        products = db.get_documents("customers")
        return jsonify({'data': products})
    except Exception as e:
        return jsonify({'msg': "Internal Server Error"}), 500


@app.post("/product")
def addproduct():
    try:
        payload = request.get_json()
        if not validators.product(payload):
            return jsonify({'msg': "Bad Request"}), 400
        db.add_document(payload, "products", db.Products)
        return jsonify({'msg': 'ok'}), 200
    except Exception as e:
        return jsonify({'msg': "Internal Server Error"}), 500


@app.get("/product")
def getproducts():
    try:
        products = db.get_documents("products")
        return jsonify({'data': products})
    except Exception as e:
        return jsonify({'msg': "Internal Server Error"}), 500


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
