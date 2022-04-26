import datetime
import os
from tkinter import filedialog

import requests
import base64
import io
import matplotlib.image as mpimg

server = "http://vcm-25858.vm.duke.edu:5200"
# server = 'http://127.0.0.1:5000'


def get_patient_list_from_server():
    """ Send server GET request

    This function takes sends the server a get
    request that will return a list of patient
    medical record numbers

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_list")
    return r.text


def get_ecg_list_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a list of patient
    ecg timestamps

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_ecg_list"
                            "/"+str(record_num_string))
    return r.text


def get_med_list_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a list of patient
    ecg timestamps

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_med_list"
                            "/"+str(record_num_string))
    return r.text


def get_patient_name_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a patient's name
    that matches the medical record number

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_patient_name"
                            "/"+str(record_num_string))
    return r.text


def get_patient_hr_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a patient's heart rate
    that matches the medical record number

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_patient_hr"
                            "/"+str(record_num_string))
    return r.text


def get_patient_timestamp_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a patient's timestamp
    that matches the medical record number

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_patient_"
                            "timestamp/"+str(record_num_string))
    return r.text


def get_patient_ecg_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a patient's b64 ecg string
    that matches the medical record number

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/monitoring/get_patient_ecg"
                            "/"+str(record_num_string))
    return r.text, r.status_code


def convert_string_to_ndarray(b64_string):
    """ Converts b64string to ndarray

    Converts b64string to ndarray for image

    Params:
        b64_string: string variable containing the image
        bytes encoded as a base64 string.
    Returns:
        img_ndarray: variable containing a ndarray with
        image data
    """

    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')

    return img_ndarray


def convert_string_to_imgfile(b64_string, new_filename):
    """ Converts b64string to imgfile

    Converts b64string to imgfile saved to current path

    Params:
        b64_string: string variable containing the image
        bytes encoded as a base64 string.

        new_filename: string variable with base new filename
    Returns:
        img_ndarray: variable containing a ndarray with
        image data
    """

    image_bytes = base64.b64decode(b64_string)
    dir = os.getcwd()
    folder_dir = os.path.join(dir, "saved_images")
    date = datetime.datetime.now()
    now = date.strftime("_%Y-%m-%d_%H-%M-%S")
    dirPath2 = os.path.join(folder_dir, new_filename)
    dirPath = dirPath2.rstrip('\n')
    filename_created = dirPath+now
    with open(filename_created + ".png", "wb") as out_file:
        out_file.write(image_bytes)
    return


def get_list_of_times_and_images(ecg_list):
    """ Gets a list of timestamps an images from ecg dictionary

    This function takes a list of dictionaries with keys
    "ecg_image" and "timestamp" and converts it to two
    separate lists of strings that contain names and
    timestamps

    Params:
        ecg_list(list): a list of dictionaries that contain
        ecg_image and timestamp
    Returns:
        time_list(list): list of timestamps strings
        image_list(list): list of image strings
    """
    time_list = []
    image_list = []
    for ecg in ecg_list:
        time_list.append(ecg["timestamp"])
        image_list.append(ecg["ecg_image"])

    return time_list, image_list


def create_image_names(length):
    """ Get a list of image names to display in combobox

    This fucntion creates a list of file names of length
    length that will display in the combobox in my GUI.

    Params:
        length: length of the string you would like
        to show in the combobox
    Returns:
        name_list(list): list of strings of filenames
    """
    name_list = []
    base_name = 'image_no_'
    for index in range(length):
        current_name = base_name + str(index)
        name_list.append(current_name)
    return name_list
