# Πληροφοριακά Συστήματα - 2η υποχρεωτική εργασία 2021

Δημήτριος Λαζαράκης

Στα παραδείγματα ως client χρησιμοποιείται το [httpie](https://httpie.io/). 

# Endpoints
#### `/register`
Ο χρήστης μπόρει να χρησιμοποιήσει το endpoint για να κάνει register έναν απλό user ή έναν administrator. Πρέπει να γίνει ένα POST request και να δωθεί σε μορφή JSON το `email`, το `name` και το `password` του χρήστη. Επιπλέον αν δωθεί και το value `category` ο χρήστης μπορεί να προσδιορίσει τον ρόλο του user/administrator (`user`,`admin`/`administrator`), αλλιώς by default θα γίνει `user`. Εφόσον δεν βρεθεί εγγραφή με το ίδιο email ο νέος χρήστης θα γραφτεί στην `Users` collection.

Example:

`http POST localhost:5000/register  "email"="dim@gmail.com" "password"="password123" "name"="Dimitris" "category"="admin" -j -v`



#### `/login`

Ο χρήστης μπορεί να χρησιμοποιήσει το endpoint για να συνδεθεί με έναν λογαριασμό (user/administrator). Αρκεί να πραγματοποιηθεί ένα POST request με το `email` και το `password` value σε μορφή JSON. Στην περίπτωση που υπάρχει ο συνδιασμός του `email` και `password` στην βάση δεδομένων δημιουργείται ένα `uuid` το οποίο επιστρέφεται στον χρήστη μαζί με το `email` του.

Example:

`http POST localhost:5000/login  "email"="dimam1@gmail.com" "password"="aaabbbccc" -j -v`




#### `/searchProduct`

Ο χρήστης μπορεί να ψάξει για κάποιο συγκεκριμένο προϊόν βάση `name`,`category` ή `_id` παρέχοντας το `authorization` token του. Έπειτα αναλόγα το value που έδωσε ο χρήστης πραγματοποιείται αναζήτηση στο collection products για το συγκεκριμένο προϊόν ή προϊόντα. Τέλος επιστρέφεται σε μορφή json το αποτέλεσμα της αναζήτησης

Example:

`http POST 127.0.0.1:5000/searchProduct name="Cookies" authorization:"d9cefa88-d282-11eb-90c8-0242ac120003"`



#### `/addtoCart`

Ο χρήστης μπορεί να προσθέσει ένα προϊόν στο καλάθι του παρέχοντας το `_id` του και τον αριθμό `stock` που θέλει. Εφόσον ο χρήστης είναι αυθεντικοποιημένος πραγματοποιείται αναζήτηση βάση του `_id` και εφόσον υπάρχει διαθέσιμο `stock` προστίθεται στο καλάθι του χρήστη. Επίσης η τιμή του προϊόντος επί το επιθυμητό `stock` προστίθεται στο `cart`. Τέλος επιστρέφεται μήνυμα επιτυχίας στον χρήστη.

Example:

`http POST 127.0.0.1:5000/addtoCart authorization:"7f7b745c-d28d-11eb-8321-0242ac120003A" _id="60d083a93e6705cec433bbea" stock=1`



#### `/getCart`

Ο χρήστης μπορεί να δει το καλάθι του εφόσον είναι logged in. Επιστρέφονται σε μορφή JSON τα περιεχόμενα του καλαθιού

Example:

`http localhost:5000/getCart  authorization:84a90a48-d116-11eb-8cd4-0242ac120003 -j -v` 


#### `deletefromCart`

Ο χρήστης μπορεί αν διαγράψει κάποιο προϊόν από το καλάθι του χρησιμοποιώντας το value `_id`. Εφόσον το `_id` βρεθεί στο καλάθι διαγράφεται και εμφανίζεται σχετικό μήνυμα επιτυχίας. 

Example:

`http DELETE localhost:5000/deletefromCart authorization:7f7b745c-d28d-11eb-8321-0242ac120003 _id="7f7b745c-d28d-11eb-8321-0242ac120003"`


#### `/checkout`

Ο χρήστης μπορεί να κάνει checkout παρέχοντας την κάρτα του (16 ψηφία) με το value `card`. Εφόσον είναι authenticated το checkout πραγματοποίεται και για κάθε αντικείμενο στο καλάθι αφαιρείται το `stock` από τη βάση δεδομένων. Tέλος εμφανίζεται η τιμή συνολική των προϊόντων του καλαθιού.

Example:

`http POST 127.0.0.1:5000/checkout authorization:"afd16e0e-d29c-11eb-b5be-0242ac120003" card="1234567890987656"`


#### `/deleteAccount`

Ο χρήστης μπορεί να διαγράψει τον λογαριασμό του εφόσον είναι authenticated και παρέχει το `authorization` token. Η εγγραφή του χρήστη θα διαγραφή από τη βάση δεδομένων βάση `email` και το authentication token (`uuid`) του θα γίνει invalid. Επιστρέφεται μήνυμα επιτυχίας.

Example:

`http POST 127.0.0.1:5000/deleteAccount authorization:"a62e30f6-d11d-11eb-8775-0242ac120003"`



#### `/addProduct`

Ο χρήστης μπορεί να προσθέσει προϊόντα στη βάση δεδομένων εφόσον είναι διαχειριστής παρέχοντας τα δεδομένα `name`, `price`, `stock`, `category` και `description`. Δημιουργείται ένα νέο dictionary που περιέχει τα στοιχεία του προϊόντος και προστίθεται στη βάση δεδομένων.

Example:

`http POST 127.0.0.1:5000/addProduct name="Cookies" "price"=2 description="Chocolate cookies" category="biscuits" stock=20 authorization:"bea540ce-d074-11eb-9dd6-0242ac120003"`


#### `/deleteProduct`

Ο χρήστης μπορεί να διαγράψει ένα προϊόν από τη βάση δεδομένων χρησιμοποιώντας το συγκεκριμένο endpoint. Εφόσον ο χρήστης είναι administrator και παρέχοντας το `_id`, πραγματοποιείται αναζήτηση βάση `_id` και διαγράφεται το συγκεκριμένο προϊόν.

Example:

`http DELETE localhost:5000/deletefromCart authorization:070aa052-d291-11eb-ad42-0242ac120003 _id="60d083a93e6705cec433bbea"`


#### `/updateProduct`

Ο χρήστης μπορεί να παρέχει ένα `_id` και να αλλάξει το `name`, `price` και το `description`. Για κάθε πεδίο που παρέχεται από τον χρήστη μεταβάλλεται η τιμή του. Τέλος εμφανίζεται μήνυμα επιτυχίας. 

Εxample:

`http PUT localhost:5000/updateProduct _id="60d07668ae94a3b0dc5aefd4" name="Cookie 2" price=5 description="Biscuit product" stock=25 authorization:ec4e870e-d2a1-11eb-b7a0-0242ac120003`

