from rest_framework import status
from rest_framework.test import APITestCase
import datetime


class TestClientMixin(APITestCase):
    date_format = '%Y-%m-%d'
    headers = None

    def _test_create(
            self, url: str, payload: dict, req_format=None, status_code=status.HTTP_201_CREATED):
        """ Test post request
            format: json, multipart, etc
            headers: your http headers
        """

        data = {
            'data': payload,
            'format': req_format,
            'headers': self.headers
        }
        response = self.client.post(url, **data)
        self.assertEqual(response.status_code, status_code)
        return response
