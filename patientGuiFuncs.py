import os
import requests
import base64
import io

server = "http://vcm-25858.vm.duke.edu:5200"
# server = 'http://127.0.0.1:5000'


def new_patient_post_request(record, name, medical_image,
                             ecg_image, heart_rate):
    """ Send server POST request

    This function takes in information from the GUI
    and calls another function to package information
    into a dictionary to be used in the request

    Args:
        record (int/str): Medical Record
        name (str): Patient name
        medical_image (str): Image in b64 string
        ecg_image (str): Image in b64 string
        heart_rate (float): Heart Rate

    Returns:
        r.text (str): Status of request

    """
    send_dict = package_into_dict(record, name, medical_image,
                                  ecg_image, heart_rate)
    r = requests.post(server+"/api/patient/new_patient", json=send_dict)
    return r.text


def package_into_dict(record, name, medical_image, ecg_image, heart_rate):
    """ Package variables into dict

    To post information to a server, we package variables
    into a dict via this function.

    Args:
        record (int/str): Medical Record
        name (str): Patient name
        medical_image (str): Image in b64 string
        ecg_image (str): Image in b64 string
        heart_rate (float): Heart Rate

    Returns:
        new_patient_data (str): Dict of info

    """
    keys = ["record", "name", "medical_image", "ecg_image", "heart_rate"]
    objs = [record, name, medical_image, ecg_image, heart_rate]
    new_patient_data = dict()
    for key, obj in zip(keys, objs):
        if obj:
            new_patient_data[key] = obj
    return new_patient_data


def convert_image_to_str(filename):
    """ Convert image to b64 string

    Function opens iamge given a
    path and converts that iamge
    into base644 string

    Args:
        filename (str): Path of image

    Returns:
        str(b64_bytes): Base64 string of converted image
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    return str(b64_bytes, encoding="utf-8")


def convert_to_str(non_str):
    """ Convert variable to str

    Convert variable to string

    Args:
        non_str (varies): Non string

    Returns:
        str (str): String of variable

    """
    return str(non_str)
