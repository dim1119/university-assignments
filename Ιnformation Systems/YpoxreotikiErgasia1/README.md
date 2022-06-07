# Πληροφοριακά Συστήματα - 1η υποχρεωτική εργασία 2021
Δημήτριος Λαζαράκης

### Xρησιμοποιήθηκε:
- Python 3.5.3
- Flask 1.1.2
- pymongo 3.11.3

## Ερώτημα 1ο
```python
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
    # Search for the specific username if none found, insert the new username and password in the database
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
```
Στο endpoint */createUser* ο χρήστης πρέπει να στείλει ένα POST request που να περιέχει ενα username και password ώστε να κάνει register. Θα υπάρξει ένα query στην mongodb που θα αναζητά εγγραφές με το ίδιο username και μετά θα τις καταμετρήσει. Εφόσον δεν βρεθεί κάποιος χρήστης με το συγκεκριμένο username, θα δημιουργηθεί ένα νέο dictionary που θα περιέχει το username και password του χρήσητη, το οποίο θα εγγραφεί στο collection `Users` της database και θα επιστραφεί μήνυμα επιτυχίας (status 200). Σε περίπτωση που υπάρχει ήδη αυτό το email στο collection `Users` θα επιστραφεί μήνυμα λάθος (status 400), ενώ σε περίπτωση που δεν δώσει τα απαραίτητα στοιχεία στο POST request επιστρεφεται error (status 500).

- Example request:
`curl -X POST -H "Content-Type: application/json" -d @create_user.json http://localhost:5000/createUser`
- Response:
`dim123 was added to the MongoDB`


## Ερώτημα 2ο
```python
@app.route('/login', methods=['POST'])
def login()
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
```
Στο endpoint */login* ο χρήστης πρέπει να στείλει ένα POST request με το username και το password του σε μορφή JSON ώστε να αυθεντικοποιηθεί. Εφόσον ο χρήστης στείλει τα δεδομένα που απαιτούνται πραγματοποιείται μία αναζήτηση στο collection `Users` για το συγκεκριμένο username και αποθηκεύονται τα δεδομένα που επιστρέφει η βάση αποθηκεύονται στη μεταβλητή user. Πρέπει να ελέγξουμε αν υπάρχουν στη βάση δεδομένων o συγκεκριμένος συνδιασμός username/password. Ο έλεγχος αυτό γίνεται με τη χρήση ενός try/except block και μιας flag μεταβλητής (`valid_password`). Πραγματοποιείται έλεγχος του password του χρήστη από το POST σε σχέση με αυτό από τη database και σε περίπτωση που ο έλεγχος είναι επιτυχής η μεταβλητή `valid_password` θα γίνει True. Σε κάθε άλλη περίπτωση η μεταβλητή θα γίνει False καθώς και θα γίνει parse τo exception σε περίπτωση που δεν υπάρχει το username ή το password. Σε περίπτωση που η `valid_password` είναι True καλείται η `create_session()` για το συγκεκριμένο username, επιστρέφοντας ένα uuid για το συγκεκριμένο χρήστη. Το uuid αυτό μαζί με το username του χρήση επιστρέφονται σε JSON μορφή (status 200). Αντιθέτως αν η `valid_password` είναι False  ή τα δεδομένα που έδωσε ο χρήστης είναι σε λάθος μορφή επιστρέφεται μήνυμα λάθους (status 400 και status 500 αντίστοιχα).

- Example request:
`curl -X POST -H "Content-Type: application/json" -d @create_user.json http://localhost:5000/login` όπου το αρχείο `create_user.json` περιέχει: 
```json
{
    "username": "dim123",
    "password": "345"
}
```
- Response:
`{"username": "dim123", "uuid": "1a4c8226-b558-11eb-870f-00155d3e4c1b"}`

## Ερώτημα 3ο
```python
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
```

Στο endpoint */getStudent* ο χρήστης πρέπει να στείλει ένα GET request με το email του μαθητή σε μορφή JSON και το uuid του στο request header `Authorization`. Εφόσον τα JSON δεδομένα είναι λανθασμένα επιστρέφεται error (status 500). Αρχικά πραγματοποιείται ένας έλεγχος για το αν το uuid αυτό είναι valid. Σε περίπτωση που ο χρήστης δώσει invalid uuid επιστρέφεται μήνυμα λάθους (status 400). Εφόσον του uuid του είναι valid πραγματοποιείται αναζήτηση για το συγκεκριμένο email στο database με την χρήση της συνάρτησης `find_one()`. Αν βρεθεί ο μαθητής στην database, το πεδίο `_id` γίνεται None και επιστρέφονται όλα τα δεδομένα του σε μορφή json (status 200). Αν δεν βρεθεί ο μαθητής επίστρεφεται μήνυμα λάθους (status 400).

- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" http://localhost:5000/getStudent -d '{"email":"lilyengland@ontagene.com"}' -H "Content-Type: application/json" -X GET`
- Response:
`{"yearOfBirth": 1995, "email": "lilyengland@ontagene.com", "address": [{"city": "Rockhill", "street": "Hendrickson Street", "postcode": 18631}], "name": "Lily England", "_id": null}`

## Ερώτημα 4ο
```python
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
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
```
Στο endpoint */getStudents/thirties* ο χρήστης πρέπει να στείλει ένα GET request με το uuid του στο request header `Authorization`. Εφόσον το uuid του είναι valid (αλλιώς επιστρέφεται error - status 401) η συνάρτηση `strftime()` παίρνει τον τωρινό χρόνο του συστήματος και αφαιρεί τον αριθμό 30 με σκοπό να βρεθεί η ημερομηνία γέννησης των ατόμων που είναι 30 χρονών. Καθώς θέλουμε η λίστα που θα επιστρέψουμε να ονομάζεται `students` (local variable) και καλούμε το object της pymongo `students` (global variable) αποθήκευσα την global μεταβλητή στο `student_dir`. Κάνοντας ένα query για το συγκεκριμένο `yearOfBirth` στην database με την χρήση της `find()` επιστρέφονται τα στοιχεία των φοιτητών που είναι 30 χρονών. Σε περίπτωση που δεν επιστραφεί κάποιο άτομο επιστρέφεται μήνυμα λάθους (status 500). Για κάθε student που επιστρέφεται, τα στοιχεία του/της γίνονται `append()` σε μια λίστα και το πεδίο `_id` γίνεται None. Tέλος επιστρέφεται η λίστα με τα στοιχεία των μαθητών σε μορφή JSON (status 200).

- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" http://localhost:5000/getStudents/thirties -X GET`
- Response:
`[{"yearOfBirth": 1991, "email": "browningrasmussen@ontagene.com", "address": [{"city": "Cuylerville", "street": "Doone Court", "postcode": 17331}], "name": "Browning Rasmussen", "_id": null}, {"gender": "male", "yearOfBirth": 1991, "email": "bennettbaker@ontagene.com", "name": "Bennett Baker", "_id": null}]`

## Ερώτημα 5ο
```python
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_thirty_and_over():
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
```
Στο endpoint */getStudents/oldies* ο χρήστης πρέπει να στείλει ένα GET request με το uuid του στο request header `Authorization`. Εφόσον το uuid του είναι valid (αλλιώς επιστρέφεται error - status 401) η συνάρτηση `strftime()` παίρνει τον τωρινό χρόνο του συστήματος και αφαιρεί τον αριθμό 30 με σκοπό να βρεθεί η ημερομηνία γέννησης των ατόμων που είναι 30 χρονών ή περισσότερο. Καθώς θέλουμε η λίστα που θα επιστρέψουμε να ονομάζεται `students` (local variable) και καλούμε το object της pymongo `students` (global variable) αποθήκευσα την global μεταβλητή στο `student_dir`. Κάνοντας ένα query για το συγκεκριμένο `yearOfBirth` στην database με την χρήση της `find()` επιστρέφονται τα στοιχεία των φοιτητών που είναι 30 χρονών ή παραπάνω. Σε περίπτωση που δεν επιστραφεί κάποιο άτομο επιστρέφεται μήνυμα λάθους (status 500). Για κάθε student που επιστρέφεται, τα στοιχεία του/της γίνονται `append()` σε μια λίστα και το πεδίο `_id` γίνεται None. Tέλος επιστρέφεται η λίστα με τα στοιχεία των μαθητών σε μορφή JSON (status 200).

- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" http://localhost:5000/getStudents/oldies -X GET`
- Response:
```
[{"yearOfBirth": 1979, "email": "patriciapatterson@ontagene.com", "address": [{"city": "Bodega", "street": "Lawn Court", "postcode": 16678}], "name": "Patricia Patterson", "_id": null}, {"yearOfBirth": 1979, "email": "gardnerjimenez@ontagene.com", "address": [{"city": "Leeper", "street": "Montauk Avenue", "postcode": 12465}], "name": "Gardner Jimenez", "_id": null}, {"yearOfBirth": 1965, "email": "herreraware@ontagene.com", "address": [{"city": "Ypsilanti", "street": "Portal Street", "postcode": 18622}], "name": "Herrera Ware", "_id": null}, 
.
.
.
{"yearOfBirth": 1990, "email": "testname@ontagene.com", "address": [{"city": [{"city": "Nanafalia", "postcode": 15243, "street": "Calder Place"}], "postcode": [{"city": "Nanafalia", "postcode": 15243, "street": "Calder Place"}], "street": "Calder Place"}], "name": "Test Name", "_id": null}, {"yearOfBirth": 1990, "email": "testname@ontagene.com", "address": [{"city": "Nanafalia", "postcode": "Nanafalia", "street": "Calder Place"}], "name": "Test Name", "_id": null}, {"name": "Test Name", "email": "testname@ontagene.com", "address": [{"city": "Nanafalia", "postcode": 15243, "street": "Calder Place"}], "yearOfBirth": 1990, "_id": null}, {"gender": "female", "yearOfBirth": 1982, "email": "gracierosales@ontagene.com", "name": "Gracie Rosales", "_id": null}]
```

## Ερώτημα 6ο
```python
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
```
Στο endpoint */getStudentAddress* ο χρήστης πρέπει να στείλει ένα GET request με το email του μαθητή σε μορφή JSON και το uuid του στο request header `Authorization`. Εφόσον τα data που στέλνει ο χρήστης είναι valid και περιέχουν email (αλλιώς επιστρέφεται μήνυμα λάθους - status 500) και το uuid του είναι valid (αλλιώς επιστρέφεται error - status 401) πραγματοποιείται αναζήτηση στη βάση δεδομένων για μαθητή με το συγκεκριμένο email χρησιμοποιώντας την συνάρτηση `find_one()`. Εφόσον βρεθεί (αλλιώς επιστρέφεται error - status 400) και έχει διεύθυνση αποθηκευμένη (αλλιώς επιστρέφεται error - status 400) δημιουργείται ένα νέο dictionary `student` που περιέχει τα keys `name`, `street`, `postcode`. Τα keys αυτα παίρνουν τα δεδομένα από τα πεδία του response της βάσης δεδομένων. Τέλος επιστρέφεται το dictionary `student` σε μορφή JSON στον χρήστη (status 200).


- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" http://localhost:5000/getStudentAddress -d '{"email":"lilyengland@ontagene.com"}' -H "Content-Type: application/json" -X GET`
- Response:
`{"street": "Hendrickson Street", "name": "Lily England", "postcode": 18631}`

## Ερώτημα 7ο
```python
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
```
Στο endpoint */deleteStudent* ο χρήστης πρέπει να στείλει ένα DELETE request με το email του μαθητή σε μορφή JSON και το uuid του στο request header `Authorization`. Εφόσον τα data που στέλνει ο χρήστης είναι valid και περιέχουν email (αλλιώς επιστρέφεται μήνυμα λάθους - status 500) και το uuid του είναι valid (αλλιώς επιστρέφεται error - status 401) γίνεται έλεγχος για το αν το πεδίο email που έστειλε ο χρήστης είναι κενό (status 500), αλλιώς πραγματοποιείται αναζήτησ για το συγκεκριμένο email στους students με την χρήση της συνάρτησης `find_one()`. Εφόσον βρεθεί ο μαθητής (σε άλλη περίπτωση επιστρέφεται μήνυμα λάθους - status 400) πραγματοποιείται διαγραφή με την χρήση της συνάρτησης `delete_one()` βάση email και επιστρέφεται μήνυμα ότι η διαγραφή ήταν επιτυχής μαζί με το όνομα του (status 200).

- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b"  http://localhost:5000/deleteStudent -d '{"email":"lilyengland@ontagene.com"}' -H "Content-Type: application/json" -X DELETE`
- Response:
`Lily England was deleted`

## Ερώτημα 8ο
```python
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

```
Στο endpoint */addCourses* ο χρήστης πρέπει να στείλει ένα PATCH request με το email του μαθητή σε μορφή JSON και το uuid του στο request header `Authorization`. Εφόσον τα data που στέλνει ο χρήστης περιέχει email (αλλιώς επιστρέφεται μήνυμα λάθους - status 500) και το uuid του είναι valid (αλλιώς επιστρέφεται error - status 401) πραγμοτοποιείται καταμέτρηση των εγγραφών στο collections `Students` με το email που έδωσε ο χρήστης. Εφόσον οι εγγραφές είναι 0 επιστρέφεται μήνυμα λάθους με το email του φοιτητή (status 500). Αν υπάρχει φοιτητής με το συγκεκριμένο email καλείται η συνάρτηση `update()` η οποία, βάση του πεδιού `email` αναζητά, με την εντολή `$set` γράφει τα μαθημάτα του μαθητή στη database. Τέλος, επιστρέφεται μήνυμα επιτυχίας μαζί με το email του φοιτητή (status 200).

- Example request:
`curl -X PATCH -H "Content-Type: application/json" -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" -d @upload_courses.json http://localhost:5000/addCourses`, όπου το αρχείο `upload_courses.json` περιέχει:
```json
{
            "email": "maryellendalton@ontagene.com",
            "courses": [
                {"course 1": 10}, 
                {"course 2": 5 }, 
                {"course 3": 8},
                {"course 5": 4}
            ]
        } 
```
- Response:
`Student with email maryellendalton@ontagene.com got their subjects and grades set.`

## Ερώτημα 9ο
```python
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
```

Στο endpoint */getPassedCourses* ο χρήστης πρέπει να στείλει ένα GET request με το email του μαθητή σε μορφή JSON και το uuid του στο request header `Authorization`. Εφόσον τα δεδομένα που στέλνει είναι σωστά (αλλιώς επιστρέφεται error - status 500 και 401 αντίστοιχα) δημιουργείται ένα dictionary `student` και μετά γίνεται έλεγχος για το αν υπάρχει μαθητής με το συγκεκριμένο email μέσω των συναρτήσεων `find()` και `count()` και αν δεν βρεθεί κάποιος μαθητής επιστρέφεται error - status 500. Έπειτα με την χρήση της `find_one()` λαμβάνουμε τα δεδομένα του συγκεκριμένου student. Εφόσον δεν έχει μαθήματα  εγγεγραμμένα επιστρέφεται error - status 500. Έπειτα για κάθε μάθημα που έχει γραμμένο ο student αποθηκεύεται το όνομα του μαθήματος και ο βαθμός σε μεταβλητές. Για κάθε συνδιασμό `course_id`,`grade` ελέγχεται αν ο βαθμός είναι μεγαλύτερος-ίσος του 5 και αν είναι αποθηκεύεται ο βαθμός `grade` στο dictionary `student` με key το `course_id`. Τέλος ελέγχεται αν ο μαθητής έχει περασμένα μάθήματα, μέσω του `len()` του `student`, και αν είναι 0 επιστρέφεται ότι δεν έχει κάποιο περασμένο μάθημα μαζί με το email του/της (status 500). Σε άλλη περίπτωση επιστρέφεται το dictionary `student` σε μορφή JSON (status 200).

- Example request:
`curl -H "Authorization: 1a4c8226-b558-11eb-870f-00155d3e4c1b" http://localhost:5000/getPassedCourses -d '{"email":"maryellendalton@ontagene.com"}' -H "Content-Type: application/json" -X GET`
- Response:
`{"course 1": 10, "course 2": 5, "course 3": 8}`