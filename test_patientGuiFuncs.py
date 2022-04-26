import pytest
from patientGuiFuncs import *


@pytest.mark.parametrize('record, name,'
                         'medical_image, ecg_image,'
                         'heart_rate, dict', [

                             ('0194', "Tony Stark",
                              None, None, None, {'record': '0194',
                                                 'name': "Tony Stark"}),

                             ('4444', "NickFury",
                              "9/582745", '104594717', 74.2,
                              {'record': '4444', 'name': "NickFury",
                               'medical_image': "9/582745",
                               'ecg_image': '104594717',
                               'heart_rate': 74.2}),


                             ('1010', None, 'gibberish_string',
                              None, None,
                              {'record': '1010',
                               'medical_image': 'gibberish_string'})


                          ])
def test_package_int_dict(record, name,
                          medical_image, ecg_image,
                          heart_rate, dict):

    expec_dict = package_into_dict(record, name,
                                   medical_image, ecg_image,
                                   heart_rate)
    assert expec_dict == dict


def test_convert_image_to_str():
    b64str = convert_image_to_str("images/acl1.jpg")
    assert b64str[0:20] == "/9j/4AAQSkZJRgABAgAA"


@pytest.mark.parametrize('non_str, expec', [

    (19492, '19492'),
    (75.2, '75.2'),
    ("string", "string")

])
def test_convert_to_str(non_str, expec):
    test_str = convert_to_str(non_str)
    assert test_str == expec
