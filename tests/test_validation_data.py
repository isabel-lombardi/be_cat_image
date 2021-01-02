import os
from PIL import Image
# from string import ascii_letters, digits, punctuation

from cat_image.validation_data import ValidationData


def test_is_username_valid():
    good_password = 'Ab123@'
    assert ValidationData.is_username_valid({'username': 'admi', 'password': good_password})
    assert ValidationData.is_username_valid({'username': 'administra', 'password': good_password})
    assert ValidationData.is_username_valid({'username': 'adm@gmail.com', 'password': good_password})
    assert ValidationData.is_username_valid({'username': 'administra@gmail.com', 'password': good_password})
    assert ValidationData.is_username_valid({'username': 'giorgio@giorgiomontanini.info', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': 'a b c', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': 'a' * 2000 + '@gmail.com', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': '@administr', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': 'administr@', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': 'adm', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': '', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': '1234', 'password': good_password})
    assert not ValidationData.is_username_valid({'username': '++++', 'password': good_password})
    # punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    assert not ValidationData.is_username_valid({'username': r"""!"#$%&'()*+,-/:;<=>?[\]^`{|}~""",
                                                 'password': good_password})


def test_is_password_valid():
    good_username = 'ma.lasciatemi@libero.it'
    assert ValidationData.is_password_valid({'username': good_username, 'password': 'Ab123@'})
    assert not ValidationData.is_password_valid({'username': good_username, 'password': '12345'})
    assert not ValidationData.is_password_valid({'username': good_username, 'password': 'abcde'})
    assert not ValidationData.is_password_valid({'username': good_username, 'password': 'ABCDE'})
    assert not ValidationData.is_password_valid({'username': good_username, 'password': 'abcdeABCDE'})
    assert not ValidationData.is_password_valid({'username': good_username, 'password': ''})
    # less than min length
    # assert not ValidationData.is_password_valid({'username': good_username, 'password': 'Ab3@'})


def test_is_images_number_valid():
    assert ValidationData.is_images_number_valid({'1': '1'})
    assert ValidationData.is_images_number_valid(
        {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10'})
    assert not ValidationData.is_images_number_valid({})
    assert not ValidationData.is_images_number_valid(
        {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
         '11': '11'})


def test_images_format_validation():
    file_abs_path = os.path.abspath(os.path.dirname(__file__))
    file_data_path = os.path.join(file_abs_path, 'data')
    images_01_path = os.path.join(file_data_path, 'cucciolo3-800X400-800x400.jpg')
    images_02_path = os.path.join(file_data_path, 'cat_01.png')
    images_03_path = os.path.join(file_data_path, 'giu.bmp')

    img_dog = Image.open(images_01_path)
    img_cat = Image.open(images_02_path)
    bmp_img = Image.open(images_03_path)

    assert img_dog.format == 'JPEG'
    assert img_cat.format == 'PNG'
    assert bmp_img.format == 'BMP'

    assert ValidationData.images_format_validation({'1': img_dog}) == []
    assert ValidationData.images_format_validation({'1': img_dog, '2': img_cat}) == []
    assert ValidationData.images_format_validation({'1': img_dog, '2': bmp_img}) == ['2']
    assert ValidationData.images_format_validation(
        {'1': img_dog, '2': img_cat, '3': bmp_img, '4': img_dog, '5': img_cat, '6': bmp_img, '7': img_dog, '8': img_cat,
         '9': bmp_img, '10': img_dog}) == ['3', '6', '9']
