from flask import Flask, render_template, url_for, redirect, Response , jsonify, request
import cv2 as cv
import numpy as np
import face_recognition
import pymongo
from pymongo import MongoClient
from bson import json_util
import uuid
import dns


app = Flask(__name__)

cluster = MongoClient("mongodb+srv://Laksh:Laksh02@cluster0.uzz3c.mongodb.net/?retryWrites=true&w=majority")
db = cluster["FindFace"]
collection = db["Faces"]

        
@app.route('/')

def home():
    return render_template('index.html')


@app.route('/i-lost-someone')

def inform():
    return render_template('face_recog.html')


# Importing the images from my directory
laksh_image = face_recognition.load_image_file("/Users/lakshmi/Desktop/lakshmi/laksh.jpg")
laksh_face_encoding = face_recognition.face_encodings(laksh_image)[0]

mom_image = face_recognition.load_image_file("/Users/lakshmi/Desktop/lakshmi/mom.jpg")
mom_face_encoding = face_recognition.face_encodings(mom_image)[0]

#Create arrays of known face encodings and their names
known_face_encodings = [
    laksh_face_encoding,
    mom_face_encoding
]
known_face_names = [
    "Lakshmi Priya",
    "Bhuvana"
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
name = "Unknown"
process_this_frame = True

# this function generates frames once the webcam is on
def generate_frames():
    camera=cv.VideoCapture(0)
    while True:
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
       # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    global name
                    name = known_face_names[best_match_index]

                face_names.append(name)
                
                
                
            # Display the name of person if recognised
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv.rectangle(frame, (left, top), (right, bottom), (164, 111, 99), 2)

                # Draw a label with a name below the face
                if (name!="Unknown"):
                    cv.rectangle(frame, (left, bottom - 35), (right, bottom), (164, 111, 99), cv.FILLED)
                    font = cv.FONT_HERSHEY_DUPLEX
                    cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
                ret,buffer=cv.imencode('.jpg',frame)
        
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(np.array(buffer)) + b'\r\n')  

@app.route('/lostfacevideo')

def lostfacevideo():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame') 

# if the missing person has been recognised, the web app will display the most recent information regarding the whereabouts of the missing person
@app.route('/i-lost-someone/person-found') 

def person_found():
    details= collection.find_one({"Name":name})
    for detail in details:
        Name = details["Name"]
        age = details["Age"]
        location_last_found = details["Location last found"]
        contact = details["Contact of the person who reported"]
        
        return render_template('person_found.html', Name = name , age=age, location_last_found= location_last_found, contact= contact)
    
# requesting data from the user after the form is filled
class User:
    def report(self):
        user={
            "_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "age": request.form['age'],
            "Location": request.form['Location'],
            "contact": request.form['contact'],
            "fileToUpload" : request.form['fileToUpload']
            }
        collection.insert_one(user)
        
        return jsonify(user) 
    
    
@app.route('/i-lost-someone/report', methods=['GET', 'POST'])

def informlost():
    return render_template('informlost.html')  #asks the user to fill a form which includes details of the missing person 

@app.route('/i-lost-someone/reportedlostperson', methods=['GET','POST'])

def thankyouu():
    User().report()
    return "Thankyou for reporting the missing person. We will get back to you soon!"


# report if someone recovered a missing person
@app.route('/i-found-someone', methods=['GET','POST'])

def informfound():
    return render_template('informfound.html')

@app.route('/reportedperson', methods=['GET','POST'])

def thankyou():
    User().report()
    return "Thankyou for reporting the recovered person. We will get back to you soon!"



if __name__ == '__main__':
    app.run()
    
   
    
    
