from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose InfoSys database
db = client['InfoSys']
students = db['Students']

# Initiate Flask App
app = Flask(__name__)

# Insert Student


@app.route('/insertstudent', methods=['POST'])
def insert_student():

    # Request and parse the JSON data
    try:
        json_data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad request", status=500, mimetype='application/json')
    
    data = json_data

    # Return response according to the json received
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data or not "yearOfBirth" in data or not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    if not "street" in data["address"] or not "postcode" in data["address"] or not "city" in data["address"]:
        return Response("Address information incomplete", status=500, mimetype="application/json")

    if students.find({"email": json_data["email"]}).count() == 0:
        student = {
            "email": json_data["email"],
            "name": json_data["name"],
            "yearOfBirth": json_data["yearOfBirth"],
            "address": [
                {
                    "street": json_data["address"]["street"],
                    "city":  json_data["address"]["city"],
                    "postcode":  json_data["address"]["postcode"]
                }
            ]
        }
        # Add student to the 'students' collection
        students.insert_one(student)
        return Response("User with email " + str(json_data["email"])+" was added to the MongoDB", status=200, mimetype='application/json')
    else:
        return Response("A user with the given email already exists", status=200, mimetype='application/json')


# Read Operations
# Get all students
@app.route('/getallstudents', methods=['GET'])
def get_all_students():
    iterable = students.find({})
    output = []
    for student in iterable:
        student['_id'] = None
        output.append(student)
    return jsonify(output)


# Get the number of all the students in the DB
@app.route('/getstudentcount', methods=['GET'])
def get_students_count():
    number_of_students = students.find({}).count()
    return jsonify({"Number of students": number_of_students})


# Find student by email
@app.route('/getstudent/<string:email>', methods=['GET'])
def get_student_by_email(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email": email})
    if student != None:
        student = {'_id': str(student["_id"]), 'name': student["name"],
                   'email': student["email"], 'yearOfBirth': student["yearOfBirth"]}
        return jsonify(student)
    return Response('no student found', status=500, mimetype='application/json')


# Get Students with addresses
@app.route('/getStudentsWithAddress', methods=['GET'])
def get_students_w_addresses():
    # Find all students that have the address fields with empty values
    students_w_address = students.find(
        {"address": {"$exists": "true", "$ne": ""}})
    output = []
    for student in students_w_address:
        student['_id'] = None
        output.append(student)
    return jsonify(output)


# Find student's address via email
@app.route('/getStudentsAddress/<string:email>', methods=['GET'])
def get_student_adress(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    # Search by email
    student = students.find_one({"email": email})
    if student != None:

        # Form 'student' in json
        try:
            student = {'_id': str(student["_id"]), 'name': student["name"],
                   'address': student["address"], 'email': student["email"]}
        except Exception as e:
            return Response('The user has no address', status=500, mimetype='application/json')
        else:
            return jsonify(student)
    return Response('no student found', status=500, mimetype='application/json')


# Find students born in the 80s that have an address
@app.route('/getEightiesAddress', methods=['GET'])
def get_Eighties_Address():
    eighties_students = students.find({"$and": [{"yearOfBirth": {"$gte": 1980, "$lte": 1989}}, {
        "address": {"$exists": "true", "$ne": ""}}]})
    output = []
    if eighties_students != None:
        for student in eighties_students:
            student['_id'] = None
            output.append(student)
    return jsonify(output)
    return Response('No students were born in the 80s', status=500, mimetype='application/json')


# Count all the students that have addresses
@app.route('/countAddress', methods=['GET'])
def count_students_with_address():
    results = students.find({"address": {"$exists": "true", "$ne": ""}})
    results_count = results.count()
    if results_count == 0:
        return Response('no students were found without addresses', status=500, mimetype='application/json')
    output = {'count': results_count}
    return jsonify(output)


# Count students born on the same year
@app.route('/countYearOfBirth/<int:year>', methods=['GET'])
def count_year_of_birth(year):
    # Search by year of birth and count the results
    count = students.find({"yearOfBirth": {"$eq": year}}).count()
    if count == 0:
        return Response('No students were found born on year '+str(year), status=500, mimetype='application/json')
    output = {'count': count}
    return jsonify(output)


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)