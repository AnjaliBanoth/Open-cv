#we need to install all the libraries first

import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import os

# Load Haar cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Create save folder
if not os.path.exists("saved_faces"):
    os.makedirs("saved_faces")

# Global variables
cap = None
frame = None
faces = []
is_running = False

def start_detection():
    global cap, is_running
    if not is_running:
        cap = cv2.VideoCapture(0)
        is_running = True
        update_frame()

def stop_detection():
    global is_running
    is_running = False
    if cap:
        cap.release()

def update_frame():
    global cap, frame, faces

    if is_running and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Face {i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (255, 0, 0), 2)

            cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Convert and show in GUI
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            lbl_video.imgtk = imgtk
            lbl_video.configure(image=imgtk)

    if is_running:
        lbl_video.after(10, update_frame)

def save_face():
    if frame is None or len(faces) == 0:
        messagebox.showinfo("Info", "No face to save!")
        return

    for i, (x, y, w, h) in enumerate(faces):
        face_img = frame[y:y+h, x:x+w]
        filename = f"saved_faces/face_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
        cv2.imwrite(filename, face_img)
    messagebox.showinfo("Success", f"{len(faces)} face(s) saved!")

def on_exit():
    stop_detection()
    root.destroy()

# GUI Window
root = tk.Tk()
root.title("Face Counter with GUI")
root.geometry("800x600")

lbl_video = tk.Label(root)
lbl_video.pack(padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Start Detection", width=20, command=start_detection).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Stop Detection", width=20, command=stop_detection).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Save Face Image", width=20, command=save_face).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Exit", width=20, command=on_exit).grid(row=0, column=3, padx=10)

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()


#Thank You