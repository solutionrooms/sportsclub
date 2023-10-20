from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and configure SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

Swagger(app)


# Define Organisation model
class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Define People model
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    person_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Define Session model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    session_description = db.Column(db.Text)
    session_start_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define SessionPeople model
class SessionPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)


# Define SessionGame model
class SessionGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    game_start_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define GameTeam model
class GameTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('session_game.id'), nullable=False)


# Define GameTeamPeople model
class GameTeamPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_team_id = db.Column(db.Integer, db.ForeignKey('game_team.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)


@app.route('/crud/<string:table>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def crud_operations(table):
    """
    CRUD API
    ---
    tags:
      - CRUD Operations
    parameters:
      - name: table
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            id:
              type: integer
            org_name:
              type: string
            person_name:
              type: string
            organisation_id:
              type: integer
    responses:
      200:
        description: Success
    """
    if table == 'organisation':
        model = Organisation
    elif table == 'people':
        model = People
    elif table == 'session':
        model = Session
    elif table == 'session_people':
        model = SessionPeople
    elif table == 'session_game':
        model = SessionGame
    elif table == 'game_team':
        model = GameTeam
    elif table == 'game_team_people':
        model = GameTeamPeople
    else:
        return jsonify({"message": "Invalid table name"}), 400

    if request.method == 'POST':
        new_item = model(**request.json)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item created"}), 201

    elif request.method == 'GET':
        items = model.query.all()
        return jsonify([item.to_dict() for item in items]), 200

    elif request.method == 'PUT':
        item = model.query.get(request.json['id'])
        for key, value in request.json.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({"message": "Item updated"}), 200

    elif request.method == 'DELETE':
        item = model.query.get(request.json['id'])
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200

    elif request.method == 'PATCH':
        item = model.query.get(request.json['id'])
        if item is None:
            return jsonify({"message": "Item not found"}), 404
        for key, value in request.json.items():
            if hasattr(item, key):
                setattr(item, key, value)
        db.session.commit()
        return jsonify({"message": "Item partially updated"}), 200


# Route to initialize database
@app.route('/init')
def init_db():
    """
    init API
    ---

    responses:
      200:
        description: Success
    """
    db.create_all()
    org1 = Organisation(org_name='Org1')
    org2 = Organisation(org_name='Org2')
    db.session.add(org1)
    db.session.add(org2)
    db.session.commit()

    person1 = People(organisation_id=1, person_name='Person1')
    person2 = People(organisation_id=2, person_name='Person2')
    db.session.add(person1)
    db.session.add(person2)
    db.session.commit()

    return jsonify({"message": "Database initialized"})


# Simple hello world route
@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, world!"})

# Uncomment below lines to run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
