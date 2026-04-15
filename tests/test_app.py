import pytest
import sys
import os

# Agregamos la ruta de la aplicación al path para poder importarla
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Prueba que el endpoint principal responde correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hola desde Flask en Docker' in response.data