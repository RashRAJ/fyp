from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2


mixer.init()
mixer.music.load("music.wav")

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def detector():
    try:
        print("detect")
        thresh = 0.25
        frame_check = 20
        detect = dlib.get_frontal_face_detector()
        predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
        camera=cv2.VideoCapture(0)

        flag=0
        while True:
            success,frame=camera.read()
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
                    leftEAR = eye_aspect_ratio(leftEye)
                    rightEAR = eye_aspect_ratio(rightEye)
                    ear = (leftEAR + rightEAR) / 2.0
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                    if ear < thresh:
                        flag += 1
                        print (flag)
                        if flag >= frame_check:
                            cv2.putText(frame, "****************ALERT!****************", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.putText(frame, "****************ALERT!****************", (10,325),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            mixer.music.play()
                    else:
                        flag = 0
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
        print(f"detect done - frame: ${frame}")
        return frame
            # yield (b'--frame\r\n'
            #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Detection failed: {e}")

def test():
    print("test")
    detector()
    print (eye_aspect_ratio(1))
    # return "test"