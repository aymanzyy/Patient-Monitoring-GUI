import certifi
from flask import Flask, request, jsonify, json
from patient import Patient
from mongoDBFuncs import *
from pymodm import connect
import ssl

ca = certifi.where()
app = Flask(__name__)


def connect_to_Mongo():
    """ Connect to MongoDatabase

    Function gets called via the main loop
    in order to connect application to database

    """
    print("Welcome to MongoDB!")
    connect('mongodb+srv://azy4:easy@bme547.7ayqw.mongodb.net/'
            'tester?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)
    print("Connected Successfully!")
    return


@app.route("/api/patient/new_patient", methods=["POST"])
def new_patient():
    """ New patient request

    Recieves post request and calls
    data_driver to handle saving onto
    MongoDB

    Returns:
        status (str): Status message of request
        code (int): Status code of request

    """
    in_data = request.get_json()
    _, status, code = data_driver(in_data)
    return status, code


@app.route("/api/monitoring/get_list", methods=["GET"])
def get_mrn_list():
    """ GET route to obtain a list of all MRNs
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message or
        results string containing the list of strings.
    """
    answer, status_code = get_id_list_from_db()
    print(answer)
    return json.dumps(answer), status_code


@app.route("/api/monitoring/get_patient_name/<record_num>", methods=["GET"])
def get_patient_name(record_num):
    """ GET route to obtain a patient's name given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient name, plus a status code.
    """
    answer, status_code = get_patient_name_from_db(record_num)
    print(answer)
    return jsonify(answer), status_code


@app.route("/api/monitoring/get_patient_hr/<record_num>", methods=["GET"])
def get_patient_hr(record_num):
    """ GET route to obtain a patient's hr given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient hr, plus a status code.
    """
    answer, status_code = get_patient_hr_from_db(record_num)
    print(answer)
    return jsonify(answer), status_code


@app.route("/api/monitoring/get_patient_timestamp/<record_num>",
           methods=["GET"])
def get_patient_timestamp(record_num):
    """ GET route to obtain a patient's timestamp given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient hr, plus a status code.
    """
    answer, status_code = get_patient_timestamp_from_db(record_num)
    print(answer)
    return jsonify(answer), status_code


@app.route("/api/monitoring/get_patient_ecg/<record_num>", methods=["GET"])
def get_patient_ecg(record_num):
    """ GET route to obtain a patient's ECG given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient ECG, plus a status code.
    """
    answer, status_code = get_patient_ecg_from_db(record_num)
    print(answer)
    return answer, status_code


@app.route("/api/monitoring/get_ecg_list/<record_num>", methods=["GET"])
def get_ecg_list(record_num):
    """ GET route to obtain a patient's ECG LIST given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient ECG, plus a status code.
    """
    answer, status_code = get_ecg_list_from_db(record_num)
    print(answer)
    return json.dumps(answer), status_code


@app.route("/api/monitoring/get_med_list/<record_num>", methods=["GET"])
def get_med_list(record_num):
    """ GET route to obtain a patient's medical image LIST given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient medical images,
        plus a status code.
    """
    answer, status_code = get_med_list_from_db(record_num)
    print(answer)
    return json.dumps(answer), status_code


@app.route("/api/add_on/patient_dict/<patient_id>", methods=["GET"])
def get_patient_info(patient_id):
    """ GET route to obtain database entry for a patient by id number

    This function implements a GET route with a variable URL.  The desired
    patient id number is included as part of the URL.  The function calls
    another function to implement the functionality and receives an
    answer and status code from that function, which it then returns.

    Returns:
        dict, int: a result of a dictionary containing the
        patient data, plus a status code.
    """
    answer, status_code = get_patient_dict(patient_id)
    return json.dumps(answer), status_code


@app.route("/api/add_on/patient_record_numbers/", methods=["GET"])
def get_patient_record_numbers():
    """ GET route to obtain medical record number for a patient

    This function implements a GET route with a variable URL. The
    function calls
    another function to implement the functionality and receives an
    answer and status code from that function, which it then returns.
    Returns a list of all patient medical record numbers available.

    Returns:
        list, int: a result of a list of patient medical record numbers,
        plus a status code.
    """
    answer, status_code = get_pat_record_numbers()
    return json.dumps(answer), status_code


@app.route("/api/add_on/get_patient_name/<record_num>", methods=["GET"])
def get_patient_name_2(record_num):
    """ GET route to obtain a patient's name given MRN
    This function implements a GET route with a set URL.

    Returns:
        str, int: An error message if patient_id was invalid or a
        results string containing the patient name, plus a status code.
    """
    answer, status_code = get_patient_name_from_db(record_num)
    print(answer)
    return jsonify(answer), status_code


if __name__ == '__main__':
    connect_to_Mongo()
    app.run(host="0.0.0.0", port=5200)
