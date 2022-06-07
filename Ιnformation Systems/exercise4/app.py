from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose InfoSys database
db = client['InfoSys']
courses = db['Courses']
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


# Insert a course in the DB
@app.route('/insertCourse', methods=['POST'])
def insert_course():
    # Request and parse the JSON data
    try:
        json_data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad request", status=500, mimetype='application/json')

    data = json_data

    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data or not "course_id" in data or not "ects" in data:
        return Response("Invalid Course Data", status=500, mimetype="application/json")

    if courses.find({"course_id": json_data["course_id"]}).count() == 0:
        course = {
            "course_id": json_data["course_id"],
            "name": json_data["name"],
            "ects": int(json_data["ects"])
        }
        courses.insert_one(course)
        return Response("Course was added to the MongoDB", status=200, mimetype='application/json')
    else:
        return Response("A lessons with the same ID exists", status=200, mimetype='application/json')

# Get a course's details
@app.route('/get-course', methods=['GET'])
def get_couse():
    course_id = request.args.get("course_id")
    if course_id == None:
        return Response("Bad request", status=500, mimetype='application/json')
    course = courses.find_one({"course_id": course_id})
    if course != None:
        if "description" not in course:
            course = {
                "course_id": course["course_id"],
                "name": course["name"],
                "ects": int(course["ects"])
            }
        else:
            course = {
                "course_id": course["course_id"],
                "name": course["name"],
                "ects": int(course["ects"]),
                "description": course["description"]
            }
        return jsonify(course)
    return Response('no course found with the id '+str(course_id), status=500, mimetype='application/json')


# Add course to student via email
@app.route('/add-course/<string:email>', methods=['PUT'])
def add_course(email):
    if request.data:
        data = json.loads(request.data.decode('utf-8'))
        output = students.update(
            {"email": email}, {"$push": {"courses": data['course_id']}})
        if(output["updatedExisting"] == 1):
            return Response("Lesson " + str(data["course_id"]) + " added to email: " + email, status=200, mimetype='application/json')
    else:
        return Response("No Data provided", status=200, mimetype='application/json')


# Delete student via email
@app.route('/delete-student', methods=['DELETE'])
def delete():
    email = request.args.get("email")
    if not email:
        return Response("No email was provided", status=200, mimetype='application/json')
    output = students.remove({"email": email})
    if output['n'] == 0:
        return Response("No student was found with that email", status=200, mimetype='application/json')
    return Response("Student with email:" + email + " was deleted", status=200, mimetype='application/json')


# Add a description to a course
@app.route('/insert-course-description', methods=['POST'])
def insert_course_description():
    course_id = request.args.get("course_id")
    description = json.loads(request.data.decode('utf-8'))["description"]
    if not course_id or not description:
        return Response("No course_id or description was provided", status=200, mimetype='application/json')
    output = courses.update({"course_id": course_id}, {
                            "$set": {"description": description}})
    if(output["updatedExisting"] == 1):
        return Response("Added description in course with id " + str(course_id), status=200, mimetype='application/json')
    return Response("There has been an error", status=200, mimetype='application/json')



# Update a course
@app.route('/update-course', methods=['PUT'])
def update_course():
    course_id = request.args.get("course_id")
    if course_id:
        data = json.loads(request.data.decode('utf-8'))
        if not "name" in data or not "course_id" in data or not "ects" in data or not "description" in data:
            return Response("Invalid Course Data", status=500, mimetype="application/json")
        output = courses.update({"course_id": course_id}, {"$set": {
                                "course_id": data['course_id'], "name": data['name'], "ects": data['ects'], "description": data["description"]}})

        if(output["updatedExisting"] == 1):
            return Response("Course " + str(data["course_id"]) + " was updated", status=200, mimetype='application/json')
        else:
            return Response("Course with that id was not found", status=200, mimetype='application/json')
    else:
        return Response("No course_id was provided", status=200, mimetype='application/json')


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
