# White Box Functional Testing

from src import app as flask_app
import json
import pytest

@pytest.fixture
def app():
    return flask_app.app

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

def test_openapi_unsuccessful():
    assert flask_app.checkOpenapi("") == False
    assert flask_app.checkOpenapi(None) == False

def test_title():
    assert flask_app.checkTitle("Update Crediting Status of 55 WDL Application PayNow") == True

