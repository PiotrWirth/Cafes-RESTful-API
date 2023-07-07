from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(can_take_calls=random_cafe.can_take_calls,
                   coffee_price=random_cafe.coffee_price,
                   has_sockets=random_cafe.has_sockets,
                   has_toilet=random_cafe.has_toilet,
                   has_wifi=random_cafe.has_wifi,
                   id=random_cafe.id,
                   img_url=random_cafe.img_url,
                   location=random_cafe.location,
                   map_url=random_cafe.map_url,
                   name=random_cafe.name,
                   seats=random_cafe.seats)

@app.route("/all",methods=['GET'])
def all():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/search",methods=['GET'])
def search():
        query_location = request.args.get('loc')
        cafes = db.session.query(Cafe).where(Cafe.location == query_location)
        if cafes:
            return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
        else:
            return jsonify(error={"Not Forund":"Sorry,we don't have a cafe at that location"})
            



## HTTP POST - Create Record
@app.route("/add",methods=['POST'])
def add_cafe():
    return jsonify(response={"success":"Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>",methods=['PATCH'])
def update_coffee_price(cafe_id):
    query_price = request.args.get('new_price')
    cafe = db.get_or_404(Cafe, cafe_id)
    cafe.coffee_price = query_price
    db.session.commit()
    return jsonify(response={"Success":"Price was changed successfully"})

## HTTP DELETE - Delete Record
API_KEY="TopSecretAPIKey"
@app.route("/report-closed/<cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key')
    if api_key==API_KEY:
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(respond={"Success":"Successfully deleted"})
        else:
            return jsonify(respond={"Not Found":"Sorry,a cafe with that id was not found in the database."})
    else:
        return jsonify(respond={"error":"Sorry,that's not allowed. Make sure you have the correct api_key"})
if __name__ == '__main__':
    app.run(debug=True)
