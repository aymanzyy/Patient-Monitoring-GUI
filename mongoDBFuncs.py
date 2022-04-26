from patient import Patient
from pymodm import errors as pymodm_errors
from datetime import datetime
import base64
import binascii


def data_driver(in_data):
    """ Drives handling of patient data

    Given a dictionary of data, this function
    validates that the dictionary contains
    correctly formatted information via
    calling another function. After this,
    the function checks if the data corresponds
    to an existing patient. If so, it calls
    the appropriate add_existing function and vice
    versa if the patient is new

    Args:
        in_data (dict): Dictionary of patient's
        data

    Returns:
        _ (int): Throwaway variable or patient
        status (str): Status message of save
        code (int): Status code of save

    """
    err1, code1 = overall_dict_validation(in_data)
    throwaway_var = 0
    if code1 != 200:
        return throwaway_var, err1, code1
    try:
        record_init = in_data["record"]
        checkPatient = Patient.objects.raw({"_id": int(record_init)}).first()
        print(checkPatient)
        saved_info, message, code = add_to_existing(in_data, checkPatient)
        return saved_info, message, code
    except pymodm_errors.DoesNotExist:
        print("PYMODM ERROR")
        saved_patient, message, code = add_new_patient_to_db(in_data)
        return saved_patient, message, code


def add_to_existing(in_data, oldPatient):
    """ Add information to existing patient

    The function takes in a patient and
    a dictionary of data to add to an
    existing patient. It goes through each
    variables, appending medical/ecg image
    and heart rate (along with a calculated
    timestamp) into a list. After doing so,
    the patient is saved onto the database
    and an appropriate status message
    and code are returned

    Args:
        in_data (dict): Dictionary of patient data
        oldPatient (Patient): Existing patient

    Returns:
        oldPatient (Patient): Updated patient
        init_msg (str): Status message
        code (int): Status code

    """
    poss_keys = ["medical_image", "ecg_image", "heart_rate", 'timestamp']
    keys_avail = in_data.keys()
    new_dict = dict()
    new_name_bool = 0
    init_msg = "Nothing new added"
    for key in keys_avail:
        if key == "name":
            oldPatient.name = str(in_data['name'])
            new_name_bool = 1
        elif key in poss_keys:
            if key == "medical_image":
                new_dict[key] = in_data[key]
            elif key == "ecg_image":
                new_dict[key] = in_data[key]
            elif key == "heart_rate":
                new_dict[key] = float(in_data[key])
            elif key == "timestamp":
                new_dict[key] = in_data[key]

    if new_name_bool == 1:
        init_msg = "Name updated"
    if 'ecg_image' in keys_avail:
        if 'heart_rate' in keys_avail:
            new_dict['timestamp'] = datetime.now()
    if new_dict != dict():
        oldPatient.data.append(new_dict)
        return oldPatient.save(), "Patient Data Updated", 200
    return oldPatient.save(), init_msg, 200


def add_new_patient_to_db(in_data):
    """ Add new patient to database

    The function takes in a patient and
    a dictionary of data to add to an
    existing patient. It goes through each
    variables, appending medical/ecg image
    and heart rate (along with a calculated
    timestamp) into a list. After doing so,
    the patient is saved onto the database
    and an appropriate status message
    and code are returned

    Args:
        in_data (dict): Dictionary of patient data

    Returns:
        newPatient (Patient): New patient
        init_msg (str): Status message
        code (int): Status code

    """
    new_pat = Patient()
    known_keys = ["record", "name"]
    poss_keys = ["medical_image", "ecg_image", "heart_rate", 'timestamp']
    keys_avail = in_data.keys()
    new_dict = dict()
    for key in keys_avail:
        if key in known_keys:
            if key == "record":
                new_pat.record = int(in_data[key])
            elif key == "name":
                new_pat.name = str(in_data[key])
        elif key in poss_keys:
            if key == "medical_image":
                new_dict[key] = in_data[key]
            elif key == "ecg_image":
                new_dict[key] = in_data[key]
            elif key == "heart_rate":
                new_dict[key] = float(in_data[key])
            elif key == "timestamp":
                new_dict[key] = in_data[key]
    if 'ecg_image' in keys_avail:
        if 'heart_rate' in keys_avail:
            new_dict['timestamp'] = datetime.now()
    if new_dict != dict():
        new_pat.data.append(new_dict)
        return new_pat.save(), "Patient Added to Database w/Files", 200
    return new_pat.save(), "Patient Added to Database", 200


def overall_dict_validation(in_data):
    """ Dictionary validation driver

    To validate each part of the dictionary,
    this function calls personalized data
    validation functions. If all pass,
    the correct status message/code are returned
    If not, whichever key fails triggers an
    appropriate status code/message return

    Args:
        in_data (dict): Dictionary of patient data

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    known_keys = in_data.keys()
    err1, code1 = val_keys(in_data)
    if code1 == 400:
        return err1, code1
    err2, code2 = val_record(in_data['record'])
    if code2 == 400:
        return err2, code2
    if 'name' in known_keys:
        err3, code3 = val_name(in_data['name'])
        if code3 == 400:
            return err3, code3
    if 'medical_image' in known_keys:
        err4, code4 = val_image(in_data['medical_image'])
        if code4 == 400:
            return err4, code4
    if 'ecg_image' in known_keys:
        err5, code5 = val_image(in_data['ecg_image'])
        if code5 == 400:
            return err5, code5
    if 'heart_rate' in known_keys:
        err6, code6 = val_hr(in_data['heart_rate'])
        if code6 == 400:
            return err6, code6
    if 'timestamp' in known_keys:
        err7, code7 = val_ts(in_data['timestamp'])
        if code7 == 400:
            return err7, code7
    return "Dictionary is valid", 200


def val_keys(in_dict):
    """ Validation of keys

    Before anything else, we validate that
    the dictionary sent contains only keys
    we expect. This function takes the
    patient dictionary and checks each key
    to see if it belongs

    Args:
        in_data (dict): Dictionary of patient data

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    accepted_keys = ['record', 'name', 'medical_image',
                     'ecg_image', 'heart_rate', 'timestamp']
    print(in_dict.keys)
    if 'record' not in in_dict.keys():
        return "Dict doesn't have record number", 400
    for key in in_dict.keys():
        if key not in accepted_keys:
            return "Unacceptable key in dict", 400
    return "Dict is acceptable", 200


def val_record(v_record):
    """ Validate medical record number

    We expect an image or numerical string.
    This function checks to see if this is
    true and returns the appropirate message
    status and code based on this.

    Args:
        v_record (int/str): Medical record number

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    if v_record.isnumeric():
        temp_rec = int(v_record)
        if temp_rec < 0:
            return "Record number shouldn't be negative", 400
        else:
            return temp_rec, 200
    else:
        return "Couldn't convert record number into int", 400


def val_name(v_name):
    """ Validate patient name

    We expect an string of a patient's name.
    This function checks to see if this is
    true and returns the appropirate message
    status and code based on this.

    Args:
        v_name (str): Patient name

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    if v_name.isalpha():
        return str(v_name), 200
    elif " " in v_name:
        temp1 = v_name.split()
        if temp1[0].isalpha() and temp1[1].isalpha():
            return str(v_name), 200
        else:
            return "Name is not of type string", 400
    else:
        return "Name is not of type string", 400
    # try:
    #     temp_name = str(v_name)
    #     return temp_name, 200
    # except ValueError:
    #     return "Name is not of type string", 400


def val_hr(v_hr):
    """ Validate heart rate

    We expect a float of a heart beat.
    This function checks to see if this is
    true and returns the appropirate message
    status and code based on this.

    Args:
        v_hr (float): Heart Rate

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    temp_hr = 0
    try:
        temp_hr = float(v_hr)
        if temp_hr < 0:
            return "Invalid heart rate value", 400
        else:
            return temp_hr, 200
    except ValueError:
        return "Couldn't convert heart rate into int", 400


def val_ts(v_ts):
    """ Validate timestamp

    We expect an appropriately formatted timestamp.
    This function checks to see if this is
    true and returns the appropirate message
    status and code based on this.

    Args:
        v_ts (str): Timestamp

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    try:
        datetime.strptime(v_ts, "%Y-%m-%d %H:%M:%S")
        return "Timestamp is valid", 200
    except ValueError:
        return "incorrect timestamp formatting", 400


def val_image(v_image):
    """ Validate image encoding

    We expect a base64 string of an image.
    This function checks to see if this is
    true by attempting to decode the image
    and returns the appropirate message
    status and code based on this.

    Args:
        v_image (str): Base64 string of image

    Returns:
        status_msg (str): Status message of validation
        status_code (int): Status code of validation

    """
    try:
        base64.b64decode(v_image, validate=True)
        return "Image string is valid", 200
    except binascii.Error:
        return "Image not in base64", 400


def get_id_list_from_db():
    """Gets a list of all available medical record numbers in the database

    This function accesses the MongoDB and collects the record numbers
    into a list so that they may be seen in the monitoring GUI

    Returns:
        record_num_list (str): list of all medical record numbers

    """
    record_num_list = []
    all_patients = Patient.objects.raw({})
    print(all_patients)
    for patient in all_patients:
        record_num_list.append(patient.record)

    if not record_num_list:
        return "No patients in DB", 400

    return record_num_list, 200


def get_patient_name_from_db(record_num_string):
    """Gets a patient's name from db given the MRN

    This function accesses the MongoDB and collects a patient's
    name based on the MRN given

    Args:
        record_num_string (str): MRN for selected patient

    Returns:
        selected_name (str): name of the patient
        or error message
    """

    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()
        selected_name = patient.name

        if selected_name is None:
            return "NO NAME", 200
        return selected_name, 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_patient_hr_from_db(record_num_string):
    """Gets a patient's heartrate from db given the MRN

    This function accesses the MongoDB and collects a patient's
    most recent heartrate based on the MRN given

    Args:
        record_num_string (str): MRN for selected patient
    Returns:
        selected_hr (int, str): heartrate of the patient
        or error message
    """

    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()
        length_data = len(patient.data)
        found_HR = False
        index = length_data-1
        while not found_HR and index >= 0:
            try:
                selected_hr = patient.data[index]["heart_rate"]
                found_HR = True
            except KeyError:
                index = index - 1
        if found_HR is False:
            return "NO HEARTRATE", 200
        else:
            return selected_hr, 200
    except KeyError:
        return "NO HEARTRATE", 200
    except IndexError:
        return "NO HEARTRATE", 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_patient_timestamp_from_db(record_num_string):
    """Gets a patient's heartrate timestamp from db given the MRN

    This function accesses the MongoDB and collects a patient's
    most recent heartrate timestamp based on the MRN given

    Args:
        record_num_string (str): MRN for selected patient
    Returns:
        selected_timestamp (int, str): heartrate of the patient
        or error message
    """

    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()
        length_data = len(patient.data)
        found_timestamp = False
        index = length_data - 1
        while not found_timestamp and index >= 0:
            try:
                selected_timestamp = patient.data[index]["timestamp"]
                found_timestamp = True
            except KeyError:
                index = index - 1
        if found_timestamp is False:
            return "NO TIMESTAMP", 200
        else:
            return selected_timestamp, 200
    except KeyError:
        return "NO TIMESTAMP", 200
    except IndexError:
        return "NO TIMESTAMP", 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_patient_ecg_from_db(record_num_string):
    """Gets a patient's most recent ECG from db given the MRN

    This function accesses the MongoDB and collects a patient's
    most recent ECG based on the MRN given

    Args:
        record_num_string (str): MRN for selected patient
    Returns:
        selected_timestamp (int, str): heartrate of the patient
        or error message
    """
    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()
        length_data = len(patient.data)
        found_ecg = False
        index = length_data - 1
        while not found_ecg and index >= 0:
            try:
                selected_ecg = patient.data[index]["ecg_image"]
                found_ecg = True
            except KeyError:
                index = index - 1
        if found_ecg is False:
            return "NO ECG IMAGE", 200
        else:
            return selected_ecg, 200
    except KeyError:
        return "NO ECG IMAGE", 200
    except IndexError:
        return "NO ECG IMAGE", 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_ecg_list_from_db(record_num_string):
    """Gets a list of all available medical record numbers in the database

        This function accesses the MongoDB and collects the record numbers
        into a list so that they may be seen in the monitoring GUI

        Args:
            record_num_string (str): MRN for selected patient

        Returns:
            record_num_list (str): list of all medical record numbers

    """
    list_ecg_dicts = []
    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()
        for index, current_data in enumerate(patient.data):
            try:
                ecg_dict = {"timestamp": current_data["timestamp"],
                            "ecg_image": current_data["ecg_image"]}
                list_ecg_dicts.append(ecg_dict)
            except KeyError:
                pass
        return list_ecg_dicts, 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_med_list_from_db(record_num_string):
    """Gets a list of all available medical images of a patient

        This function accesses the MongoDB and collects the record numbers
        into a list so that they may be seen in the monitoring GUI

        Args:
            record_num_string (str): MRN for selected patient

        Returns:
            record_num_list (str): list of all medical record numbers

    """
    list_med_images = []
    try:
        record_num = int(record_num_string)
        patient = Patient.objects.raw({"_id": record_num}).first()

        for current_data in patient.data:
            try:
                current_medical_image = current_data["medical_image"]
                list_med_images.append(current_medical_image)
            except KeyError:
                pass
        return list_med_images, 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return 'Medical record not of type int', 400


def get_pat_record_numbers():
    """collects patient medical record numbers from database

    This function accesses the MongoDB and collects the medical record numbers
    patients
    """
    patient_list = []
    for patient in Patient.objects.raw({}):
        patient_list.append(patient.record)
        print(patient_list)

    if not patient_list:
        return "No patient in DB", 400
    return patient_list, 200


def get_patient_dict(patient_id):
    """Gets a dictionary for each patient containing
    patient stats from db given the MRN

    This function accesses the MongoDB and collects the inputted patient
    information as a dictionary based on the MRN given

    Args:
        patient_id (str): MRN for selected patient

    Returns:
        single_patient_dict (dict): dictionary containing inputted patient info
        or error message
    """
    try:
        patient_id = int(patient_id)
        single_patient = Patient.objects.raw({"_id": patient_id}).first()
        print(single_patient)
        single_patient_dict = single_patient.data[-1]
        print(single_patient_dict)
        return single_patient_dict, 200
    except pymodm_errors.DoesNotExist:
        return "A patient with that MRN does not exist", 400
    except ValueError:
        return "Medical record not of type int", 400
