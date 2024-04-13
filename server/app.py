from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'GET':
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return make_response(jsonify(bakeries), 200)
    elif request.method == 'POST':
        data = request.form
        bakery = Bakery(name=data['name'])
        db.session.add(bakery)
        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 201)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    if request.method == 'GET':
        return make_response(jsonify(bakery.to_dict()), 200)
    elif request.method == 'PATCH':
        data = request.form
        if 'name' in data:
            bakery.name = data['name']
        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 200)
    elif request.method == 'DELETE':
        db.session.delete(bakery)
        db.session.commit()
        return make_response(jsonify({'message': 'Bakery deleted successfully'}), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(jsonify(baked_goods), 200)
    elif request.method == 'POST':
        data = request.form
        baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=data['bakery_id'])
        db.session.add(baked_good)
        db.session.commit()
        return make_response(jsonify(baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def baked_good_by_id(id):
    baked_good = BakedGood.query.get_or_404(id)
    if request.method == 'GET':
        return make_response(jsonify(baked_good.to_dict()), 200)
    elif request.method == 'PATCH':
        data = request.form
        if 'name' in data:
            baked_good.name = data['name']
        if 'price' in data:
            baked_good.price = data['price']
        if 'bakery_id' in data:
            baked_good.bakery_id = data['bakery_id']
        db.session.commit()
        return make_response(jsonify(baked_good.to_dict()), 200)
    elif request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()
        return make_response(jsonify({'message': 'Baked good deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)