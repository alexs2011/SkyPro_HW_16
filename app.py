import datetime
import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        user_data = User.query.all()
        return jsonify([user.to_dict() for user in user_data]), 200
    if request.method == 'POST':
        new_user = json.loads(request.data)
        new_user_obj = User(
            id=new_user['id'],
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            age=new_user['age'],
            email=new_user['email'],
            role=new_user['role'],
            phone=new_user['phone']
        )

        db.session.add(new_user_obj)
        db.session.commit()
        db.session.close()
        return "Пользователь создан", 200


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(uid: int):
    if request.method == 'GET':
        user = User.query.get(uid)
        return jsonify(user.to_dict()) if user else {}
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        user = db.session.query(User).get(uid)
        if not user:
            return "Пользователь не найден", 404

        user.first_name = new_data['first_name']
        user.last_name = new_data['last_name']
        user.age = new_data['age']
        user.email = new_data['email']
        user.role = new_data['role']
        user.phone = new_data['phone']

        db.session.add(user)
        db.session.commit()
        db.session.close()
        return "Пользователь изменён", 200
    if request.method == 'DELETE':
        user = db.session.query(User).get(uid)
        if not user:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return "Пользователь удалён", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        order_data = Order.query.all()
        return jsonify([order.to_dict() for order in order_data]), 200
    if request.method == 'POST':
        new_order = json.loads(request.data)

        start_month, start_day, start_year = [int(i) for i in new_order['start_date'].split('/')]
        end_month, end_day, end_year = [int(i) for i in new_order['end_date'].split('/')]

        start_date_formatted = datetime.date(year=start_year, month=start_month, day=start_day)
        end_date_formatted = datetime.date(year=end_year, month=end_month, day=end_day)

        new_order_obj = Order(
            id=new_order['id'],
            name=new_order['name'],
            description=new_order['description'],
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            address=new_order['address'],
            price=new_order['price'],
            customer_id=new_order['customer_id'],
            executor_id=new_order['executor_id']
        )

        db.session.add(new_order_obj)
        db.session.commit()
        db.session.close()
        return "Заказ создан", 200


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(order_id: int):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        return jsonify(order.to_dict()) if order else {}
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if not order:
            return "Заказ не найден", 404

        start_month, start_day, start_year = [int(i) for i in new_data['start_date'].split('/')]
        end_month, end_day, end_year = [int(i) for i in new_data['end_date'].split('/')]

        start_date_formatted = datetime.date(year=start_year, month=start_month, day=start_day)
        end_date_formatted = datetime.date(year=end_year, month=end_month, day=end_day)

        order.name = new_data['name']
        order.description = new_data['description']
        order.start_date = start_date_formatted
        order.end_date = end_date_formatted
        order.address = new_data['address']
        order.price = new_data['price']
        order.customer_id = new_data['customer_id']
        order.executor_id = new_data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return "Заказ изменён", 200
    if request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if not order:
            return "Заказ не найден", 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return "Заказ удалён", 200


@app.route('/offers', methods=['GET', 'POST'])
def offer():
    if request.method == 'GET':
        offer_data = Offer.query.all()
        return jsonify([offer.to_dict() for offer in offer_data]), 200
    if request.method == 'POST':
        new_offer = json.loads(request.data)
        new_offer_obj = Offer(
            id=new_offer['id'],
            order_id=new_offer['order_id'],
            executor_id=new_offer['executor_id']
        )

        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(offer_id: int):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        return jsonify(offer.to_dict()) if offer else {}
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if not offer:
            return "Предложение не найдено", 404

        offer.order_id = new_data['order_id']
        offer.executor_id = new_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return "Предложение изменено", 200
    if request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if not offer:
            return "Предложение не найдено", 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return "Предложение удалено", 200


if __name__ == '__main__':
    app.run(debug=True)
