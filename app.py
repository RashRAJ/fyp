from flask import Flask, render_template, Response, redirect, url_for, session, request, jsonify, g
from flask_mysqldb import MySQL
from flask_cors import CORS
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import cv2
import detector

# from detector module
from imutils import face_utils
from datetime import date, timedelta, datetime
from pygame import mixer
import imutils
import dlib
import time


app=Flask(__name__)
cors = CORS(app)
app.secret_key = '6d7311d50a781c48949e47b8cb1958493b8693bdd4ce3b234cf7adb858ae625f'

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ -DB SECTION- @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ddot:U5ruZqQG-2q29w-s@localhost/Drows_detectDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6d7311d50a781c48949e47b8cb1958493b8693bdd4ce3b234cf7adb858ae625f'
db = SQLAlchemy(app)


################################### Login/signup section ##################################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def generate_token(self):
        # Define payload with user ID and expiration time
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time (e.g., 1 day)
        }
        # Generate JWT token with payload and secret key
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token  

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to verify password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class RideHistory(db.Model):
    __tablename__ = 'RideHistory'
    id = db.Column(db.Integer, primary_key=True)
    ride_date = db.Column(db.Date, nullable=False)
    ride_duration = db.Column(db.Time, nullable=False)  # Change the column type to TIME
    # alertness_level = db.Column(db.Integer, nullable=False)
    drowsiness_level = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='ride_histories')

    def __repr__(self):
        return f"RideHistory(ride_date='{self.ride_date}', ride_duration='{self.ride_duration}', " \
               f"alertness_level='{self.alertness_level}', drowsiness_level='{self.drowsiness_level}')"
################################## RIDE HISTORY section ##################################

ride_date = date.today()
camera_on = False
start_time = None 
eye_closure_timestamps = []
drowsiness_level = "None"
user_id = ""

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
    eyes_closed = False 
    closure_start_time = None
    last_update_time = None
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
                    if not eyes_closed:
                        eyes_closed = True
                        closure_start_time = time.time()
                    # print (flag)
                    # current_time = time.time()
                    # print(current_time)
                    # eye_closure_timestamps.append(current_time)
                    # eye_closure_timestamps = [t for t in eye_closure_timestamps if current_time - t <= 60]
                    # print(eye_closure_timestamps)
                    if flag >= frame_check:
                        cv2.putText(frame, "****************ALERT!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "****************ALERT!****************", (10,325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        mixer.music.play()
                else:
                    flag = 0
                    mixer.music.pause()
                    if eyes_closed:
                        if closure_start_time is not None:
                            duration = time.time() - closure_start_time
                            if duration >= 1.0:  
                                current_time = int(closure_start_time)
                                if current_time != last_update_time:
                                    eye_closure_timestamps.append(current_time)
                                    last_update_time = current_time
                        eyes_closed = False
            # cv2.imshow("Frame", frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # camera.release()
    
    current_time = time.time()
    eye_closure_timestamps = [t for t in eye_closure_timestamps if current_time - t <= 60]
    print(eye_closure_timestamps)

    update_drowsiness_level()

def update_drowsiness_level():
    print("update_drowsiness_level")
    global drowsiness_level, eye_closure_timestamps
    count = len(eye_closure_timestamps)
    print("update_drowsiness_level", count)
    if count >= 25:
        drowsiness_level = "Critical"
    elif count >= 15:
        drowsiness_level = "Major"
    elif count >= 5:
        drowsiness_level = "Low"
    else:
        drowsiness_level = "None"
    print("update_drowsiness", drowsiness_level)

@app.route('/api/user', methods=['POST'])
def create_user():
    global user_id
    data = request.json
    password_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    user_id = session.get('user_id')
    print(user_id, 'signup')


    return jsonify(user_id=user_id, message='User created successfully'), 201


@app.route('/api/signin', methods=['POST'])
def signin():
    global user_id
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify(message='User does not exist'), 401

    if not user.verify_password(password):
        return jsonify(message='Invalid password'), 401
    
    session['user_id'] = user.id
    user_id = session.get('user_id')
    print(user_id, 'signin')

    token = user.generate_token()

    return jsonify(token=token, username=user.username), 200


@app.route('/drowsiness_level')
def get_drowsiness_level():
    global drowsiness_level
    return jsonify(level=drowsiness_level)


@app.route('/control_camera', methods=['POST'])
def control_camera():
    global camera_on, start_time, end_time, ride_duration, user_id
    if request.json and 'state' in request.json:
        state = request.json['state']
        if state == 'start':
            camera_on = True
            start_time = time.time()  
        elif state == 'stop':
            camera_on = False
            end_time = time.time()
            ride_duration_seconds = int(end_time - start_time) 
            ride_duration = time.strftime('%H:%M:%S', time.gmtime(ride_duration_seconds)) 
            
            print(user_id, "RideHistory")
            if user_id:
                ride_history = RideHistory(
                    ride_date=date.today(),
                    ride_duration=ride_duration,
                    drowsiness_level=drowsiness_level,
                    user_id=user_id
                )
                db.session.add(ride_history)
                db.session.commit()
            else:
                print("invalid user id : did not save")


            if start_time is not None: 
                start_time = None  
        return jsonify({"success": True, "state": camera_on})
    return jsonify({"success": False})






@app.route('/api/ride_history', methods=['GET'])
def get_ride_history():
    try:
        user_id = session.get('user_id')

        ride_histories = RideHistory.query.filter_by(user_id=user_id).all()
        ride_history_data = []
        for ride_history in ride_histories:
            ride_history_data.append({
                'ride_date': ride_history.ride_date,
                'ride_duration': str(ride_history.ride_duration),  # Convert to string
                'drowsiness_level': ride_history.drowsiness_level
            })
        return jsonify(ride_history_data), 200
    except Exception as e:
        return jsonify(message='Failed to retrieve ride history', error=str(e)), 500



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





