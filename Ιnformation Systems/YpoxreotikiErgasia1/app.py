from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
    Το συγκεκριμένο endpoint θα δέχεται στο body του request του χρήστη ένα json της μορφής: 

    {
        "usename": "some username", 
        "password": "a very secure password"
    }

    * Θα πρέπει να εισαχθεί ένας νέος χρήστης στο σύστημα, ο οποίος θα εισάγεται στο collection Users (μέσω της μεταβλητής users). 
    * Η εισαγωγή του νέου χρήστη, θα γίνεται μόνο στη περίπτωση που δεν υπάρχει ήδη κάποιος χρήστης με το ίδιο username. 
    * Αν γίνει εισαγωγή του χρήστη στη ΒΔ, να επιστρέφεται μήνυμα με status code 200. 
    * Διαφορετικά, να επιστρέφεται μήνυμα λάθους, με status code 400.
    """

    # Έλεγχος δεδομένων username / password
    # Αν δεν υπάρχει user με το username που έχει δοθεί. 
    # Να συμπληρώσετε το if statement.
    #  if ... :
        # Μήνυμα επιτυχίας

    # Search for the specific username. if none found, insert the new username and password in the database
    if users.find({"username": data["username"]}).count() == 0:
        user={
        "username":data["username"],
        "password":data["password"]
        }

        users.insert_one(user)
        return Response(data['username']+" was added to the MongoDB",status=200, mimetype='application/json')
    # Διαφορετικά, αν υπάρχει ήδη κάποιος χρήστης με αυτό το username.
    else:
        # Μήνυμα λάθους (Υπάρχει ήδη κάποιος χρήστης με αυτό το username)
        return Response("A user with the given username already exists",status=400, mimetype='application/json')
    

# ΕΡΩΤΗΜΑ 2: Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Να καλεστεί η συνάρτηση create_session() (!!! Η ΣΥΝΑΡΤΗΣΗ create_session() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) 
        με παράμετρο το username μόνο στη περίπτωση που τα στοιχεία που έχουν δοθεί είναι σωστά, δηλαδή:
        * το data['username'] είναι ίσο με το username που είναι στη ΒΔ (να γίνει αναζήτηση στο collection Users) ΚΑΙ
        * το data['password'] είναι ίσο με το password του συγκεκριμένου χρήστη.
        * Η συνάρτηση create_session() θα επιστρέφει ένα string το οποίο θα πρέπει να αναθέσετε σε μία μεταβλητή που θα ονομάζεται user_uuid.
        
        * Αν γίνει αυθεντικοποίηση του χρήστη, να επιστρέφεται μήνυμα με status code 200. 
        * Διαφορετικά, να επιστρέφεται μήνυμα λάθους με status code 400.
    """

    # Έλεγχος δεδομένων username / password
    # Αν η αυθεντικοποίηση είναι επιτυχής. 
    # Να συμπληρώσετε το if statement.
    # if ... :
    user = users.find_one({"username": data["username"]})
    
    # After searching for the username check for the password using a try/except
    try:
        if user["password"] == data["password"]:
            valid_password=True
        else:
            valid_password=False
    except Exception as e:
        valid_password=False
    else:
        if valid_password==True:
            user_uuid = create_session(user["username"])
            res = {"uuid": user_uuid, "username": data['username']}
            return Response(json.dumps(res),status=200,mimetype='application/json')
        else:
            return Response("Wrong username or password.",status=400,mimetype='application/json')


# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email 
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή και θα επιστρέφει τα δεδομένα του. 
        Να περάσετε τα δεδομένα του φοιτητή σε ένα dictionary που θα ονομάζεται student.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα.
    """
    # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).

    # Check for the authorization header
    uuid = request.headers.get('authorization')
    
    # If the uuid is valid search for a student using their email and return their registered data
    if is_session_valid(uuid):
        student = students.find_one({"email": data["email"]})
        if student != None:
            student['_id'] = None
            return Response(json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("No student was found with this email",status=400,mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')
    

# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """
    
    uuid = request.headers.get('authorization')
    if is_session_valid(uuid):

        # Calculate the current year minus 30 to find the students that are 30
        current_year = time.strftime("%Y")
        target_year = int(current_year) - 30
        # Save the global variable students to student_dir
        student_dir = globals()["students"]
        output = student_dir.find({"yearOfBirth":{"$eq": target_year}})
        
        if output != None:
            students = []
            for student in output:
                student['_id'] = None
                students.append(student)
        else:
            return Response("No students are 30 years old.",status=500,mimetype='application/json')


        # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχουν φοιτητές που είναι 30 ετών).
        return Response(json.dumps(students), status=200, mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')


# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_thirty_and_over():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών και άνω.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """
    uuid = request.headers.get('authorization')
    if is_session_valid(uuid):

        # Calculate the current year minus 30 to find the students that are older that 30 years old
        current_year = time.strftime("%Y")
        target_year = int(current_year) - 30
        # Save the global variable students to student_dir
        student_dir = globals()["students"]
        student_thirty_and_over = student_dir.find({"yearOfBirth":{"$lte": target_year}})
        
        if student_thirty_and_over != None:
            students = []
            for student in student_thirty_and_over:
                student['_id'] = None
                students.append(student)
        else:
            return Response("No students were found older than 30 years old", status=500, mimetype='application/json')
        # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (υπάρχουν φοιτητές που είναι τουλάχιστον 30 ετών).
        return Response(json.dumps(students), status=200, mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')


# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 
@app.route('/getStudentAddress', methods=['GET'])
def get_student_w_ad():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
        * Στη περίπτωση που ο φοιτητής έχει δηλωμένη τη κατοικία του, θα πρέπει να επιστρέφεται το όνομα του φοιτητή η διεύθυνσή του(street) και ο Ταχυδρομικός Κωδικός (postcode) της διεύθυνσης αυτής.
        * Στη περίπτωη που είτε ο φοιτητής δεν έχει δηλωμένη κατοικία, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους. 
        
        Αν υπάρχει όντως ο φοιτητής με δηλωμένη κατοικία, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
        Το student{} να είναι της μορφής: 
        student = {"name": "Student's name", "street": "The street where the student lives", "postcode": 11111}
    """
    uuid = request.headers.get('authorization') 
    if is_session_valid(uuid):

        if data["email"] != None:
            student = students.find_one({"email": data["email"]})
            if student != None:
                
                if "address" in student:
                    # Parse the requested data that mongodb returned
                    student = {'name': student["name"],
                    'street':student["address"][0]["street"], 
                    'postcode': student["address"][0]["postcode"]
                    }
                else:
                    return Response("The selected student does not have a registered address.",status=400,mimetype='application/json')
            else:
                return Response("No student was found with this email",status=400,mimetype='application/json')
        else:
            return Response("Invalid email",status=500,mimetype='application/json')
        # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητή (υπάρχει ο φοιτητής και έχει δηλωμένη κατοικία).
        return Response(json.dumps(student), status=200, mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')

# ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email 
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
        * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, να διαγράφεται από τη ΒΔ. Να επιστρέφεται μήνυμα επιτυχούς διαγραφής του φοιτητή.
        * Διαφορετικά, να επιστρέφεται μήνυμα λάθους. 
        
        Και στις δύο περιπτώσεις, να δημιουργήσετε μία μεταβλήτη msg (String), η οποία θα περιλαμβάνει το αντίστοιχο μήνυμα.
        Αν βρεθεί ο φοιτητής και διαγραφεί, στο μήνυμα θα πρέπει να δηλώνεται και το όνομά του (πχ: msg = "Morton Fitzgerald was deleted.").
    """
    uuid = request.headers.get('authorization')
    if is_session_valid(uuid):
        if not data["email"]:
            return Response("No email was provided", status=500, mimetype='application/json')
        # Find a student by their email
        student = students.find_one({"email": data["email"]})
        if student == None:
            msg = "No student was found with the email " + data["email"]
            return Response(msg, status=400, mimetype='application/json')
        # If the student exists delete their data from the database
        students.delete_one({"email": data["email"]})
        msg = student["name"] + " was deleted"
        return Response(msg, status=200, mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')

# ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email 
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "courses" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. Στο body του request θα πρέπει δίνεται ένα json της παρακάτω μορφής:
        
        {
            email: "an email",
            courses: [
                {'course 1': 10, 
                {'course 2': 3 }, 
                {'course 3': 8},
                ...
            ]
        } 
        
        Η λίστα courses έχει μία σειρά από dictionary για τα οποία τα key αντιστοιχούν σε τίτλο μαθημάτων και το value στο βαθμό που έχει λάβει ο φοιτητής σε αυτό το μάθημα.
        * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, θα πρέπει να γίνει εισαγωγή των μαθημάτων και των βαθμών τους, σε ένα νέο key του document του φοιτητή που θα ονομάζεται courses. 
        * Το νέο αυτό key θα πρέπει να είναι μία λίστα από dictionary.
        * Αν δε βρεθεί φοιτητής με αυτό το email να επιστρέφεται μήνυμα λάθους. 
    """
    uuid = request.headers.get('authorization')
    if is_session_valid(uuid):

        # Check for the email in the db
        if students.find({"email": data["email"]}).count() == 0:
            return Response("Student with email "+ data["email"] + " was not found",status=500,mimetype='application/json')


        # Update the courses using the $set command of mongodb
        output = students.update({"email": data["email"]}, {"$set":{"courses": data["courses"]}})

        msg = "Student with email "+ data["email"] + " got their subjects and grades set."
        return Response(msg, status=200, mimetype='application/json')
    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')



# ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή.
        * Στη περίπτωση που ο φοιτητής έχει βαθμολογία σε κάποια μαθήματα, θα πρέπει να επιστρέφεται το όνομά του (name) καθώς και τα μαθήματα που έχει πέρασει.
        * Στη περίπτωη που είτε ο φοιτητής δεν περάσει κάποιο μάθημα, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους.
        
        Αν υπάρχει όντως ο φοιτητής με βαθμολογίες σε κάποια μαθήματα, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
        Το dictionary student θα πρέπει να είναι της μορφής: student = {"course name 1": X1, "course name 2": X2, ...}, όπου X1, X2, ... οι βαθμολογίες (integer) των μαθημάτων στα αντίστοιχα μαθήματα.
    """


    uuid = request.headers.get('authorization')
    if is_session_valid(uuid):


        # Check for the email in the db
        student={}
        if students.find({"email": data["email"]}).count() == 0:
            return Response("Student with email "+ data["email"] + "was not found",status=500,mimetype='application/json')

        student_db = students.find_one({"email": data["email"]})

        # Check if the response from the database contains "courses"
        if "courses" not in student_db:
            return Response("Student with email "+ data["email"] + " had no courses registered.",status=500,mimetype='application/json')

        # Iterate through the student's courses returned from the database 
        for course in student_db["courses"]:

            # In each iteration save the course and the grade in a variable
            for course_id, grade in course.items():

                # Check if the grade is >= 5 and if true save the course in the student dictionary
                if grade>=5:
                    student[course_id]=grade

        # If no courses are passed
        if len(student)==0:
            return Response("Student with email "+ data["email"] + " has no passed courses.",status=500,mimetype='application/json')

        return Response(json.dumps(student), status=200, mimetype='application/json')

    else:
        return Response("Session is not valid.",status=401,mimetype='application/json')

# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)