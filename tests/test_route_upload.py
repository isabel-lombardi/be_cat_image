from flask import json
from time import sleep

from cat_image.main import app
from tests.data.images_data import golden_retriver_base64, bmp_image

dict_OK = {'1': golden_retriver_base64, '2': golden_retriver_base64}
dict_NOK = {'1': 'this_is_not_an_image_file'}
dict_NOK2 = {'1': bmp_image}


def test_route_upload():
    response = app.test_client().post(
        '/upload',
        data=json.dumps(dict_OK),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    print(response)
    assert response.status_code == 200  # <<<***
    # assert data['message'] == "OK"      # <<<***
    assert data['status'] == "OK"
    assert data['result']['1'][0][0] == "golden retriever"
    assert data['result']['1'][0][1] == 44.376583099365234  # 43.70540237426758
    assert data['result']['2'][0][0] == "golden retriever"
    assert data['result']['2'][0][1] == 44.376583099365234  # 43.70540237426758
    # { '1': [['golden retriever', 43.70540237426758]] }


def test_route_upload_bad_format():
    response = app.test_client().post(
        '/upload',
        data=json.dumps(dict_NOK),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data['status'] == "error"
    assert data['message'] == 'Decoding failed'
    assert data['wrong_images_id'] == ['1']


def test_route_upload_bmp_format():
    # sleep(10.5)
    response = app.test_client().post(
        '/upload',
        data=json.dumps(dict_NOK2),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data['status'] == "error"
    assert data['message'] == 'Incorrect images format'
    assert data['wrong_images_id'] == ['1']
