from flask import Flask, render_template, Response, redirect, url_for, session, request, jsonify
# from flask_mysqldb import MySQL
from flask_cors import CORS
import cv2
import detector

# from detector module
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import time


app=Flask(__name__)
cors = CORS(app)
app.secret_key = 'my-secret-key'

# MYSQL Configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'Drows_detectDB'

# db = MySQL(app)


################################### Login/signup section ##################################
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False)
#     password_hash = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(50), nullable=False)

# @app.route('/api/user', methods=['POST'])
# def create_user():
#     data = request.json
#     new_user = User(username=data['username'], email=data['email'], password_hash=data['password'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify(message='User created successfully'), 201

################################## Login/signup section ##################################

camera_on = False
eye_closure_timestamps = []
drowsiness_level = "None"

def generate_frames():
    global camera_on, eye_closure_timestamps
    camera = cv2.VideoCapture(0)
    thresh = 0.25
    frame_check = 20
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

    flag=0
    while camera_on and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            for subject in subjects:
                shape = predict(gray, subject)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = detector.eye_aspect_ratio(leftEye)
                rightEAR = detector.eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag += 1
                    # print (flag)
                    current_time = time.time()
                    print(current_time)
                    eye_closure_timestamps.append(current_time)
                    eye_closure_timestamps = [t for t in eye_closure_timestamps if current_time - t <= 60]
                    print(eye_closure_timestamps)
                    if flag >= frame_check:
                        cv2.putText(frame, "****************ALERT!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "****************ALERT!****************", (10,325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        mixer.music.play()
                else:
                    flag = 0
                    mixer.music.pause()
            # cv2.imshow("Frame", frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # camera.release()
    
    update_drowsiness_level()

def update_drowsiness_level():
    global drowsiness_level, eye_closure_timestamps
    count = len(eye_closure_timestamps)
    if count >= 25:
        drowsiness_level = "Critical"
    elif count >= 15:
        drowsiness_level = "Major"
    elif count >= 5:
        drowsiness_level = "Low"
    else:
        drowsiness_level = "None"


@app.route('/drowsiness_level')
def get_drowsiness_level():
    global drowsiness_level
    return jsonify(level=drowsiness_level)

@app.route('/control_camera', methods=['POST'])
def control_camera():
    global camera_on
    if request.json and 'state' in request.json:
        state = request.json['state']
        camera_on = state == 'start'
        return jsonify({"success": True, "state": camera_on})
    return jsonify({"success": False})

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')


@app.route('/video')
def video():
    if camera_on:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response("Camera off", status=204)
if __name__=='__main__':
    app.run(debug=True)