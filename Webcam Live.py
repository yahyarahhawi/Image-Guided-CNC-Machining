import cv2
import tkinter as tk
from tkinter import Scale, Label
from PIL import Image, ImageTk
import numpy as np
import skimage.color
from skimage.morphology import disk
import skimage.exposure
import skimage.filters

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # Set up the frames for different sections
        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.display_frame = tk.Frame(self.window)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize video capture
        self.frame_width = 400
        self.frame_height = 300
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            print(f"Failed to open camera with index {self.video_source}")
            self.window.destroy()
            return
        
        # Setup video properties
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        
        # Create canvases for video and images
        self.live_canvas = tk.Canvas(self.display_frame, width=self.frame_width, height=self.frame_height)
        self.live_canvas.grid(row=0, column=0, padx=10, pady=10)
        
        self.base_canvas = tk.Canvas(self.display_frame, width=self.frame_width, height=self.frame_height)
        self.base_canvas.grid(row=1, column=0, padx=10, pady=10)
        
        self.diff_canvas = tk.Canvas(self.display_frame, width=self.frame_width, height=self.frame_height)
        self.diff_canvas.grid(row=0, column=1, padx=10, pady=10)

        self.edge_canvas = tk.Canvas(self.display_frame, width=self.frame_width, height=self.frame_height)
        self.edge_canvas.grid(row=1, column=1, padx=10, pady=10)
        
        # Control buttons and sliders
        self.btn_capture_base = tk.Button(self.control_frame, text="Capture Base Image", command=self.capture_base_image)
        self.btn_capture_base.grid(row=0, column=0, sticky="ew")

        self.btn_compare = tk.Button(self.control_frame, text="Calculate Difference", command=self.compare_images)
        self.btn_compare.grid(row=1, column=0, sticky="ew")

        self.btn_compare_edges = tk.Button(self.control_frame, text="Compare Edges", command=self.compare_edges_function)
        self.btn_compare_edges.grid(row=2, column=0, sticky="ew")

        self.exposure_scale = Scale(self.control_frame, from_=-8, to=-1, label="Exposure", orient=tk.HORIZONTAL)
        self.exposure_scale.grid(row=3, column=0, sticky="ew")

        self.focus_scale = Scale(self.control_frame, from_=0, to=100, label="Focus", orient=tk.HORIZONTAL)
        self.focus_scale.grid(row=4, column=0, sticky="ew")

        # Adding a threshold slider for edge comparison
        self.threshold_scale = Scale(self.control_frame, from_=0.0, to=0.1, resolution=0.001, label="Edge Threshold", orient=tk.HORIZONTAL)
        self.threshold_scale.set(0.02)  # Default threshold
        self.threshold_scale.grid(row=5, column=0, sticky="ew")

        self.accuracy_label = tk.Label(self.control_frame, text="Accuracy:")
        self.accuracy_label.grid(row=6, column=0, sticky="ew")

        self.base_image = None
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.live_photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
            self.live_canvas.create_image(self.frame_width // 2, self.frame_height // 2, image=self.live_photo, anchor=tk.CENTER)
        self.window.after(10, self.update)

    def adjust_exposure(self, event):
        exposure_value = self.exposure_scale.get()
        self.vid.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

    def adjust_focus(self, event):
        focus_value = self.focus_scale.get()
        self.vid.set(cv2.CAP_PROP_FOCUS, focus_value)

    def capture_base_image(self):
        ret, frame = self.vid.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.base_image = Image.fromarray(rgb_frame)
            self.base_photo = ImageTk.PhotoImage(image=self.base_image)
            self.base_canvas.create_image(self.frame_width // 2, self.frame_height // 2, image=self.base_photo, anchor=tk.CENTER)

    def compare_images(self):
        if self.base_image is not None:
            ret, frame = self.vid.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                compared_frame, accuracy = compare(np.array(self.base_image), np.array(rgb_frame))
                self.diff_photo = ImageTk.PhotoImage(image=Image.fromarray(compared_frame))
                self.diff_canvas.create_image(self.frame_width // 2, self.frame_height // 2, image=self.diff_photo, anchor=tk.CENTER)
                self.accuracy_label.config(text=f"Accuracy: {accuracy:.5f}")

    def compare_edges_function(self):
        ret, frame = self.vid.read()
        if ret and self.base_image is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            edges_result, flaws_detected = compare_edges(np.array(self.base_image), np.array(rgb_frame), self.threshold_scale.get())
            edge_image = np.uint8(edges_result * 255)  # Convert boolean array to uint8 for display
            self.edge_photo = ImageTk.PhotoImage(image=Image.fromarray(edge_image))
            self.edge_canvas.create_image(self.frame_width // 2, self.frame_height // 2, image=self.edge_photo, anchor=tk.CENTER)
            # Update the accuracy label to also show flaws detected
            self.accuracy_label.config(text=f"Accuracy: {flaws_detected:.5f} Flaws Detected: {flaws_detected:.2%}")

def compare_edges(img_base, ex1, threshold):
    def find_edges(image):
        gray = (skimage.color.rgb2gray(image) * 255).astype(np.uint8)
        mask = gray < 150
        gray = skimage.exposure.equalize_hist(gray)
        gray = gray * mask
        gray = skimage.exposure.adjust_gamma(gray, 2.6, 5)
        gray = skimage.filters.median(gray, disk(2))
        edges = skimage.filters.farid(gray) > threshold
        return edges
    
    img_base = find_edges(img_base) * 255
    ex1 = find_edges(ex1) * 255
    final = np.clip(ex1 - img_base, a_min=0, a_max=255) > 0
    total = np.sum(img_base < 150)
    numerator = np.sum(final)
    if total > 0:
        flaws_detected = numerator / total
    else:
        flaws_detected = 0  # Avoid division by zero
    return final, flaws_detected


def compare(img_base, ex1):
    canvas = np.zeros_like(img_base)
    img_base = img_base[:, :, 2]
    ex1 = ex1[:, :, 2]
    base_T = 255 - ((img_base > 170) * 255)
    ex1_T = 255 - ((ex1 > 170) * 255)
    window = np.zeros_like(base_T)
    window[:, :] = 1
    base_T = window * base_T
    ex1_T = window * ex1_T
    canvas[:, :, 1] = base_T
    canvas[:, :, 2] = base_T
    canvas[:, :, 0] = ex1_T
    slicable = (skimage.color.rgb2gray(canvas) * 255).astype(np.uint8)
    more = slicable == 54
    less = slicable == 200
    b = np.sum(np.logical_or(base_T, more))
    a = np.sum(base_T > 0)
    accuracy = a / b
    return canvas, accuracy

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "Webcam Application")
