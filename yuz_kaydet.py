from picamera2 import Picamera2
import cv2
import os

# --- 1. Get person's name ---
name = input("Enter the person's name (no Turkish characters): ").strip().lower()
save_path = os.path.join("known_faces", name)
os.makedirs(save_path, exist_ok=True)

# --- 2. Continue from existing photo count ---
existing_photos = [f for f in os.listdir(save_path) if f.endswith((".jpg", ".png"))]
count = len(existing_photos)
max_photos = 20

# --- 3. Initialize the camera ---
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# --- 4. Load Haar cascade for face detection ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Press SPACE to capture a face, or Q to quit.")

# --- 5. Main loop for capturing faces ---
while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Manual Face Capture", frame)
    key = cv2.waitKey(1)

    if key == 32:  # SPACE key
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            filename = os.path.join(save_path, f"{name}_{count}.jpg")
            cv2.imwrite(filename, face)
            print(f"Saved: {filename}")
            count += 1
            if count >= max_photos:
                break

    elif key == ord("q"):
        break

    if count >= max_photos:
        print("Reached maximum photo count.")
        break

# --- 6. Cleanup ---
picam2.stop()
cv2.destroyAllWindows()
