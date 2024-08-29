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
        """

        data = {
            'data': payload,
            'format': req_format,
            'headers': self.headers
        }
        response = self.client.post(url, **data)
        self.assertEqual(response.status_code, status_code)
        return response

    def _test_get(
            self, url, queryset=None, pagination=False, status_code=status.HTTP_200_OK, **kwargs):
        """ Test get request
            params:
                url: url to test
                queryset: if queryset - will assert response.data with queryset.count()
                pagination: if pagination
                    provide result and count keys names in kwargs
                    kwargs['results'] = 'results'
                    try to get data from response.data[kwargs['results']]
                    try to get count from response.data[kwargs['count']]

        """

        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            data = response.data
            count = None
            if pagination:
                results = kwargs.get('results', 'results')
                count = kwargs.get('results', 'count')
                try:
                    data = response.data[results]
                    count = response.data[count]
                except KeyError:
                    return

            if queryset is not None:
                self.assertEqual(len(data), queryset.count())
                if count:
                    self.assertEqual(count, queryset.count())
            else:
                self.assertTrue(len(data) > 0)
        return response

    def _test_delete(self, url, queryset=None, code=status.HTTP_204_NO_CONTENT):
        """ Test delete request
            assert status code
            assert not queryset.exists() if queryset is not None
        """
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, code)
        if queryset:
            self.assertFalse(queryset.exists())
        return response