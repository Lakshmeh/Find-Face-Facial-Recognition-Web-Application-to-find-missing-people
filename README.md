# Find-Face-Facial-Recognition-Web-Application-to-find-missing-people
About the Project:
Children and senior citizens are the most susceptible to getting lost in public places and lose contact with their family members. 
**Find Face** is a Web Application which uses Face Recognition Technology to find missing people. It is a cross-platform for the missing people and their family. This web application is user-friendly and provides additional resources and helpline websites to users. As of now, Find Face has not been deployed yet, but will be soon.

![Logo](https://github.com/Lakshmeh/Find-Face-Facial-Recognition-Web-Application-to-find-missing-people/blob/main/static/img/findfaceicon.png)



This is made specially for children and senior citizens who are more vulnerable to such situations
## Features of this Web App
- Contact the missing person's family using the power of facial recognition
- Report a missing person with their images and most recent location regarding their whereabouts
- Report a recovered person with their images and most recent location regarding their whereabouts



## Tech Stacks I used

**Client:** HTML, CSS, Javascript

**Server:** Flask, MongoDB cloud database


## Packages and modules used 
(also included in the runnable requirements.txt file)

- face_recognition
- Flask
- Open CV
- Numpy
- pymongo for python
- uuid (to generate unique ids)
- dnspython 



## Get started on your local system
To get started with the testing process of this web application, it is required to implement the following steps:

**Step 1: Clone the project**

```bash
  git clone https://github.com/Lakshmeh/Find-Face-Facial-Recognition-Web-Application-to-find-missing-people
```

**Step 2: Install dependencies** (just requirements.txt file)

```bash
  pip install -r requirements.txt
  pip install dnspython
```

**Step 3: Run code.py file as follows**

```bash
  FLASK_APP = code.py flask run
```
or 
```bash
  venv FLASK_APP = code.py python -m flask run
```  
or 
```bash
  python3 code.py
```  

**Step 4: Hit (http://127.0.0.1:5000/) on any browser to see the web application working on your local system.**

 ## Future Scope
 I plan on including the following -
 - Real time webcam frame capture using opencv to store image data.
 - Provide the option for storing data of the same missing person again and again and provide the most recent information of the missing person
 - Make face recognition possible from large distances
 - Other functionalities to improve user experience
