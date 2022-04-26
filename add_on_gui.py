from pymodm import connect
from pymodm import MongoModel, fields
from add_on_func import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import json
from skimage.io import imsave
import matplotlib.pyplot as mpimg
from monitoringGuiFuncs import convert_string_to_ndarray

current_patient_dict = {}


def admin_gui():

    def abort_program():
        """ Abort GUI

        By destroying the root, this function
        exits the GUI client

        """
        root.destroy()

    def display_hr(heart_rate, count):
        """ Displays heart rate for each patient.

            This function outputs the heart rate from each patient
            dictionary onto the gui

            Args(str): heart rate, count
        """
        ttk.Label(root, text=str(heart_rate)).\
            grid(column=0, row=count+3, columnspan=2, sticky=tk.W)

    def display_name(name, count):
        """ Displays name for each patient.

            This function outputs the name from each patient
             onto the gui

            Args(str): name, count
        """
        ttk.Label(root, text=str(name)).\
            grid(column=3, row=count+3, columnspan=5, sticky=tk.W)

    def display_ecg_image_from_array(ecg_nd_array):
        """ Displays the ecg image from nd array

            This is for deplaying images that
            will not be downloaded. The image is resized
            and replaces the image before it on the GUI

        """
        f = io.BytesIO()
        imsave(f, ecg_nd_array, plugin='pil')
        out_img = io.BytesIO()
        out_img.write(f.getvalue())
        img_obj = Image.open(out_img)
        resized_img_obj = img_obj.resize((300, 300))
        tk_image = ImageTk.PhotoImage(resized_img_obj)
        ecg_image_label.configure(image=tk_image)

        return

    def display_ecg(ecg):
        """ Displays ecg image for each patient.

            This function converts ecg data into an ndarray
             and then displays the image from each patient
            dictionary onto the gui

            Args(str): ecg
        """
        nd_array = convert_string_to_ndarray(ecg)
        display_ecg_image_from_array(nd_array)
        return

    def display_default():
        """Displays the default ecg image.

        When a patient wants to return to default image this
        function assists in accomplishing that
        """
        ecg_image_label.config(image=tk_ecg_image)
        return

    def display_patient_list():
        """Displays patient information for each specified category.

        Uses the medical record number to access patient
        data which includes patient
        name, heart rate, and ecg image. This information
        is then displayed in gui

        """
        global current_patient_dict
        mrn_list = json.loads(get_patient_mrns_from_server())

        all_patients_info = []

        for count_hr, mrn in enumerate(mrn_list):
            current_patient_hr, status = get_patient_dict(mrn)
            if status == 200:
                try:
                    patient_info_hr = json.loads(current_patient_hr)
                    display_hr(patient_info_hr["heart_rate"], count_hr)
                except KeyError:
                    display_hr("No heartrate", count_hr)
            else:
                display_hr("No heartrate", count_hr)
        for count, mrn in enumerate(mrn_list):
            current_patient_ecg, status = get_patient_dict(mrn)
            if status == 200:
                try:
                    patient_info_1 = json.loads(current_patient_ecg)
                    all_patients_info.append(patient_info_1)
                    ttk.Button(root, text="Display ECG Image",
                               command=(lambda count=count:
                                        display_ecg(all_patients_info
                                                    [count]["ecg_image"])))\
                        .grid(column=8, row=count + 3,
                              columnspan=8, sticky=tk.W)
                except KeyError:
                    ttk.Button(root, text="NO ECG IMAGE",
                               command=(lambda: display_default())). \
                        grid(column=8, row=count + 3,
                             columnspan=8, sticky=tk.W)
            else:
                ttk.Button(root, text="NO ECG IMAGE",
                           command=(lambda: display_default())). \
                    grid(column=8, row=count + 3,
                         columnspan=8, sticky=tk.W)
        for count, mrn in enumerate(mrn_list):
            current_patient, status = get_patient_name_2_from_server(mrn)
            if status == 200:
                try:
                    patient_info = json.loads(current_patient)
                    print(patient_info)
                    display_name(patient_info, count)
                except KeyError:
                    display_name("No Name", count)
            else:
                display_name("No Name", count)
        root.after(3000, display_patient_list)

    def reset_ecg_image():
        """ Reset medical image

        Once triggered via tkinter button, this function
        resets the image currently displaying on the ecg
        image side, replacing it with the default image

        """
        local_image = Image.open("default_images/hosptial.png")
        resized_image = local_image.resize((300, 300))
        tk_ecg_image = ImageTk.PhotoImage(resized_image)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image
    root = tk.Tk()
    root.title("Add_on GUI")
    root.geometry('700x700')
    root.after(3000, display_patient_list)
    # Labels
    ttk.Label(root, text="Heart Rate").\
        grid(column=0, row=0, columnspan=2, sticky=tk.W)
    ttk.Label(root, text="Patient Name").\
        grid(column=3, row=0, columnspan=5, sticky=tk.W)
    ttk.Label(root, text="ECG").\
        grid(column=8, row=0, columnspan=8, sticky=tk.W)

    # Image
    ttk.Label(root, text="ECG Image:").\
        grid(column=1, row=20, columnspan=3, sticky=tk.W)
    local_ecg_image = Image.open("default_images/hosptial.png")
    resized_ecg_image = local_ecg_image.resize((300, 300))
    tk_ecg_image = ImageTk.PhotoImage(resized_ecg_image)
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.image = tk_ecg_image
    ecg_image_label.grid(column=1, row=21, rowspan=18)

    # Buttons
    ttk.Button(root, text="Close Window", command=abort_program)\
        .grid(column=5, row=21, sticky=tk.W)
    ttk.Button(root, text="Reset ECG Image", command=reset_ecg_image)\
        .grid(column=4, row=21, sticky=tk.W)

    # Restart GUI
    # start GUI

    root.mainloop()


if __name__ == '__main__':
    admin_gui()
