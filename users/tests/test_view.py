import pytest


@pytest.mark.django_db
def test_Getall(client):
    response = client.get('/users/')
    assert response.status_code == 200
