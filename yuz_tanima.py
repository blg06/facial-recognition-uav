import cv2
import face_recognition
import os
import numpy as np
import json
from picamera2 import Picamera2
import time

# Load known faces
known_face_encodings = []
known_face_names = []
known_faces_dir = "known_faces"

for person_name in os.listdir(known_faces_dir):
    person_dir = os.path.join(known_faces_dir, person_name)
    if not os.path.isdir(person_dir):
        continue
    for filename in os.listdir(person_dir):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(person_dir, filename)
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_image)
            if len(encodings) > 0:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)

# Load additional face data
with open("face_data.json", "r", encoding="utf-8") as f:
    face_data = json.load(f)

# Initialize the PiCamera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (800, 600)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)

process_every_n_frames = 5
frame_count = 0
recent_faces = {}
display_duration = 3

while True:
    frame = picam2.capture_array()
    current_time = time.time()
    frame_count += 1

    if frame_count % process_every_n_frames == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        current_detected = {}

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            if name in face_data:
                person = face_data[name]
            else:
                person = {
                    "name": "Unknown",
                    "age": "-",
                    "tc": "-",
                    "criminal_record": "-"
                }

            face_key = name + str(top * 2) + str(left * 2)  # unique-ish key
            current_detected[face_key] = {
                "data": person,
                "time": current_time,
                "coords": (top * 2, right * 2, bottom * 2, left * 2)
            }

        recent_faces = current_detected

    for name, info in recent_faces.items():
        top, right, bottom, left = info["coords"]
        person = info["data"]
        is_criminal = person["criminal_record"].lower() == "evet"

        box_color = (0, 0, 255) if is_criminal else (0, 255, 0)
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

        lines = [
            ("Name:", person["name"]),
            ("Age:", str(person["age"])),
            ("TC:", "***" + person["tc"][-4:] if person["tc"] != "-" else "-"),
            ("Criminal Record:", person["criminal_record"])
        ]

        y_offset = bottom + 20
        for label, value in lines:
            if label == "Criminal Record:" and is_criminal:
                cv2.putText(frame, f"{label} {value}", (left, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(frame, label, (left, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                cv2.putText(frame, value, (left + 130, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            y_offset += 30

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    time.sleep(0.01)

cv2.destroyAllWindows()
picam2.stop()