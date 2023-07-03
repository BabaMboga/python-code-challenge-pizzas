#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/pizzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        data = [{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants]
        return jsonify(data)

api.add_resource(Restaurants, '/restaurants')

class RestaurantsById(Resource):
    def get(self,id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return{'error': 'Restaurant not found'}, 404
        
        pizzas = []
        for restaurant_pizza in restaurant.restaurant_pizzas:
            pizza = Pizza.query.get(restaurant_pizza.pizza_id)
            pizzas.append({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})

        response_body = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': pizzas
        }

        return jsonify(response_body)
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {'error': 'Restaurant not found'}, 404
        #Delete the associated restaurant pizzas
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()

        db.session.delete(restaurant)
        db.session.commit()
        return {'success': 'Record successfully deleted'}, 204
    
api.add_resource(RestaurantsById,'/restaurants/<int:id>')




if __name__ == '__main__':
    app.run(port=5555)
