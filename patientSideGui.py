import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from numpy import record
from patientGuiFuncs import *
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from ecg_analysis import *
import os

from server import new_patient
TK_SILENCE_DEPRECATION = 1

post_heart_rate = None
post_med_image = None
post_ecg_image = None
ecg_image_flag = True
med_image_flag = True


def patient_side_gui():
    """ Patient-Side GUI

    This window contains all of the GUI/tkinter
    functionality required for the user to interact
    with the server and in turn the MongoDB.
    Functionality is broken down into different
    buttons/functions

    """
    def abort_program():
        """ Abort GUI

        By destroying the root, this function
        exits the GUI client

        """
        root.destroy()
        return

    def compute_ecg_command():
        """ Process ECG file and compute heart_rate

        This function allows a user to select a .csv
        file and compute heart rate and ecg trace
        based on previously defined ecg_analysis function.
        Once the ecg trace is calculated, it will update
        the ecg image window.


        """
        global post_med_image
        global post_ecg_image
        global post_ecg_path
        global post_heart_rate
        ecg_path = filedialog.askopenfilename(initialdir="ecg_test_data")
        if ecg_path == "":
            return
        ecg_data = import_data(ecg_path)
        peak_array = find_peaks(ecg_data)
        heartrate = get_heartrate(ecg_data[:, 0], peak_array)
        plotter = plot_trace(ecg_data, peak_array, ecg_path)
        post_heart_rate = heartrate
        heart_rate = convert_to_str(heartrate)
        calc_hr.set(heart_rate)
        print(plotter)
        temp_image = Image.open(plotter)
        res_temp_image = temp_image.resize((400, 400))
        tk_ecg_image = ImageTk.PhotoImage(res_temp_image)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image
        base_ecg_image = convert_image_to_str(plotter)
        post_ecg_image = base_ecg_image
        return

    def display_med_image():
        """ Displays the selected medical image

        This functions gets triggered via a tkinter button,
        allowing the user to choose a medical image to view.
        Once a file has been selected, the image is resized
        and replacees the image before it on the GUI

        """
        global post_med_image
        filename = filedialog.askopenfilename(initialdir="images")
        if filename == "":
            return
        temp_image = Image.open(filename)
        res_temp_image = temp_image.resize((400, 400))
        tk_image = ImageTk.PhotoImage(res_temp_image)
        med_image_label.configure(image=tk_image)
        med_image_label.image = tk_image
        base_med_image = convert_image_to_str(filename)
        filename = os.path.basename(filename)
        post_med_image = base_med_image
        return

    def display_ecg_image():
        """ Displays the selected medical image

        This functions gets triggered via a tkinter button,
        allowing the user to choose an ECG traceimage to view.
        Once a file has been selected, the image is resized
        and replaces the image before it on the GUI

        """
        global post_ecg_image
        filename = filedialog.askopenfilename(initialdir="images")
        if filename == "":
            return
        temp_image = Image.open(filename)
        res_temp_image = temp_image.resize((400, 400))
        tk_image = ImageTk.PhotoImage(res_temp_image)
        ecg_image_label.configure(image=tk_image)
        ecg_image_label.image = tk_image
        base_ecg_image = convert_image_to_str(filename)
        filename = os.path.basename(filename)
        post_ecg_image = base_ecg_image
        return

    def reset_med_image():
        """ Reset medical image

        Once triggered via tkinter button, this function
        resets the image currently displaying on the medical
        image side, replacing it with the default image

        """
        global post_med_image
        local_image = Image.open("default_images/hosptial.png")
        resized_image = local_image.resize((400, 400))
        tk_med_image = ImageTk.PhotoImage(resized_image)
        med_image_label.configure(image=tk_med_image)
        med_image_label.image = tk_med_image
        post_med_image = None

    def reset_ecg_image():
        """ Reset medical image

        Once triggered via tkinter button, this function
        resets the image currently displaying on the ecg
        image side, replacing it with the default iamge

        """
        global post_ecg_image
        local_image = Image.open("default_images/hosptial.png")
        resized_image = local_image.resize((400, 400))
        tk_ecg_image = ImageTk.PhotoImage(resized_image)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image
        post_ecg_image = None

    def check_record_exists():
        """ Check if medical record number is entered

        In order for a server request to be made, the
        minimum a user has to input is a record number.
        In order to stop users from clicking the Post
        Info button, this function disables the button
        when it detects no entry in the medical record
        number text box.

        """

        if len(record_entry.get()) == 0:
            post_info_button.config(state=tk.DISABLED)
        else:
            post_info_button.config(state=tk.NORMAL)
        root.after(200, check_record_exists)

    def post_info():
        """ Call server post request

        In order for the server to receive information,
        we create this function that calls another function
        to package and submit the post request

        Returns:
            return_mes (str): Return message from POST

        """
        global post_med_image
        global post_ecg_image
        global post_heart_rate

        pat_record = record_entry.get()
        pat_name = name_entry.get()
        pat_medical_image = post_med_image
        pat_heart_rate = post_heart_rate
        pat_ecg_image = post_ecg_image
        return_mes = new_patient_post_request(pat_record, pat_name,
                                              pat_medical_image, pat_ecg_image,
                                              pat_heart_rate)
        post_ecg_image = None
        post_med_image = None
        post_heart_rate = None
        print(return_mes)
        status_msg.set(return_mes)
        return return_mes

    root = tk.Tk()
    root.title("Patient-Side GUI Client")
    root.geometry('900x625')

    ttk.Label(root, text="Patient-Side GUI Client").grid(column=0,
                                                         row=0,
                                                         sticky="w")

    # Medical Record Number Entry
    ttk.Label(root, text="Medical Record Number:").grid(column=0, sticky="w")
    record_entry = tk.StringVar()
    tk.Entry(root, textvariable=record_entry, width=25).grid(column=1,
                                                             row=1,
                                                             columnspan=3,
                                                             sticky="w")

    # Patient Name Entry
    ttk.Label(root, text="Patient Name:").grid(column=0, sticky="w")
    name_entry = tk.StringVar()
    tk.Entry(root, textvariable=name_entry, width=25).grid(column=1,
                                                           row=2,
                                                           columnspan=3,
                                                           sticky="w")

    # Heart Rate Status
    calc_hr = tk.StringVar()
    calc_hr.set("Nothing Here For Now")
    ttk.Label(root, text="Heart Rate:").grid(column=0, sticky="w")
    ttk.Entry(root, text=calc_hr).grid(column=1, row=3, sticky="w")

    # Select & Display Local Computer Image
    ttk.Label(root, text="Local Medical image:").grid(column=0, row=11)
    local_image = Image.open("default_images/hosptial.png")
    resized_image = local_image.resize((400, 400))
    tk_med_image = ImageTk.PhotoImage(resized_image)
    med_image_label = ttk.Label(root, image=tk_med_image)
    med_image_label.image = tk_med_image
    med_image_label.grid(column=0, row=12, columnspan=3)

    ttk.Button(root, text="Display Medical Image",
               command=display_med_image).grid(column=3,
                                               row=0,
                                               columnspan=1,
                                               sticky="e")
    ttk.Button(root, text="Reset Medical Image",
               command=reset_med_image).grid(column=4, row=0)

    # Select & Display Local ECG Image
    ttk.Label(root, text="Local ECG Image:").grid(column=3, row=11)
    local_ecg_image = Image.open("default_images/hosptial.png")
    resized_ecg_image = local_ecg_image.resize((400, 400))
    tk_ecg_image = ImageTk.PhotoImage(resized_ecg_image)
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.image = tk_ecg_image
    ecg_image_label.grid(column=3, row=12, columnspan=3)

    ttk.Button(root, text="Display ECG file",
               command=display_ecg_image).grid(column=3,
                                               row=1,
                                               columnspan=1,
                                               sticky="e")
    ttk.Button(root, text="Reset ECG Image",
               command=reset_ecg_image).grid(column=4,
                                             row=1,
                                             columnspan=1,
                                             sticky="e")

    # Process Local ECG Data
    # ttk.Label(root, text="Local ECG File:").grid(column=7,sticky="w")
    ttk.Button(root, text="Process ECG file",
               command=compute_ecg_command).grid(column=3,
                                                 row=2,
                                                 columnspan=1,
                                                 sticky="e")
    ecg_file = tk.StringVar()

    # Send API Request
    post_info_button = ttk.Button(root, text="Post Info", command=post_info)
    post_info_button.grid(column=5, row=0, columnspan=1, sticky="e")

    # Cancel Button
    cancel_button = ttk.Button(root, text="Cancel", command=abort_program)
    cancel_button.grid(column=5, row=1, columnspan=1, sticky="w")

    # Status Message
    status_msg = tk.StringVar()
    status_msg.set("Nothing Here For Now")
    ttk.Label(root, text="Status:").grid(column=3, row=4, sticky="w")
    ttk.Entry(root, text=status_msg).grid(column=4, row=4, sticky="w")

    check_record_exists()
    root.mainloop()


if __name__ == "__main__":
    patient_side_gui()
