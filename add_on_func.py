import requests
import base64
import binascii
import matplotlib.pyplot as mpimg
import io


server = "http://vcm-25858.vm.duke.edu:5200"
# server = 'http://127.0.0.1:5000'


def get_patient_mrns_from_server():
    """Obtains medical record numbers from server

    Function communicates with server to obtain the patient record
    numbers from database.

    Returns(str): list of medical record numbers

    """
    r = requests.get(server + "/api/add_on/patient_record_numbers/")
    print(r.text)
    return r.text


def get_patient_dict(patient_id):
    """Obtains patient information using medical record number

    Function takes each patient id and outputs a dictionary containing
    corresponding patient data which includes ecg trace and heart rate.

    Args(str): patient medical record number

    Returns(dict): dictionary of patient information for specified
                patient medical record number

    """
    r = requests.get(server + "/api/add_on/patient_dict/"+str(patient_id))
    print(r.status_code)
    print(r.text)
    return r.text, r.status_code


def get_patient_name_2_from_server(record_num_string):
    """ Send server GET request

    This function takes sends the server a get
    request that will return a patient's name
    that matches the medical record number

    Returns:
        r.text (str): Status of request

    """
    r = requests.get(server+"/api/add_on/get_patient_name/"
                     + str(record_num_string))
    return r.text, r.status_code


'''
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
'''
