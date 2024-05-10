import os

from flask import Flask, request, jsonify, Response

import api.validators as validators
from api.middleware import Middleware
# from api.invoice import invoicegen
from api.utlis import DBHandle
import traceback


app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)
db = DBHandle()


@app.post("/pdfgen")
def pdfgen():
    try:
        payload = request.get_json()
        # if not validate_payload(payload):
        #     return jsonify({"msg": "Bad Request"}), 400
        print(payload)
        # file = invoicegen(
        #     payload['items'],
        #     "arjun",
        #     "908090090",
        # )
    except KeyError as e:
        return jsonify({"msg": "Bad Request" + str(e)}), 400
    return Response({}, mimetype="application/pdf", headers={"Content-Disposition": "attachment;filename=report.pdf"})



@app.get("/customer")
def getcustomers():
    try:
        products = db.get_documents("customers")
        return jsonify({'data': products})
    except Exception as e:
        return jsonify({'msg': "Internal Server Error" + repr(e)}), 500


@app.post("/product")
def addproduct():
    try:
        payload = request.get_json()
        if not validators.product(payload):
            return jsonify({'msg': "Bad Request"}), 400
        db.add_document(payload, "products", db.Products)
        return jsonify({'msg': 'ok'}), 200
    except Exception as e:
        return jsonify({'msg': "Internal Server Error" + repr(e)+ " " + traceback.format_exc()}), 500


@app.post('/customer')
def addcustomer():
    try:
        payload = request.get_json()
        if not validators.customer(payload):
            return jsonify({'msg': "Bad Request"}), 400
        db.add_document(payload, "customers", db.Customer)
        return jsonify({'msg': 'ok'}), 200
    except Exception as e:
        return jsonify({'msg': "Internal Server Error" + repr(e)}), 500


@app.get("/product")
def getproducts():
    try:
        products = db.get_documents("products")
        return jsonify({'data': products})
    except Exception as e:
        return jsonify({'msg': "Internal Server Error" +repr(e)}), 500


