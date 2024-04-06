from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        messages_list = [message.to_dict() for message in messages]
        return jsonify(messages_list), 200
    elif request.method == 'POST':
        data = request.json
        new_message = Message(
            body=data.get('body'),
            username=data.get('username'),
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

    # if request.method == 'GET':

    #     s = Message.query.order_by(Message.created_at.sorted(reverse = False)).all()
    #     rs = [item.to_dict() for item in s]
    #     response = make_response(
    #         jsonify(rs),
    #         200
    #     )
    #     return response
    # elif request.method == 'POST':
    #     new_message  = Message(
    #         body = request.form.get('body'),
    #         username = request.form.get('username'),
    #     )
    #     db.session.add(new_message)
    #     db.session.commit()
    #     message_dict = new_message.to_dict()
    #     response = make_response(
    #         message_dict,
    #         200
    #     )
    #     return response

@app.route('/messages/<int:id>',methods =['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        response = make_response(
            {"message": "message not found"}, 
            404
            )
        return response


    elif request.method == 'PATCH':
        data = request.get_json() 
        if 'body' in data:  
            new_body = data.get('body') 
            message.body = new_body  
            db.session.commit()  
        return make_response(message.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response({"message": "message successfully deleted"}, 200)

if __name__ == '__main__':
    app.run(port=5001)
