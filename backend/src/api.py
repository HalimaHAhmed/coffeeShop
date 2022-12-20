import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink,db
from .auth.auth import AuthError, requires_auth
from collections.abc import Mapping

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# with app.app_context():
#      db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# @app.route('/')
# def hello():cd
#     return 'hello halimah'
@app.get('/drinks')
def get_drinks():
    drinks = db.session.query(Drink).all()
    all_drinks = [drink.short() for drink in drinks]
    return {
        "success": True,
        "drinks": all_drinks
    }


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.get('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    drinks = Drink.query.all()
    get_drink_details =[drink.long() for drink in drinks ]

    return jsonify({
        'success':True,
        'drinks':get_drink_details
    })
    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.post('/drinks')
@requires_auth('post:drinks')
def create_drinks(jwt):
    body= request.get_json()

   
    title = body.get('title')
    recipe =json.dumps(body.get('recipe'))
    
    drink = Drink(recipe=f"{recipe}",title=title)
    drink.insert()

    drinks = Drink.query.all()
    all_drinks = [drink.long() for drink in drinks]


    return jsonify({
        'success':True,
        'drinks':all_drinks
    })



    

    pass

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.patch('/rinks/<id>')
@requires_auth('patch:drinks')
def create_patch(id,jwt):
    drink_to_update = db.session.query(Drink).filter(Drink.id==id).one_or_none
    if drink_to_update is None:
        abort(404)
    data = request.get_json()
    title = data.get('title')
    recipe = json.dumps(data.get('recipe'))

    drink_to_update.update()
    drinks = Drink.query.all()
    all_drinks = [drink.long() for drink in drinks]

    
    
    return jsonify({
        'success': True,
        'drinks': all_drinks

    })


    






        

   
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.delete('/drinks/<id>')
@requires_auth('delete:drinks')
def delete_drink(jwt,id):
    drink_to_delete = db.session.query(Drink).filter(Drink.id == id).one_or_none()

    if  drink_to_delete is None:
        abort(404)

    try:
        drink_to_delete.delete()
        return jsonify({'success': True, 'delete': id})
    except :
        abort(404)

    



    pass
# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404





'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def not_found(error):

    return jsonify({
        'success':False,
        'error':401,
        'message': 'unAutherized'

    }),401