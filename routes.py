from app import app, db
from flask import abort, jsonify, request, Response, make_response
import taskService
import userService
import json
from model.User import Users
import uuid
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[-1]

        if not token:
            return make_response( {"message": "A valid token is missing"},401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        except Exception:
            return make_response( {"message": "The token is invalid"},401)

        return f(*args, **kwargs)
    return decorator


@app.route('/register', methods=['POST'])
def signup_user():  
    data = request.get_json()  

    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = Users(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=False) 
    db.session.add(new_user)  
    db.session.commit()    

    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST'])  
def login_user(): 
 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Users.query.filter_by(username=auth.username).first()   
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    try:
        completed = None
        title = None
        if request.args.get("completed"):
            completed = json.loads(request.args.get("completed"))
            assert (isinstance(completed, bool) )
        if request.args.get("title"):
            title = request.args.get("title")
            assert isinstance(title, str)
        tasks,total_items = taskService.get_tasks(completed,title)
        return jsonify(total_items= total_items, data=tasks)
    except AssertionError as e:
        return Response(str(e),400)
      
@app.route('/tasks/<string:id>', methods=['GET'])
@token_required
def get_task_by_id(id):
    try:
        data = taskService.get_tasks_by_id(id=int(id))
        return jsonify(data)
    except AssertionError as e:
        return Response(str(e),400)

@app.route('/users', methods=['GET'])
@token_required
def get_users():
    try:
        users,total_items = userService.get_users()
        return jsonify(total_items= total_items, data=users)

    except Exception as e:
        return Response(str(e),500)    

@app.route('/users/<string:user_id>', methods=['GET'])
@token_required
def get_user_by_id(user_id):
    try:
        data = userService.get_user_by_id(user_id=int(user_id))
        if data == None:
            abort(404)
        return jsonify(data)
    except AssertionError as e:
        return Response(str(e),400)

@app.route('/users/<string:user_id>/tasks', methods=['GET'])
@token_required
def get_tasks_by_user_id(user_id):
    try:
        completed = None
        title = None
        if request.args.get("completed"):
            completed = json.loads(request.args.get("completed"))
            assert (isinstance(completed, bool) )
        if request.args.get("title"):
            title = request.args.get("title")
            assert isinstance(title, str)
            
        if userService.verify_user(int(user_id)):
            tasks, total_items = taskService.get_tasks_by_user_id(completed= completed, title= title,user_id=int(user_id))
            return jsonify(total_items= total_items, data=tasks)
        else:
            return make_response({"message": "User does not exist"},400)
    except AssertionError as e:
        return Response(str(e),400)