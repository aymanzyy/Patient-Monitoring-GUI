import pytest
from monitoringGuiFuncs import *
from mongoDBFuncs import add_new_patient_to_db, add_to_existing
from patientGuiFuncs import convert_image_to_str
from patient import Patient
from server import connect_to_Mongo
# connect_to_Mongo()

b64str = convert_image_to_str("images/test_image.jpg")
test_ndArray = convert_string_to_ndarray(b64str)

'''
ALL OF THE BELOW FUNCTION DO NOT ACTUALLY NEED TO BE
TESTED BECAUSE THEY HAVE SERVER FUNCTIONALITY AND
CANNOT BE RELIED UPON FOR TESTING


b64str2 = convert_image_to_str("images/acl2.jpg")



for patient in Patient.objects.raw({}):
    patient.delete()

add_new_patient_to_db({'record': 1, 'name': "Jerry Seinfeld",
                       'heartrate': 75,
                       'timestamp': "2022-04-7 13:45:20",
                       "ecg_image": "imgstring1"})
add_new_patient_to_db({'record': 2, 'name': "George",
                       'heartrate': 80,
                       'timestamp': "2023-04-7 13:45:20",
                       "ecg_image": "imgstring2"})
add_new_patient_to_db({'record': 3,
                       'name': "NickFury", "heart_rate": 100})
test_Patient1 = Patient.objects.raw({"_id": int(1)}).first()
add_to_existing({'record': 1, 'name': "Jerry Seinfeld",
                 "medical_image": "medimgstring1"}, test_Patient1)


def test_get_patient_list_from_server():
    test_ndArray = convert_string_to_ndarray(b64str)

    for patient in Patient.objects.raw({}):
        patient.delete()

    add_new_patient_to_db({'record': 1, 'name': "Jerry Seinfeld",
                           'heartrate': 75,
                           'timestamp': "2022-04-7 13:45:20",
                           "ecg_image": "imgstring1"})
    add_new_patient_to_db({'record': 2, 'name': "George",
                           'heartrate': 80,
                           'timestamp': "2023-04-7 13:45:20",
                           "ecg_image": "imgstring2"})
    add_new_patient_to_db({'record': 3,
                           'name': "NickFury", "heart_rate": 100})
    test_Patient1 = Patient.objects.raw({"_id": int(1)}).first()
    add_to_existing({'record': 1, 'name': "Jerry Seinfeld",
                     "medical_image": "medimgstring1"}, test_Patient1)
    expected = "[1, 2, 3]"
    answer = get_patient_list_from_server()
    assert answer == expected


@pytest.mark.parametrize('record, msg', [

    ("1", '[{"ecg_image": "imgstring1", "timestamp": "2022-04-7 13:45:20"}]'),

    (2, '[{"ecg_image": "imgstring2", "timestamp": "2023-04-7 13:45:20"}]'),

    (7, '"A patient with that MRN does not exist"'),

    ("8f8", '"Medical record not of type int"')

])
def test_get_ecg_list_from_server(record, msg):
    test_msg = get_ecg_list_from_server(record)
    assert test_msg == msg
    return


@pytest.mark.parametrize('record, msg', [

    ("1", '["medimgstring1"]'),

    (2, '[]'),

    (7, '"A patient with that MRN does not exist"'),

    ("8f8", '"Medical record not of type int"')
])
def test_get_med_list_from_server(record, msg):
    test_msg = get_med_list_from_server(record)
    assert test_msg == msg
    return


@pytest.mark.parametrize('record, msg', [

    ("1", '"Jerry Seinfeld"\n'),

    (2, '"George"\n'),

    (7, '"A patient with that MRN does not exist"\n'),

    ("8f8", '"Medical record not of type int"\n')
])
def test_get_patient_name_from_server(record, msg):
    test_msg = get_patient_name_from_server(record)
    assert test_msg == msg
    return


@pytest.mark.parametrize('record, msg', [

    ("3", "100.0\n"),

    (7, '"A patient with that MRN does not exist"\n'),

    ("8f8", '"Medical record not of type int"\n')
])
def test_get_patient_hr_from_server(record, msg):
    test_msg = get_patient_hr_from_server(record)
    assert test_msg == msg
    return


@pytest.mark.parametrize('record, msg', [

    ("1", '"2022-04-7 13:45:20"\n'),

    (2, '"2023-04-7 13:45:20"\n'),

    (7, '"A patient with that MRN does not exist"\n'),

    ("8f8", '"Medical record not of type int"\n')
])
def test_get_patient_timestamp_from_server(record, msg):
    test_msg = get_patient_timestamp_from_server(record)
    assert test_msg == msg
    return


@pytest.mark.parametrize('record, msg, code', [

    ("1", "imgstring1", 200),

    (2, "imgstring2", 200),

    (7, "A patient with that MRN does not exist", 400),

    ("8f8", "Medical record not of type int", 400)
])
def test_get_patient_ecg_from_server(record, msg, code):
    test_msg, test_status = get_patient_ecg_from_server(record)
    assert test_msg == msg
    assert test_status == code
    return
'''


def test_convert_string_to_ndarray():
    ndArray = convert_string_to_ndarray(b64str)
    assert (ndArray[0][0:5] == test_ndArray[0][0:5]).all


def test_convert_string_to_file():
    import filecmp
    import os
    b64str4 = convert_image_to_str("images/test_image.jpg")
    convert_string_to_imgfile(b64str4, "test_image_output")
    date = datetime.datetime.now()
    now = date.strftime("_%Y-%m-%d_%H-%M-%S")
    base_name = "saved_images/test_image_output"
    test_file = base_name+now+".png"
    answer = filecmp.cmp(test_file,
                         "images/test_image.jpg")
    os.remove(test_file)
    assert answer is True


@pytest.mark.parametrize('test_dict_list, time_list, image_list', [

    ([{"ecg_image": "pickle", "timestamp": "date"}], ["date"], ["pickle"]),

    ([{"ecg_image": "pickle", "timestamp": "date"},
      {"ecg_image": "pickle1", "timestamp": "date1"}],
     ["date", "date1"], ["pickle", "pickle1"])

])
def test_get_list_of_times_and_images(test_dict_list, time_list, image_list):
    test_time, test_image = get_list_of_times_and_images(test_dict_list)
    assert test_time == time_list
    assert test_image == image_list


@pytest.mark.parametrize('length, name_list', [

    (1, ["image_no_0"]),

    (2, ["image_no_0", "image_no_1"]),

])
def test_create_image_names(length, name_list):
    test_list = create_image_names(length)
    assert test_list == name_list
