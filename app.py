from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'appsqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=True)
    comment = db.Column(db.String(150), unique=False)

    def __init__(self, name, email, comment):
        self.name = name
        self.email = email
        self.comment = comment

class ContactSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'comment')

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)   

#Endpoint to create an entry

@app.route('/contact', methods=["POST"])
def add_contact():
    name = request.json['name']
    email = request.json['email']
    comment = request.json['comment']

    new_contact = Contact(name,email,comment)

    db.session.add(new_contact)
    db.session.commit()

    contact = Contact.query.get(new_contact.id)

    return contact_schema.jsonify(contact)

@app.route('/contacts', methods=["GET"])
def get_contacts():
    all_contacts = Contact.query.all()
    result = contacts_schema.dump(all_contacts)

    return jsonify(result)

@app.route('/contact/<id>', methods=["PUT"])
def update_contact(id):
    contact = Contact.query.get(id)

    name = request.json['name']
    email = request.json['email']
    comment = reqeust.json['comment']

    db.session.commit()
    return contact_schema.jsonify(contact)

@app.route('/contact/<id>', methods=["DELETE"])
def get_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()

    return "CONTACT DELETED"

if __name__=='__main__':
    app.run(debug=True)    




