**BUCKETLIST API**
----
<p>According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before, but wants to do before dying. This Bucket List API allows a user to create an account and sign in, perform CRUD operations on the bucketlists, and perform CRUD operations on items attached to these bucketlists.
</p>
----

**Register User**
----
  Adds a user using their email and password.

* **URL**

  /api/version:/auth/register

* **Method:**

  `POST`

*  **URL Params**

    **Required:**

    `version=[string]`

* **Data Params**

    **Required:**

    `email=[string]`<br />
    `password=[string]`<br />

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{ "message" : "You registered successfully. Login." }`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />

  * **Content:** {'message': 'Please enter an email'}

  OR

  * **Content:** {'message': 'Use the correct email format'}

  OR

  * **Content:** {'message': 'User already exists. Login.'}

  OR

  * **Content:** {'message': 'The length of the password should be at least six characters'}



  * **Code:** 409 Conflict <br />

  * **Content:** {'message': 'User already exists. Login.'}

* **Sample Call:**

  ```python
  auth = {'email': 'abcd@abcd.com', 'password': 'abcdabcd'}
  post("/api/v1/auth/register", data=auth)
  ```

----

**Login User**
----
  Returns authentication token.

* **URL**

  /api/version:/auth/login

* **Method:**

  `POST`

*  **URL Params**

    **Required:**

    `version=[string]`

* **Data Params**

    **Required:**

    `email=[string]`<br />
    `password=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{'message': "You logged in successfully.", 'access_token' : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTg1NjkwNTUsImlhdCI6MTQ5ODU1NDY1NSwic3ViIjoyfQ.pk8-FR4uveWerDj5ZCW7UQKTrRLPA2k4wIgM5zJ7xAc" }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Content:** {'message': 'Invalid email or password, Please try again.'}

* **Sample Call:**

  ```python
  auth = {'email': 'abcd@abcd.com', 'password': 'abcdabcd'}
  post("/api/v1/auth/login", data=auth)
  ```

----

**Get bucketlists**
----
  Returns all bucketlists.

* **URL**

  /api/version:/bucketlists/

* **Method:**

  `GET`

*  **URL Params**

    **Required:**

    `version=[string]`

    **Optional:**

    `q=[string]`<br />
    `limit=[integer]`<br />
    `page=[integer]`<br />

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    `{ `<br />
    &nbsp;&nbsp;`"bucketlists": [  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`{` <br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"created_by": 2,  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Wed, 14 Jun 2017 17:46:48 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Thu, 15 Jun 2017 06:59:04 GMT",`  <br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"id": 3,  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"items": [],`  <br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"name": "kkk"  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`},  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`{  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"created_by": 2,  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Thu, 15 Jun 2017 07:33:09 GMT",`<br />  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Thu, 15 Jun 2017 07:33:09 GMT",  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"id": 14,  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"items": [],  `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"name": "kkkk" `<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`},  `<br />
    &nbsp;&nbsp;`],  `<br />
    &nbsp;&nbsp;`"next_page": "/api/v1/bucketlists/?q=buck&limit=2&offset=2", `<br />
    &nbsp;&nbsp;`"previous_page": ""  `<br />
    `}`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  * **Content:** {"message": "Invalid Token"}

* **Sample Call:**

  ```python
  header = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'}
  get("/api/v1/bucketlists/", headers=header)
  ```

----

**Get bucketlist**
----
  Returns one bucketlist.

* **URL**

  /api/version:/bucketlists/id:

* **Method:**

  `GET`

*  **URL Params**

    **Required:**

    `version=[string]`<br />
    `id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    `{`<br />
    &nbsp;&nbsp;` "bucketlist": {`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"created_by": 2,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Thu, 15 Jun 2017 07:36:33 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Thu, 15 Jun 2017 07:36:33 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"id": 14,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"items": [`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{`
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "bucketlist_id": 14`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "date_created": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "date_modified": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "done": false,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "id": 32,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`  "name": "gff"`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`]`<br />
    &nbsp;&nbsp;`}`<br />
    `}`<br />


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />

  OR

  * **Code:** 401 UNAUTHORIZED <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  get("/api/v1/bucketlists/14", headers=header)
  ```

----

**Add bucketlist**
----
  Adds a bucketlist and returns it.

* **URL**

  /api/version:/bucketlists/

* **Method:**

  `POST`

*  **URL Params**

    `version=[string]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    `{`<br />
    &nbsp;&nbsp;` "bucketlist": {`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"created_by": 2,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"id": 20,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"items": [],`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"name": "head phones"`<br />
    &nbsp;&nbsp;` }`<br />
    `}`<br />

* **Error Response:**

  * **Code:** 409 Conflict <br />

  * **Content:** {"message": "Bucketlist name already exists!"}

  OR

  * **Code:** 400 Bad Request <br />

  * **Content:** {"message": "Name missing!"}

  OR

  * **Code:** 400 Bad Request <br />

  * **Content:** {"message": "Please input name!"}

  

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  bucket = {'name': 'head phones'}
  post("/api/v1/bucketlists/", data=bucket, headers=header)
  ```

----

**Update bucketlist**
----
  Edits bucketlist and returns the bucketlist.

* **URL**

  /api/version:/bucketlists/id:

* **Method:**

  `PUT`

*  **URL Params**

    `version=[string]`<br />
    `id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 201 <br />
  **Content:** <br />
    `{`<br />
    &nbsp;&nbsp;` "bucketlist": {`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"created_by": 2,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Tue, 27 Jun 2017 12:19:57 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"id": 20,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"items": [],`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"name": "ear phones"`<br />
    &nbsp;&nbsp;` }`<br />
    `}`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  bucket = {'name': 'ear phones'}
  put("/api/v1/bucketlists/14", data=bucket, headers=header)
  ```

----

**Delete bucketlist**
----
  Deletes a bucketlist and returns True.

* **URL**

  /api/version:/bucketlists/id:

* **Method:**

  `DELETE`

*  **URL Params**

    `version=[string]`<br />
    `id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 'message': "bucketlist <int:id> deleted" }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  delete("/api/v1/bucketlists/14", headers=header)
  ```

----

**Add bucketlist item**
----
  Adds a bucketlist item and returns it.

* **URL**

  /api/version:/bucketlists/id:/items/

* **Method:**

  `POST`

*  **URL Params**

    `version=[string]`<br />
    `id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    `{`<br />
    &nbsp;&nbsp;` "item": {`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"bucketlist_id": 2,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"done": false,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"id": 5,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"name": "pan cake"`<br />
    &nbsp;&nbsp;` }`<br />
    `}`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  item = {'name': 'pan cake'}
  post("/api/v1/bucketlists/2/items/", data=item, headers=header)
  ```

----

**Update bucketlist item**
----
  Updates a bucketlist item and returns it.

* **URL**

  /api/version:/bucketlists/id:/items/item_id:

* **Method:**

  `PUT`

*  **URL Params**

    `version=[string]`<br />
    `id=[integer]`<br />
    `item_id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    `{`<br />
    &nbsp;&nbsp;` "item": {`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_created": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"date_modified": "Sun, 05 Mar 2017 10:17:37 GMT",`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"done": false,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"id": 5,`<br />
    &nbsp;&nbsp;&nbsp;&nbsp;`"name": "cup cake"`<br />
    &nbsp;&nbsp;` }`<br />
    `}`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  item = {'name': 'cup cake', 'done': True}
  put("/api/v1/bucketlists/2/items/5", data=item, headers=header)
  ```

----

**Delete bucketlist item**
----
  Deletes a bucketlist item and returns True.

* **URL**

  /api/version:/bucketlists/id:/items/item_id:

* **Method:**

  `DELETE`

*  **URL Params**

    `version=[string]`<br />
    `id=[integer]`<br />
    `item_id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 'message': Item <item_id> deleted }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  delete("/api/v1/bucketlists/2/items/5", headers=header)
  ```