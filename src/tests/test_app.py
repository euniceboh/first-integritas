from src import app as flask_app
import json
import pytest

@pytest.fixture
def app():
    return flask_app.app

# Will do most of the route (only 2) testing as Unit Testing 
def test_catchall_route(app):
    client = app.test_client()
    url = '/any/other/route'
    response = client.get(url)
    assert response.status_code == 200

def test_oaschecker_route(app):
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200

def test_swaggeruipreview_route(app):
    client = app.test_client()
    url = '/swaggeruipreview'
    response = client.get(url)
    assert response.status_code == 200

def test_openapi():
    assert flask_app.checkOpenapi("3.0.0") == True

def test_title():
    assert flask_app.checkTitle("Update Crediting Status of 55 WDL Application PayNow") == True

# def test_post_route__failure__bad_request():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url = '/post/test'

#     mock_request_headers = {
#         'authorization-sha256': '123'
#     }

#     mock_request_data = {}

#     response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
#     assert response.status_code == 400