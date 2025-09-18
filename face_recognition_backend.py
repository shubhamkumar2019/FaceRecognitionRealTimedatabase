from flask import Flask, jsonify, request, render_template
import cv2
import face_recognition
import numpy as np
import pickle
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import os

app = Flask(__name__, template_folder=os.path.abspath(
    "C:\\Users\\KIIT\\PycharmProjects\\FaceRecognitionRealTimeDatabase\\template"))  # Ensure correct path


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-c7a6e-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')


with open("EncodeFile.p", "rb") as file:
    encode_list_known_with_ids = pickle.load(file)
encode_list_known, student_ids = encode_list_known_with_ids


last_update_times = {}


@app.route('/')
def home():
    return render_template("1a.html")


@app.route('/attendance', methods=['GET'])
def get_attendance():
    students = ref.get()
    return jsonify(students)

@app.route('/face_recognition_frontend.html')
def face_recognition_frontend():
    return render_template("face_recognition_frontend.html")

@app.route('/1b.html')
def about():
    return render_template("1b.html")

@app.route('/1c.html')
def teacher():
    return render_template("1c.html")

@app.route('/recognize', methods=['POST'])
def recognize_faces():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_np = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Invalid image data"}), 400

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    recognized_students = []
    recognized_ids = set()
    THRESHOLD = 0.5  # Face distance threshold

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(encode_list_known, face_encoding)
        best_match_index = np.argmin(face_distances)
        confidence = face_distances[best_match_index]

        if confidence <= THRESHOLD:
            matches = face_recognition.compare_faces(encode_list_known, face_encoding)
            if matches[best_match_index]:
                student_id = student_ids[best_match_index]

                if student_id in recognized_ids:
                    continue  # Skip duplicate

                recognized_ids.add(student_id)
                student_data = ref.child(student_id).get()
                current_time = datetime.now()
                last_update_time = last_update_times.get(student_id, current_time - timedelta(seconds=31))

                if (current_time - last_update_time).total_seconds() >= 30:
                    total_attendance = student_data.get("total_attendance", 0) + 1
                    last_attendance_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    ref.child(student_id).update({
                        "total_attendance": total_attendance,
                        "last_attendance_time": last_attendance_time
                    })
                    last_update_times[student_id] = current_time
                else:
                    total_attendance = student_data.get("total_attendance", 0)
                    last_attendance_time = student_data.get("last_attendance_time", "N/A")

                recognized_students.append({
                    "id": student_id,
                    "name": student_data.get("name", "Unknown"),
                    "total_attendance": total_attendance,
                    "last_attendance_time": last_attendance_time,
                    "major": student_data.get("major", "N/A"),
                    "section": student_data.get("section", "N/A"),
                    "starting_year": student_data.get("starting_year", "N/A")
                })
        else:
            print(f"Low confidence ({confidence:.2f}), face not recognized.")

    if not recognized_students:
        return jsonify({"error": "No reliable matches found"}), 200

    return jsonify({"recognized_students": recognized_students})





if __name__ == '__main__':
    app.run(debug=True)