from datetime import datetime
from random import uniform, choice, shuffle
from string import ascii_letters, digits
from models import db, Restaurant, Pizza, RestaurantPizza
from app import app

def generate_random_string(length):
    characters = ascii_letters + digits
    return ''.join(choice(characters) for _ in range(length))

def create_sample_data():
    # List of random pizza names to pick from
    pizza_names = ['Margherita', 'Pepperoni', 'Vegetarian', 'Hawaiian', 'Supreme',
                   'Mushroom', 'BBQ Chicken','Four Cheese','Meat Lovers','Spinach Alfredo',
                   'Buffalo Chicken','Veggie Delight','Sausage and Mushroom','Pepper and Onion',
                   'Chicken Tikka','Bacon and Pineapple','Garlic Shrimp','Pesto and Tomato',
                   'Greek','Burger'
    ]

    with app.app_context():
        pizzas = []
        shuffle(pizza_names)
        for name in pizza_names:
            ingredients = generate_random_string(20)
            pizza = Pizza(name=name, ingredients=ingredients, created_at=datetime.now(), updated_at=datetime.now())
            pizzas.append(pizza)

        db.session.add_all(pizzas)
        db.session.commit()

        restaurants = []
        for _ in range(50):
            name = generate_random_string(10)
            address = generate_random_string(30)
            restaurant = Restaurant(name=name, address=address)
            restaurants.append(restaurant)

        db.session.add_all(restaurants)
        db.session.commit()

        restaurant_pizzas = []
        for _ in range(50):
            pizza = choice(pizzas)
            restaurant = choice(restaurants)
            price = round(uniform(1.0, 30.0), 2)
            if not RestaurantPizza(pizza_id=pizza.id, restaurant_id=restaurant.id, price=price).validate():
                continue
            restaurant_pizza = RestaurantPizza(pizza_id=pizza.id, restaurant_id=restaurant.id, price=price)
            restaurant_pizzas.append(restaurant_pizza)

        db.session.add_all(restaurant_pizzas)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
