import os
import face_recognition
import pickle
from openpyxl import Workbook
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from PIL import Image, ImageTk

# Global variables
known_face_encodings = None
roll_numbers = None
present_count = 0
live_detection_active = True


# Training function
def train():
    global known_face_encodings, roll_numbers

    main_folder = main_folder_entry.get()
    if not main_folder:
        messagebox.showerror("Error", "Please select the training folder.")
        return

    train_button.config(state=tk.DISABLED)
    status_label.config(text="Training in progress...")

    def training_thread():
        global known_face_encodings, roll_numbers

        try:
            training_folders = [os.path.join(main_folder, folder_name) for folder_name in os.listdir(main_folder) if
                                os.path.isdir(os.path.join(main_folder, folder_name))]

            known_face_encodings = []
            roll_numbers = []

            for training_folder in training_folders:
                roll_number = os.path.basename(training_folder)
                roll_numbers.append(roll_number)
                face_encodings = []
                for image_file in os.listdir(training_folder):
                    image_path = os.path.join(training_folder, image_file)
                    image = face_recognition.load_image_file(image_path)
                    face_encoding = face_recognition.face_encodings(image)[0]
                    face_encodings.append(face_encoding)
                known_face_encodings.append(face_encodings)

            data = {"encodings": known_face_encodings, "roll_numbers": roll_numbers}
            with open("encodings.pickle", "wb") as f:
                pickle.dump(data, f)

            status_label.config(text="Training successfully completed.")
            messagebox.showinfo("Success", "Training successfully completed.")
        except Exception as e:
            status_label.config(text="Training failed.")
            messagebox.showerror("Error", f"Training failed: {str(e)}")

        # After training is complete, enable the train button
        train_button.config(state=tk.NORMAL)

    thread = threading.Thread(target=training_thread)
    thread.start()


# Live face detection function
def live_face_detection():
    global known_face_encodings, roll_numbers, present_count, live_detection_active

    # If training hasn't been done or user chooses to browse for .pickle file
    if known_face_encodings is None or roll_numbers is None:
        pickle_file_path = filedialog.askopenfilename(title="Select Trained Data File",
                                                      filetypes=[("Pickle Files", "*.pickle")])

        if not pickle_file_path:
            return

        with open(pickle_file_path, "rb") as f:
            data = pickle.load(f)
            known_face_encodings = data["encodings"]
            roll_numbers = data["roll_numbers"]

    cap = cv2.VideoCapture(0)

    detected_faces = []  # List to temporarily store detected faces and statuses
    recorded_roll_numbers = set()  # Set to store recorded roll numbers

    # Flag to monitor the live detection loop
    live_detection_active = True

    zoomed_in = False  # Flag to track zoom state
    zoom_scale = 1.5  # Factor by which to zoom in

    while live_detection_active:
        ret, frame = cap.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            roll_number_match = "Unknown"
            status = "Absent"  # Default status

            for i, known_encoding_list in enumerate(known_face_encodings):
                matches = face_recognition.compare_faces(known_encoding_list, face_encoding)
                if any(matches):
                    roll_number_match = roll_numbers[i]
                    status = "Present"  # Change status to "Present"
                    break

            # Calculate the distance between eyes (approximate face size)
            face_width = right - left
            distance_threshold = 0.5  # Adjust this threshold as needed
            if face_width > frame.shape[1] * distance_threshold:
                zoomed_in = True
                zoomed_frame = cv2.resize(frame, None, fx=zoom_scale, fy=zoom_scale)
            else:
                zoomed_in = False
                zoomed_frame = frame

            for i, known_encoding_list in enumerate(known_face_encodings):
                matches = face_recognition.compare_faces(known_encoding_list, face_encoding)
                if any(matches):
                    roll_number_match = roll_numbers[i]
                    status = "Present"  # Change status to "Present"
                    break


            if roll_number_match != "Unknown":
                if roll_number_match not in recorded_roll_numbers:
                    detected_faces.append((roll_number_match, status))
                    recorded_roll_numbers.add(roll_number_match)
                    present_count += 1  # Increase present count for new face

                if zoomed_in:
                    # Draw a rectangle around the detected face in the zoomed frame
                    rectangle_color = (0, 255, 0)  # Green color
                    rectangle_thickness = 2
                    cv2.rectangle(zoomed_frame, (left * zoom_scale, top * zoom_scale), (right * zoom_scale, bottom * zoom_scale), rectangle_color, rectangle_thickness)

        # Display present count on video frame
        font = cv2.FONT_HERSHEY_DUPLEX
        present_text = f"Present: {present_count}"

        # Adjust the text position for better visibility
        text_position = (10, 30)
        text_color = (0, 255, 0)  # Green color

        cv2.putText(frame, present_text, text_position, font, 1.0, text_color, 1)

        cv2.imshow("Face Recognition", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            live_detection_active = False  # Terminate the loop
            break

    # Close the camera window
    cap.release()
    cv2.destroyAllWindows()

    # Sort detected_faces by roll number before saving
    detected_faces.sort(key=lambda x: x[0])

    # Save the detected faces and statuses to Excel
    excel_file_path = "detected_faces.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Detected Faces"
    ws.append(["Roll Number", "Status"])
    for face_info in detected_faces:
        if face_info[0] != "Unknown":
            ws.append(face_info)
    wb.save(excel_file_path)

    print(f"Recognition complete. Detected faces saved to {excel_file_path}")


# Create UI
root = tk.Tk()
root.title("Face Recognition Training and Detection")

# Set window icon
icon_image = Image.open(r"your logo/icon image path here")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

# Set the original size of the window
original_width = 350
original_height = 220
window_geometry = f"{original_width}x{original_height}"
root.geometry(window_geometry)

training_folder_label = tk.Label(root, text="Select Training Folder:")
training_folder_label.pack()

main_folder_entry = tk.Entry(root)
main_folder_entry.pack()

browse_button = tk.Button(root, text="Browse",
                          command=lambda: main_folder_entry.insert(tk.END, filedialog.askdirectory()))
browse_button.pack()

train_button = tk.Button(root, text="Train", command=train)
train_button.pack()

detect_button = tk.Button(root, text="Live Detection", command=live_face_detection)
detect_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
