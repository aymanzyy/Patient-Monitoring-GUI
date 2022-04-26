import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from numpy import record
from patientGuiFuncs import *
from monitoringGuiFuncs import *
from mongoDBFuncs import *
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from ecg_analysis import *
from patient import Patient
from skimage.io import imsave
import os

root = tk.Tk()
root.title("Monitoring-Side GUI Client")
root.geometry('900x900')

mrn_label = ttk.Label(root)
name_label = ttk.Label(root)
hr_label = ttk.Label(root)
timestamp_label = ttk.Label(root)

selected_record_num = None
current_ecg_image_b64 = None


def monitoring_side_gui():
    """ Monitoring-Side GUI

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

    def get_list_info():
        """ Gets a list of medical record numbers

            By calling other functionality, this
            function gets the list of patient MRNs
            from the server and returns it
            """
        answer = json.loads(get_patient_list_from_server())
        print(answer)
        return answer

    def get_ecg_list_info(record_num):
        """ Gets a list of ecg images

            By calling other functionality, this
            function gets the list of patient MRNs
            from the server and returns it

            params:
                record_num(int): MRN of patient
            """
        answer = get_ecg_list_from_server(record_num)
        if answer == "NO ECG AVAILABLE":
            return answer
        else:
            return json.loads(answer)

    def get_med_list_info(record_num):
        """ Gets a list of medical record numbers

            By calling other functionality, this
            function gets the list of patient MRNs
            from the server and returns it

            params:
                record_num(int): MRN of patient
            """
        answer = get_med_list_from_server(record_num)
        if answer == "NO MED IMAGE AVAILABLE":
            return answer
        else:
            return json.loads(answer)

    def get_patient_name(record_num):
        """ Displays the patient name in GUI

            By calling other functionality, this
            function gets the patient name and
            displays it in the GUI

            params:
                record_num(int): MRN of patient
            """
        current_patient_name = json.loads(
            get_patient_name_from_server(record_num))
        name_label.config(text=current_patient_name)
        name_label.grid(column=4, row=2, sticky="w")
        return

    def get_patient_hr(record_num):
        """ Displays the patient heart rate in GUI

            By calling other functionality, this
            function gets the patient heart rate and
            displays it in the GUI

            params:
                record_num(int): MRN of patient
            """
        current_patient_hr = json.loads(
            get_patient_hr_from_server(record_num))
        hr_label.config(text=current_patient_hr)
        hr_label.grid(column=1, row=3, sticky="w")
        return

    def get_patient_timestamp(record_num):
        """ Displays the patient timestamp in GUI

            By calling other functionality, this
            function gets the patient timestamp and
            displays it in the GUI

            params:
                record_num(int): MRN of patient
            """
        current_patient_timestamp = json.loads(
            get_patient_timestamp_from_server(record_num))
        timestamp_label.config(text=current_patient_timestamp)
        timestamp_label.grid(column=4, row=3, sticky="w")
        return

    def get_patient_ecg(record_num):
        """ Displays the patient ecg in GUI

            By calling other functionality, this
            function gets the patient ecg and
            displays it in the GUI

            params:
                record_num(int): MRN of patient
            """
        global current_ecg_image_b64
        current_patient_ecg_b64, status_code = \
            get_patient_ecg_from_server(record_num)
        if current_patient_ecg_b64 == "NO ECG IMAGE" \
                or status_code != 200:
            ecg_image_label.configure(image=hospital_tk_ecg_image)
            ecg_image_label.image = hospital_tk_ecg_image
            return
        current_patient_ecg_array = \
            convert_string_to_ndarray(current_patient_ecg_b64)
        display_ecg_image_from_array(current_patient_ecg_array,
                                     ecg_image_label)
        current_ecg_image_b64 = current_patient_ecg_b64

        return

    def display_ecg_image_from_array(ecg_nd_array, display_label):
        """ Displays the ecg image from nd array

            This is for displaying images that
            will not be downloaded. The image is resized
            and replaces the image before it on the GUI

            params:
                ecg_nd_array(nd_array): image in nd form
                display_label(tk.label): The label where
                    image should be displayed

            """
        f = io.BytesIO()
        imsave(f, ecg_nd_array, plugin='pil')
        out_img = io.BytesIO()
        out_img.write(f.getvalue())
        img_obj = Image.open(out_img)
        resized_img_obj = img_obj.resize((300, 300))
        tk_image = ImageTk.PhotoImage(resized_img_obj)
        display_label.configure(image=tk_image)
        display_label.image = tk_image

        return

    def download_recent_ecg_cmd():
        """ Downloads the most recent ECG image when button is pressed

            By calling other functionality, this
            function downloads the current image based on a b64string
        """

        global current_ecg_image_b64
        convert_string_to_imgfile(current_ecg_image_b64, "most_recent_ecg")
        return

    def display_historic_ecg_cmd(img_list, index):
        """ Display the most historic ECG image when button is pressed

            By calling other functionality, this
            function displays the current image based on a b64string
        """
        b64_img_string = img_list[index]
        nd_array = convert_string_to_ndarray(b64_img_string)
        display_ecg_image_from_array(nd_array, hist_ecg_image_label)
        return

    def download_historic_ecg_cmd(img_list, index):
        """ Downloads the most historic ECG image when button is pressed

            By calling other functionality, this
            function downloads the current image based on a b64string
        """
        b64_img_string = img_list[index]
        convert_string_to_imgfile(b64_img_string, "historic_ecg")
        return

    def display_medical_cmd(img_list, index):
        """ Display the most recent medical image when button is pressed

            By calling other functionality, this
            function display the current image based on a b64string
        """
        b64_img_string = img_list[index]
        nd_array = convert_string_to_ndarray(b64_img_string)
        display_ecg_image_from_array(nd_array, hist_medical_image_label)
        return

    def download_medical_cmd(img_list, index):
        """ Download the most recent medical image when button is pressed

            By calling other functionality, this
            function download the current image based on a b64string
        """
        b64_img_string = img_list[index]
        convert_string_to_imgfile(b64_img_string, "medical_image_")
        return

    def reset_historic_image():
        """ Reset the historic image with default

            Will reset the current historical image to the
            hospital logo
        """
        hist_ecg_image_label.configure(image=hospital_tk_ecg_image)
        return

    def reset_medical_image():
        """ Reset the medical image with default

            Will reset the current medical image to the
            hospital logo
        """
        hist_medical_image_label.configure(image=hospital_tk_ecg_image)
        return

    def updater():
        """ Update the currently displayed information in the GUI

            Every 30 seconds, the GUI will be updated with new
            information for the record number list, current
            patient name, hr, timestamp, recent ecg, historic
            ecgs, and medical images
        """
        print("Updating Information")

        # Update MRN List
        record_number_list = get_list_info()
        if isinstance(record_number_list, str):
            record_number_list = [0]
        center_dropdown["values"] = record_number_list

        # Update Patient Name
        get_patient_name(selected_record_num)

        # Handle patient heartrate
        get_patient_hr(selected_record_num)

        # Handle patient heartrate timestamp
        get_patient_timestamp(selected_record_num)

        # Handle current patient ecg
        get_patient_ecg(selected_record_num)

        if selected_record_num:
            ecg_list = get_ecg_list_info(selected_record_num)
            historic_ecg_handler(ecg_list)

            med_list = get_med_list_info(selected_record_num)
            medical_image_handler(med_list)

        root.after(25000, updater)

    def historic_ecg_handler(ecg_list):
        """ Handles how the historic ecg area works

            This is for displaying historic ecgs if they
            are available. If not, the buttons will
            disappear. When valid ecgs are available,
            they will be abel to be downloaded and
            diplayed.

            params:
                ecg_list(list): list of dicts containing
                ecg_image and timestamp
            """
        if ecg_list and not isinstance(ecg_list, str):
            ecg_time_list, ecg_img_list = \
                get_list_of_times_and_images(ecg_list)
            ecg_dropdown["values"] = ecg_time_list
            ecg_dropdown.current(0)

            # Display Historic ECG Button
            display_historic_button.configure(
                command=(lambda: display_historic_ecg_cmd(
                    ecg_img_list, ecg_dropdown.current())))
            display_historic_button.grid(
                column=5, row=8, columnspan=1, sticky="w")

            # Download Historic ECG Button
            download_historic_button.configure(
                command=(lambda: download_historic_ecg_cmd(
                    ecg_img_list, ecg_dropdown.current())))
            download_historic_button.grid(
                column=5, row=9, columnspan=1, sticky="w")

        else:
            ecg_time_list = []
            ecg_dropdown.set('NO ECG AVAILABLE')
            ecg_dropdown["values"] = ecg_time_list

            reset_historic_image()
            display_historic_button.grid_forget()
            download_historic_button.grid_forget()
        return

    def medical_image_handler(med_list):
        """ Handles how the medical image area works

            This is for displaying medical images if they
            are available. If not, the buttons will
            disappear. When valid med images are available,
            they will be abel to be downloaded and
            diplayed.

            params:
                med_list(list): list of b64 strings of medical
                images
            """
        if med_list and not isinstance(med_list, str):
            image_names = create_image_names(len(med_list))
            med_dropdown["values"] = image_names
            med_dropdown.current(0)

            # Display Historic medical image Button
            display_medical_button.configure(
                command=(lambda: display_medical_cmd(
                    med_list, med_dropdown.current())))
            display_medical_button.grid(column=3, row=12, sticky="w")

            # Download medical image Button
            download_medical_button.configure(
                command=(lambda: download_medical_cmd(
                    med_list, med_dropdown.current())))
            download_medical_button.grid(column=3, row=13, sticky="w")

        else:
            med_dropdown.set('NO IMAGES AVAILABLE')
            ecg_dropdown["values"] = med_list

            reset_medical_image()
            display_medical_button.grid_forget()
            download_medical_button.grid_forget()
        return

    def enter_patient_cmd():
        """ Handles all events when entering new patient file

            By calling other functionality, this
            function displays all the required heartrate,
            name, medical record number, etc.
            """
        global mrn_label
        global name_label
        global hr_label
        global timestamp_label
        global selected_record_num

        # Clears the current patient information
        mrn_label.grid_forget()
        name_label.grid_forget()
        hr_label.grid_forget()

        # Handles MRN
        selected_record_num = record_num.get()
        mrn_label.config(text=str(selected_record_num))
        mrn_label.grid(column=1, row=2, sticky="w")

        # Handle patient Name
        get_patient_name(selected_record_num)

        # Handle patient heartrate
        get_patient_hr(selected_record_num)

        # Handle patient heartrate timestamp
        get_patient_timestamp(selected_record_num)

        # Handle current patient ecg
        get_patient_ecg(selected_record_num)

        # Reset Historic image
        reset_historic_image()

        # Reset medical image
        reset_medical_image()

        # Update Historical ecg dropdown
        ecg_dropdown.set('')
        ecg_dropdown["values"] = []
        ecg_list = get_ecg_list_info(selected_record_num)
        historic_ecg_handler(ecg_list)

        # Update Historical Medical Image dropdown
        med_dropdown.set('')
        med_dropdown["values"] = []
        med_list = get_med_list_info(selected_record_num)
        medical_image_handler(med_list)

        return

    ttk.Label(root, text="Monitoring-Side GUI Client").\
        grid(column=0, row=0, sticky="w")
    # Cancel Button
    cancel_button = ttk.Button(root, text="Cancel",
                               command=abort_program)
    cancel_button.grid(column=5, row=1, columnspan=1, sticky="w")

    # Drop Down menu of Medical Record Numbers
    ttk.Label(root, text="Medical Record Number")\
        .grid(column=3, row=0)
    record_num = tk.IntVar()
    center_dropdown = ttk.Combobox(root, textvariable=record_num)
    center_dropdown.grid(column=3, row=1)
    record_number_list = get_list_info()

    if isinstance(record_number_list, str):
        record_number_list = [0]

    center_dropdown["values"] = record_number_list
    center_dropdown.current(0)
    center_dropdown.state(['readonly'])

    # Enter Patient File Button
    enter_patient_button = ttk.Button(root, text="Enter Patient File",
                                      command=enter_patient_cmd)
    enter_patient_button.grid(column=4, row=1, columnspan=1, sticky="w")

    # Various labels for MRN and heart_rate
    ttk.Label(root, text="Selected MRN:", anchor='e').\
        grid(column=0, row=2, sticky="e")
    ttk.Label(root, text="Patient Name:", anchor='e').\
        grid(column=3, row=2, sticky="e")
    ttk.Label(root, text="Latest HR:", anchor='e').\
        grid(column=0, row=3, sticky="e")
    ttk.Label(root, text="Time of HR:", anchor='e').\
        grid(column=3, row=3, sticky="e")

    # Select & Display Local ECG Image
    ttk.Label(root, text="Most Recent ECG Image:").\
        grid(column=1, row=5, sticky="w")
    local_ecg_image = Image.open("default_images/hosptial.png")
    resized_ecg_image = local_ecg_image.resize((300, 300))
    tk_ecg_image = ImageTk.PhotoImage(resized_ecg_image)
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.image = tk_ecg_image
    ecg_image_label.grid(column=1, row=6, columnspan=3, sticky='w')

    # Download Most Recent ECG Button
    download_recent_button = ttk.Button(root,
                                        text="Download Recent ECG",
                                        command=download_recent_ecg_cmd)
    download_recent_button.grid(column=1, row=7,
                                columnspan=1, sticky="w")

    # Drop Down menu of Historical ECGs
    ttk.Label(root, text="Historical ECG Images:").\
        grid(column=4, row=7, sticky='w')
    ecg_time = tk.StringVar()
    ecg_dropdown = ttk.Combobox(root, textvariable=ecg_time)
    ecg_dropdown.grid(column=4, row=8, sticky='w')
    ecg_dropdown.state(['readonly'])

    # Display Historic ECG Button
    display_historic_button = ttk.Button(root, text="Display ECG")
    display_historic_button.grid(column=5, row=8,
                                 columnspan=1, sticky="w")
    display_historic_button.grid_forget()

    # Download Historic ECG Button
    download_historic_button = ttk.Button(root, text="Download Historic ECG")
    download_historic_button.grid(column=5, row=9,
                                  columnspan=1, sticky="w")
    download_historic_button.grid_forget()

    # Select & Display Historic ECG Image
    ttk.Label(root, text="Historic ECG Image:").\
        grid(column=4, row=5, sticky="w")
    hospital_image = Image.open("default_images/hosptial.png")
    resized_hospital_image = hospital_image.resize((300, 300))
    hospital_tk_ecg_image = ImageTk.PhotoImage(resized_hospital_image)
    hist_ecg_image_label = ttk.Label(root, image=hospital_tk_ecg_image)
    hist_ecg_image_label.image = hospital_tk_ecg_image
    hist_ecg_image_label.grid(column=4, row=6,
                              columnspan=3, sticky='w')

    # Select & Display Historic Medical Image
    ttk.Label(root, text="Medical Image:").\
        grid(column=1, row=9, sticky="w")
    hist_medical_image_label = ttk.Label(root, image=hospital_tk_ecg_image)
    hist_medical_image_label.image = hospital_tk_ecg_image
    hist_medical_image_label.grid(column=1, row=10, columnspan=3, sticky='w')

    # Drop Down menu of Historical ECGs
    ttk.Label(root, text="Historical Medical Images:").\
        grid(column=1, row=11, sticky='w')
    medical_name = tk.StringVar()
    med_dropdown = ttk.Combobox(root, textvariable=medical_name)
    med_dropdown.grid(column=1, row=12, sticky='w')
    med_dropdown.state(['readonly'])

    # Display Historic ECG Button
    display_medical_button = ttk.Button(root, text="Display Med Image")
    display_medical_button.grid(column=3, row=12, sticky="w")
    display_medical_button.grid_forget()

    # Download Historic ECG Button
    download_medical_button = ttk.Button(root, text="Download Med Image")
    download_medical_button.grid(column=3, row=13, sticky="w")
    download_medical_button.grid_forget()

    updater()
    root.mainloop()


if __name__ == "__main__":
    monitoring_side_gui()
