#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Gift

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!
@app.get('/gifts')
def get_gifts():
    gifts = Gift.query.all()
    gifts_to_dict = [g.to_dict() for g in gifts]
    return make_response(jsonify(gifts_to_dict), 200)

@app.get('/gifts/<int:id>')
def get_gift_by_id(id):
    gift = Gift.query.filter(Gift.id == id).first()
    if not gift:
        return {'error': 'not found'}, 404
        # return make_response(jsonify({'error': 'not found'}), 404)
        
    return gift.to_dict(), 200 #shortcut ver.
    # return make_response(jsonify(gift.to_dict()), 200)
    
@app.post('/gifts')
def post_gift():
    data = request.json
    
    try:
        gift = Gift(
            name = data['name'],
            price = data['price']
        )
        db.session.add(gift)
        db.session.commit()
        return gift.to_dict(), 201
    except:
        return {'error': 'Shumting Wong! cannot add'}, 406
    
@app.delete('/gifts/<int:id>')
def delete_gift(id):
    gift = Gift.query.filter(Gift.id == id).first()
    if not gift:
        return {'error': 'not found'}, 404
    db.session.delete(gift)
    db.session.commit()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
