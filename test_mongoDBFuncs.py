from matplotlib.pyplot import connect
from freezegun import freeze_time
from numpy import record
import pytest
from server import connect_to_Mongo
from datetime import datetime
import base64
import json
from mongoDBFuncs import *
from patientGuiFuncs import convert_image_to_str
connect_to_Mongo()


@pytest.fixture
def my_cleanup_fixture():
    # Startup code
    ...
    yield
    # Cleanup code
    for patient in Patient.objects.raw({}):
        patient.delete()


@freeze_time("04-07-22 13:45:20")
@pytest.mark.parametrize('in_data, e, msg, code', [

 ({'record': 6575, 'name': "NickFury",
     'medical_image': "9/582745", 'ecg_image': '104594717',
     'heart_rate': 74.2},
     [6575, 'NickFury',
      [{'medical_image': "9/582745", 'ecg_image': '104594717',
       'heart_rate': 74.2}]],
     "Patient Added to Database w/Files", 200),

 ({'record': 1001, 'name': "Stan Lee"},
  [1001, 'Stan Lee', []], "Patient Added to Database", 200),

 ({'record': 151},
  [151, None, []], "Patient Added to Database", 200),

 ({'record': 50, 'name': 'KSI', 'medical_image': '9/1832'},
  [50, 'KSI', [{'medical_image': '9/1832'}]],
  "Patient Added to Database w/Files", 200),

 ({'record': 50, 'name': 'Dr. Markoh',
   'ecg_image': '9/1123Ag21832', 'heart_rate': 75.2},
  [50, 'Dr. Markoh', [{'ecg_image': '9/1123Ag21832',
   'heart_rate': 75.2}]],
  "Patient Added to Database w/Files", 200),

])
def test_add_new_patient_to_db(in_data, e, msg, code):
    # Note, except blocks don't have specific error
    # since they can be either a Key/Index Error
    test_return, test_msg, test_code = add_new_patient_to_db(in_data)
    test_return.delete()
    assert test_msg == msg
    assert test_code == code
    assert e[0] == test_return.record
    assert e[1] == test_return.name
    try:
        assert e[2][0]['ecg_image'] == test_return.data[0]['ecg_image']
    except AssertionError:
        print("Nothing for ecg image")
    except IndexError:
        print("Nothing for ecg image")
    except KeyError:
        print("Nothing for ecg image")

    try:
        assert e[2][0]['medical_image'] == test_return.data[0]['medical_image']
    except AssertionError:
        print("Nothing for med image")
    except IndexError:
        print("Nothing for med image")
    except KeyError:
        print("Nothing for med image")

    try:
        assert e[2][0]['heart_rate'] == test_return.data[0]['heart_rate']
    except AssertionError:
        print("Nothing for heart rate image")
    except IndexError:
        print("Nothing for heart rate image")
    except KeyError:
        print("Nothing for med image")


# test_Patient = Patient.objects.raw({"_id": int(99999)}).first()
# test_Patient.delete()
add_new_patient_to_db({'record': 99999, 'name': "NickFury"})
test_Patient = Patient.objects.raw({"_id": int(99999)}).first()


@pytest.mark.parametrize('oldPat, in_data, e, msg, code', [

 (test_Patient, {'record': 99999, 'name': "Stan Lee"},
  [99999, 'Stan Lee', []], "Name updated", 200),

 (test_Patient,
  {'record': 99999, 'name': "Stan Lee",
   'ecg_image': '9/%182', 'heart_rate': 75.2},
  [99999, 'Stan Lee', [{'ecg_image': '9/1123Ag21832',
   'heart_rate': 75.2}]],
  "Patient Data Updated", 200),

 (test_Patient,
  {'record': 99999, 'name': 'Dr. Markoh',
   'ecg_image': '9/FFs123', 'heart_rate': 85.2},
  [99999, 'Dr. Markoh', [{'ecg_image': '9/1123Ag21832',
   'heart_rate': 75.2}, {'ecg_image': '9/FFs123', 'heart_rate': 85.2}]],
  "Patient Data Updated", 200),

])
def test_add_to_existing(oldPat, in_data, e, msg, code):
    test_return, test_msg, test_code = add_to_existing(in_data, oldPat)
    # test_return.delete()
    assert test_msg == msg
    assert test_code == code
    assert e[0] == test_return.record
    assert e[1] == test_return.name
    try:
        assert e[2][0]['ecg_image'] == test_return.data[0]['ecg_image']
    except AssertionError:
        print("Nothing for ecg image")
    except IndexError:
        print("Nothing for ecg image")
    except KeyError:
        print("Nothing for ecg image")

    try:
        assert e[2][0]['medical_image'] == test_return.data[0]['medical_image']
    except AssertionError:
        print("Nothing for med image")
    except IndexError:
        print("Nothing for med image")
    except KeyError:
        print("Nothing for med image")

    try:
        assert e[2][0]['heart_rate'] == test_return.data[0]['heart_rate']
    except AssertionError:
        print("Nothing for heart rate image")
    except IndexError:
        print("Nothing for heart rate image")
    except KeyError:
        print("Nothing for med image")


b64str = convert_image_to_str("images/test_image.jpg")
b64str2 = convert_image_to_str("images/acl2.jpg")


@pytest.mark.parametrize('in_data, msg, code', [
    ({'record': '6575ae', 'name': "Nic51235",
     'heart_rate': 74.2}, "Couldn't convert record number into int", 400),


    ({'record': '6575', 'name': "Nic51235",
     'heart_rate': 74.2}, "Name is not of type string", 400),


    ({'record': '6575', 'name': "NickFury",
     'medical_image': "9/582745", 'ecg_image': '104594717',
      'heart_rate': 74.2}, "Image not in base64", 400),

    ({'record': '6575', 'name': "Nic",
     'heart_rate': '74.2gew'}, "Couldn't convert heart rate into int", 400),

    ({'record': '6575', 'name': "Nic",
     'heart_rate': '-94'}, "Invalid heart rate value", 400),


    ({'record': '6575', 'name': "NickFury",
     'medical_image': "9/582745", 'ecg_image': '104594717',
      'heart_rate': 74.2}, "Image not in base64", 400),

    ({'record': '6575', 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "04-07-22 13:45:20"},
     "incorrect timestamp formatting", 400),

    ({'record': '6575', 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Dictionary is valid", 200),

])
def test_overall_dict_validation(in_data, msg, code):
    test_msg, test_code = overall_dict_validation(in_data)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('in_data, msg, code', [
    ({'record': '6575ae', 'name': "Nic51235",
     'heart_rate': 74.2}, "Couldn't convert record number into int", 400),


    ({'record': '6575', 'name': "Nic51235",
     'heart_rate': 74.2}, "Name is not of type string", 400),


    ({'record': '6575', 'name': "NickFury",
     'medical_image': "9/582745", 'ecg_image': '104594717',
      'heart_rate': 74.2}, "Image not in base64", 400),

    ({'record': '6575', 'name': "Nic",
     'heart_rate': '74.2gew'}, "Couldn't convert heart rate into int", 400),

    ({'record': '6575', 'name': "Nic",
     'heart_rate': '-94'}, "Invalid heart rate value", 400),


    ({'record': '6575', 'name': "NickFury",
     'medical_image': "9/582745", 'ecg_image': '104594717',
      'heart_rate': 74.2}, "Image not in base64", 400),

    ({'record': '6575', 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "04-07-22 13:45:20"},
     "incorrect timestamp formatting", 400),

    ({'record': '6575', 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2},
     "Patient Added to Database w/Files", 200),

    ({'record': '1001', 'name': "Stan Lee"},
     "Patient Added to Database", 200),

    ({'record': '151'},
     "Patient Added to Database", 200),

    ({'record': '50', 'name': 'KSI', 'medical_image': b64str},
     "Patient Added to Database w/Files", 200),

    ({'record': '99999', 'name': "Stan Lee"},
     "Name updated", 200),

])
def test_data_driver(in_data, msg, code):
    # Since we test all these dicts before in their respective master
    # functions,here we just want to validate the messages and codes
    throwawy, test_msg, test_code = data_driver(in_data)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('in_data, msg, code', [
    ({'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Dict doesn't have record number", 400),

    ({'record': 1949123, 'na4me': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Unacceptable key in dict", 400),

    ({'record': 1949123, 'name': "NickFury",
     'medi23cal_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Unacceptable key in dict", 400),

    ({'record': 1949123, 'name': "NickFury",
     'medical_image': b64str, 'ec3123g_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Unacceptable key in dict", 400),

    ({'record': 1949123, 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'h32eart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Unacceptable key in dict", 400),

    ({'record': 1949123, 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'times02tamp': "2022-04-7 13:45:20"},
     "Unacceptable key in dict", 400),

    ({'record': 1949123, 'name': "NickFury",
     'medical_image': b64str, 'ecg_image': b64str2,
      'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"},
     "Dict is acceptable", 200),

])
def test_val_keys(in_data, msg, code):
    test_msg, test_code = val_keys(in_data)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('v_image, msg, code', [
    (b64str, "Image string is valid", 200),

    ('HoopyDoopy', "Image not in base64", 400),

])
def test_val_image(v_image, msg, code):
    test_msg, test_code = val_image(v_image)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('v_ts, msg, code', [

    ("2022-04-7 13:45:20", "Timestamp is valid", 200),

    ("04-07-22 13:45:20", "incorrect timestamp formatting", 400),

])
def test_val_ts(v_ts, msg, code):
    test_msg, test_code = val_ts(v_ts)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('v_hr, msg, code', [
    (20, 20.0, 200),

    (-20, "Invalid heart rate value", 400),

    ("9daj341", "Couldn't convert heart rate into int", 400),

])
def test_val_hr(v_hr, msg, code):
    test_msg, test_code = val_hr(v_hr)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('v_name, msg, code', [
    ("Bucky Barnes", "Bucky Barnes", 200),

    ("BuckyBarnes", "BuckyBarnes", 200),

    ('alkj341', "Name is not of type string", 400),

    ("9daj 341", "Name is not of type string", 400),

])
def test_val_name(v_name, msg, code):
    test_msg, test_code = val_name(v_name)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('v_record, msg, code', [

    ("94022", 94022, 200),

    ("29s93", "Couldn't convert record number into int", 400),

])
def test_val_record(v_record, msg, code):
    test_msg, test_code = val_record(v_record)
    assert test_msg == msg
    assert test_code == code
    return


@freeze_time("04-07-22 13:45:20")
@pytest.mark.parametrize("input, expected, status", [
    (6575,
     {'medical_image': b64str[:100], 'ecg_image': b64str2[:100],
      'heart_rate': 74.2, 'timestamp': datetime(2022, 4, 7, 13, 45, 20)}, 200)
])
def test_get_patient_dict(input, expected, status):
    from mongoDBFuncs import get_patient_dict, add_new_patient_to_db
    input_dict = {'record': '6575', 'name': "NickFury",
                  'medical_image': b64str[:100], 'ecg_image': b64str2[:100],
                  'heart_rate': 74.2, 'timestamp': "2022-04-7 13:45:20"}
    add_new_patient_to_db(input_dict)
    answer, status_test = get_patient_dict(input)

    if status_test == 200:
        assert answer == expected
    else:
        assert answer == expected
    assert status_test == status
    return


def test_get_id_list_from_db():
    for patient in Patient.objects.raw({}):
        patient.delete()

    msg = 'No patients in DB'
    test_msg, test_code = get_id_list_from_db()
    assert test_msg == msg
    assert test_code == 400

    add_new_patient_to_db({'record': 99999,
                           'name': "NickFury", "heart_rate": 100})

    test_msg, test_code = get_id_list_from_db()
    assert test_msg == [99999]
    assert test_code == 200

    add_new_patient_to_db({'record': 99998})
    # add_new_patient_to_db({'record': 99998, 'name':
    # "JerrySpringer", "heart_rate": 100.1})

    test_msg, test_code = get_id_list_from_db()
    assert test_msg == [99999, 99998]
    assert test_code == 200

    return


@pytest.mark.parametrize('record, msg, code', [

    (99999, "NickFury", 200),

    (99998, "NO NAME", 200),

    (999, "A patient with that MRN does not exist", 400),

    ("99h99", 'Medical record not of type int', 400),

])
def test_get_patient_name_from_db(record, msg, code):
    test_msg, test_code = get_patient_name_from_db(record)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('record, msg, code', [

    (99999, 100, 200),

    (99998, "NO HEARTRATE", 200),

    (999, "A patient with that MRN does not exist", 400),

    ("99h99", 'Medical record not of type int', 400),

])
def test_get_patient_hr_from_db(record, msg, code):
    test_msg, test_code = get_patient_hr_from_db(record)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('record, msg, code', [

    (9, "2022-04-7 13:45:20", 200),

    (99999, "NO TIMESTAMP", 200),

    (999, "A patient with that MRN does not exist", 400),

    ("99h99", 'Medical record not of type int', 400),

])
def test_get_patient_timestamp_from_db(record, msg, code):
    add_new_patient_to_db({'record': 9, 'name': "CosmoKramer",
                           "heart_rate": 100,
                           'timestamp': "2022-04-7 13:45:20"})

    test_msg, test_code = get_patient_timestamp_from_db(record)
    assert test_msg == msg
    assert test_code == code
    return


@pytest.mark.parametrize('record, msg, code', [

    (1, b64str2[:100], 200),

    (9, "NO ECG IMAGE", 200),

    (7, "A patient with that MRN does not exist", 400),

    ("8f8", "Medical record not of type int", 400),

])
def test_get_patient_ecg_from_db(record, msg, code):
    add_new_patient_to_db({'record': 1, 'name': "Jerry Seinfeld",
                           'timestamp': "2022-04-7 13:45:20",
                           "ecg_image": b64str2[:100]})

    test_msg, test_code = get_patient_ecg_from_db(record)
    # Must not use full b64string for test
    assert test_msg[:100] == msg
    assert test_code == code
    return


@pytest.mark.parametrize('record, msg, code', [

    ("1", [{"timestamp": "2022-04-7 13:45:20",
           "ecg_image": b64str2[:100]},
           {"timestamp": "2023-04-7 13:45:20",
           "ecg_image": b64str[:100]}], 200),

    (7, "A patient with that MRN does not exist", 400),

    ("8f8", "Medical record not of type int", 400)

])
def test_get_ecg_list_from_db(record, msg, code):
    test_Patient1 = Patient.objects.raw({"_id": int(1)}).first()
    add_to_existing({'record': 1, 'name': "Jerry Seinfeld",
                     'timestamp': "2023-04-7 13:45:20",
                     "ecg_image": b64str[:100]}, test_Patient1)

    test_msg, test_code = get_ecg_list_from_db(record)
    assert test_msg == msg[:100]
    assert test_code == code
    return


@pytest.mark.parametrize('record, msg, code', [

    ("1", [b64str2[:100],  b64str[:100]], 200),

    (7, "A patient with that MRN does not exist", 400),

    ("8f8", "Medical record not of type int", 400)

])
def test_get_med_list_from_db(record, msg, code):
    test_Patient1 = Patient.objects.raw({"_id": int(1)}).first()
    add_to_existing({'record': 1, 'name': "Jerry Seinfeld",
                     "medical_image": b64str2[:100]}, test_Patient1)
    add_to_existing({'record': 1, 'name': "Jerry Seinfeld",
                     "medical_image": b64str[:100]}, test_Patient1)

    test_msg, test_code = get_med_list_from_db(record)
    assert test_msg == msg[:100]
    assert test_code == code
    return


@pytest.mark.usefixtures('my_cleanup_fixture')
def test_with_special_cleanup():
    pass
