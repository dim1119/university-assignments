import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json, os, sys, uuid, time
from bson.objectid import ObjectId


mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')


db = client['DSMarkets']
users = db['Users']
products = db['Products']

users_sessions = {}

# Initiate Flask App
app = Flask(__name__)

# Session creation 
def create_session(username):
	user_uuid = str(uuid.uuid1())
	users_sessions[user_uuid] = (username, time.time())
	return user_uuid

# Session validation
def is_session_valid(user_uuid):
	return user_uuid in users_sessions

# Check if uuid belongs to an admin
# based on the email
def is_admin(uuid):
	email = users_sessions[uuid][0]
	user = users.find_one({"email": email})
	if user["category"]=="admin":
		return True
	else:
		return False


# Initiliaze cart
cart = [{"Total": 0}]

@app.route('/register', methods=['POST'])
def register():
	# Request JSON data
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	if not "name" in data or not "email" in data or not "password" in data:
		return Response("Information incomplete", status=500, mimetype="application/json")

	# Search for the specific email. if none found, insert the new email, name and password in the database


	if users.find({"email": data["email"]}).count() == 0:

		# Create a new user or admin
		if "category" in data:
			if data["category"]=="admin" or data["category"]=="administrator":
				user = {
					"email": data["email"],
					"password": data["password"],
					"name": data["name"],
					"category": "admin"
				}	
			elif data["category"]=="user":
				user = {
					"email": data["email"],
					"password": data["password"],
					"name": data["name"],
					"category": "user"
				}
			else:
				return Response("Invalid user category(user/admin)", status=400, mimetype='application/json')
		else:
			user = {
					"email": data["email"],
					"password": data["password"],
					"name": data["name"],
					"category": "user"
				}

		users.insert_one(user)
		return Response(data['email']+" was added to the MongoDB", status=200, mimetype='application/json')
	else:
		return Response("A user with the given email already exists", status=400, mimetype='application/json')


@app.route('/login', methods=['POST'])
def login():
	# Request JSON data
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	if not "email" in data or not "password" in data:
		return Response("Information incomplete", status=500, mimetype="application/json")

	user = users.find_one({"email": data["email"]})

	# After searching for the email check for the password using a try/except
	try:
		if user["password"] == data["password"]:
			valid_password = True
		else:
			valid_password = False
	except Exception as e:
		valid_password = False
	finally:
		if valid_password:
			user_uuid = create_session(user["email"])
			res = {"uuid": user_uuid, "email": data['email']}
			return Response(json.dumps(res), status=200, mimetype='application/json')
		else:
			return Response("Wrong email or password.", status=400, mimetype='application/json')


@app.route('/searchProduct', methods=['POST'])
def search_product():
	# Request JSON data
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')

	# Check for the specified fields
	if (not "name" in data and not "category" in data and not "_id" in data) or len(data) != 1:
		return Response("Information incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')

	if is_session_valid(uuid):
		# Search based on the info given
		if "_id" in data:
			product_list = products.find_one({"_id": ObjectId(data["_id"])})
		elif "name" in data:
			product_list = products.find({"name": {'$regex': data["name"]}}).sort("name")
		elif "category" in data:
			product_list = products.find({"category": {'$regex': data["category"]}}).sort("price")
		else:
			Response("Error", status=401, mimetype='application/json')

		if product_list:
			# Check returned type and adapt
			if type(product_list) is dict:
				product_list["_id"]=str(product_list["_id"])
				output=product_list
			else:
				output = []
				for product in product_list:
					output.append({'name': product['name'], 'description': product['description'],
						   'price': product['price'], 'category': product['category'], 'stock': product['stock'], '_id': str(product['_id'])})
			
			# Return the items/item
			return Response(json.dumps(output), status=200, mimetype='application/json')
		else:
			Response("No product found", status=400,
					 mimetype='application/json')

	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')


@app.route('/addtoCart', methods=['POST'])
def add_cart():
	global cart

	# Request JSON data
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	if not "_id" in data or not "stock" in data:
		return Response("Information incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid):
		if not data["_id"]:
			return Response("No _id supplied", status=500, mimetype='application/json')

		# Search for the product
		product = products.find_one({"_id": ObjectId(data["_id"])})
		product["stock"]=int(product["stock"])
		product["price"]=int(product["price"])
		data["stock"]=int(data["stock"])
		if not product:
			return Response("No product found", status=400, mimetype='application/json')
		# Check for the stock
		elif product["stock"] < data["stock"]:
			return Response("stock of " + data["_id"] + " is not sufficient(max " + max_stock + ")", status=500, mimetype='application/json')

		# Append to cart 
		cart.append({"_id":data["_id"], "stock":data["stock"], "price":product["price"]})

		# Add to total sum
		cart[0]["Total"]+= data["stock"] * product["price"]
		return Response("Added " + data["_id"] + " " + str(data["stock"]) + " times to cart", status=200, mimetype='application/json')

	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')


@app.route('/getCart', methods=['GET'])
def get_cart():
	global cart

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid):
		# Return the cart
		return Response(json.dumps(cart), status=200, mimetype='application/json')

	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')


@app.route('/deletefromCart', methods=['DELETE'])
def delete_cart():
	global cart

	# Request JSON data
	data = None
	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	if not "_id" in data:
		return Response("Information incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid):
		if not "_id" in data:
			return Response("No id supplied", status=500, mimetype='application/json')

		# Search for the id
		found=False
		minus=0
		for item in list(cart):
			try:
				# Calculate the price*stock
				if data["_id"]==item["_id"]:
					minus=int(item["price"])*int(item["stock"])
					cart.remove(item)
					found=True
					break
			except Exception as e:
				continue
			
		# Change the total sum
		cart[0]["Total"]=cart[0]["Total"]-minus
		return Response("Item " + data["_id"]+" was deleted from cart", status=200, mimetype='application/json')

	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')


@app.route('/checkout', methods=['POST'])
def checkout():
	global cart
	# Request JSON data
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	elif not "card" in data or len(data["card"]) != 16 or not data["card"].isnumeric():
		return Response("Card Information Incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid):

		# Go throught all the items in the cart 
		# and update the stock on the db
		for product in next(iter(cart)):
			try:
				products.update({"_id": ObjectId(product["_id"])}, {"$subtract":{["stock",product["stock"]]}})
			except Exception as e:
				continue
		
		del cart[1:]
		value=cart[0]["Total"]
		cart[0]["Total"]=0
		
		return Response("Total value is " + str(value), status=200, mimetype='application/json')

	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')


@app.route('/deleteAccount', methods=['DELETE'])
def delete_account():
	uuid = request.headers.get('authorization')
	if is_session_valid(uuid):
		email = users_sessions[uuid][0]
		user = users.find_one({"email": email})
		if user is None:
			msg = "No user was found with your session id."
			return Response(msg, status=400, mimetype='application/json')
		# Delete user based on id
		users.delete_one({"email": email})
		msg = email + " with session id " + uuid + " was deleted."
		users_sessions.pop(uuid)
		return Response(msg, status=200, mimetype='application/json')
	else:
		return Response("Session is not valid.", status=401, mimetype='application/json')



@app.route('/addProduct', methods=['POST'])
def add_product():
	uuid = request.headers.get('authorization')
	if is_session_valid(uuid) and is_admin(uuid):
		 # Request JSON data
		data = None
		try:
			data = json.loads(request.data.decode('utf-8'))
		except Exception as e:
			return Response("bad json content", status=500, mimetype='application/json')
		if data is None:
			return Response("bad request", status=500, mimetype='application/json')
		elif not "name" in data or not "price" in data or not "description" in data or not "category" in data or not "stock" in data:
			return Response("Information incomplete", status=500, mimetype="application/json")

		# Create a new product and insert into the db
		new_product = {
		"name": data["name"], "price": data["price"], "description": data["description"],
		"category": data["category"], "stock": data["stock"]
		}


		output = products.insert_one(new_product)
		return Response("Product " + data["name"] + " was added.", status=200, mimetype='application/json')

	else:
	    return Response("Session is not valid or user is not an administrator.", status=401, mimetype='application/json')


@app.route('/deleteProduct', methods=['DELETE'])
def delete_product():
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	elif not "_id" in data:
		return Response("Information incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid) and is_admin(uuid):

		# Find and delete based on the _id
		product = products.find_one({"_id": ObjectId(data["_id"])})

		if not product:
			return Response("No product found", status=400, mimetype='application/json')

		output = products.delete_one({"_id": ObjectId(data["_id"])})

		return Response("User deleted and uuid invalidated", status=200, mimetype='application/json')
	else:
		return Response("Session is not valid or user is not an administrator.", status=401, mimetype='application/json')


@app.route('/updateProduct', methods=['PUT'])
def update_product():
	data = None
	try:
		data = json.loads(request.data.decode('utf-8'))
	except Exception as e:
		return Response("bad json content", status=500, mimetype='application/json')
	if data is None:
		return Response("bad request", status=500, mimetype='application/json')
	elif ( not "_id" in data ) and not ("name" in data or "price" in data or "description" in data or "stock" in data):
		return Response("Information incomplete", status=500, mimetype="application/json")

	uuid = request.headers.get('authorization')
	if is_session_valid(uuid) and is_admin(uuid):

		# Update the fields provided
		for field in data:
			if "_id" in field:
				continue
			products.update({"_id": ObjectId(data["_id"])}, {"$set":{field: data[field]}})

		return Response("Updated product", status=200, mimetype='application/json')    
	else:
		return Response("Session is not valid or user is not an administrator.", status=401, mimetype='application/json')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
