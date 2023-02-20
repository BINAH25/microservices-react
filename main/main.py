import os
from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate

from dotenv import load_dotenv
load_dotenv()

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    # for serializing into json
    id: int 
    title: str 
    image: str 

    # for db
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) # product_id created in django
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    # no likes -> in django

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # not sure if working ?
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(db.session.query(Product).all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        product_user = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        publish('product_liked', id)
    except Exception as e:
        print(e)
        abort(400, 'You already liked this product.')

    return jsonify({
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='8080')