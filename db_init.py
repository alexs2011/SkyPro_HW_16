import datetime

import data
from models import *

db.drop_all()
db.create_all()

for user in data.USERS:
    db.session.add(User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    ))

for order in data.ORDERS:
    start_month, start_day, start_year = [int(i) for i in order['start_date'].split('/')]
    end_month, end_day, end_year = [int(i) for i in order['end_date'].split('/')]

    start_date_formatted = datetime.date(year=start_year, month=start_month, day=start_day)
    end_date_formatted = datetime.date(year=end_year, month=end_month, day=end_day)

    db.session.add(Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=start_date_formatted,
        end_date=end_date_formatted,
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    ))

for offer in data.OFFERS:
    db.session.add(Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    ))

db.session.commit()
