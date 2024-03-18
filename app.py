from flask import Flask, render_template, Response
import cv2
from detector import detect


app=Flask(__name__)
# camera = cv2.VideoCapture(0)


# def generate_frames():
#     while True:
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
#             detect.detect()
#             # ret, buffer = cv2.imencode('.jpg', frame)
#             # frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def generate_frames():
#     thresh = 0.25
#     frame_check = 20
#     detect = dlib.get_frontal_face_detector()
#     predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

#     (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
#     (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
#     camera=cv2.VideoCapture(0)

#     flag=0
#     while True:
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
#             frame = imutils.resize(frame, width=450)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             subjects = detect(gray, 0)
#             for subject in subjects:
#                 shape = predict(gray, subject)
#                 shape = face_utils.shape_to_np(shape)
#                 leftEye = shape[lStart:lEnd]
#                 rightEye = shape[rStart:rEnd]
#                 leftEAR = detector.eye_aspect_ratio(leftEye)
#                 rightEAR = detector.eye_aspect_ratio(rightEye)
#                 ear = (leftEAR + rightEAR) / 2.0
#                 leftEyeHull = cv2.convexHull(leftEye)
#                 rightEyeHull = cv2.convexHull(rightEye)
#                 cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
#                 cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
#                 if ear < thresh:
#                     flag += 1
#                     print (flag)
#                     if flag >= frame_check:
#                         cv2.putText(frame, "****************ALERT!****************", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                         cv2.putText(frame, "****************ALERT!****************", (10,325),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                         mixer.music.play()
#                 else:
#                     flag = 0
#             # cv2.imshow("Frame", frame)
#             ret, buffer = cv2.imencode(".jpg", frame)
#             frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames():
    print("In generate_frames")
    detect()
    print("After detect")
        


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)