import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_bed_view():
    client = Client()
    url = reverse("beds:bed-list")  # /bed
    response = client.get(url)
    assert response.status_code == 200
