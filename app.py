from sql_connection import connect_database
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Vitoria96!@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)
    
    class Meta:
        fields = ('id', 'name', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class SessionSchema(ma.Schema):
    session_id = fields.Int(required=False)
    member_id = fields.Int(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)
    duration_minutes = fields.Int(required=True)
    calories_burned = fields.Int(required=True)
    
    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'session_time', 'activity', 'duration_minutes', 'calories_burned')

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    sessions = db.relationship('Session', backref='member', uselist=False)

class Session(db.Model):
    __tablename__ = 'WorkoutSessions'
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    session_date = db.Column(db.Date)
    session_time = db.Column(db.String(150))
    activity = db.Column(db.String(320))
    duration_minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'), unique=True)



@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods=['POST'])
def add_members():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Member(id=member_data['id'], name=member_data['name'], age=member_data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added successfully'}), 201


@app.route('/members/<int:id>', methods=['PUT'])
def update_members(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.id = member_data['id']
    member.name = member_data['name']
    member.age = member_data['age']
    db.session.commit()
    return jsonify({'message': 'Customer details upload successfully'}), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member removed successfully'}), 200

# --------------------------------------------------------------------- #
# --------------------------------------------------------------------- #
# --------------------------------------------------------------------- #

@app.route('/sessions', methods=['GET'])
def get_sessions():
    session = Session.query.all()
    return sessions_schema.jsonify(session)

@app.route('/sessions', methods=['POST'])
def add_sessions():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_session = Session(session_id=session_data['session_id'], member_id=session_data['member_id'], session_date=session_data['session_date'], session_time=session_data['session_time'], activity=session_data['activity'], duration_minutes=session_data['duration_minutes'], calories_burned=session_data['calories_burned'])
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'New session added successfully'}), 201

@app.route('/sessions/<int:session_id>', methods=['PUT'])
def update_sessions(session_id):
    session = Session.query.get_or_404(session_id)
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    session.member_id = session_data['member_id']
    session.session_date = session_data['session_date']
    session.session_time = session_data['session_time']
    session.activity = session_data['activity']
    session.duration_minutes = session_data['duration_minutes']
    session.calories_burned = session_data['calories_burned']

    db.session.commit()
    return jsonify({'message': 'Session details upload successfully'}), 200

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_sessions(session_id):
    session = Session.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session removed successfully'})


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
