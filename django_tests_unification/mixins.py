import json

from rest_framework import status
from rest_framework.test import APITestCase
import datetime


class TestClientMixin(APITestCase):
    date_format = '%Y-%m-%d'
    headers = None

    def __check_attr(self, obj, k, v):
        attr = getattr(obj, k)
        if isinstance(attr, datetime.date):
            attr = attr.strftime(self.date_format)
        self.assertEqual(v, attr)

    def _test_create(
            self, url: str, payload: dict, req_format='json', status_code=status.HTTP_201_CREATED):
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

    def _test_update(self, url: str, payload: str, queryset, method='patch'):
        """
        Test update request
        allows only PATCH and PUT methods
        payload = json.dumps(dict_obj)
        assert status code
        if queryset is not None - try to check that instance attribute was change
        """

        if method not in ('patch', 'put'):
            raise ValueError('method must be "patch" or "put"')

        if method == 'put':
            response = self.client.put(url, headers=self.headers, data=payload)
        else:
            response = self.client.patch(url, headers=self.headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if queryset:
            obj = queryset.first()

            payload = json.loads(payload)

            for k, v in payload.items():
                try:
                    atr = getattr(obj._meta.model, k)
                    related_model = getattr(atr.field, 'related_model', None)
                    if related_model and isinstance(v, dict):
                        related_obj = related_model.objects.filter(
                            id=getattr(obj, atr.field.attname)
                        ).first()

                        self.assertIsNotNone(related_obj)

                        for rel_k, rel_v in v.items():
                            self.__check_attr(related_obj, rel_k, rel_v)
                    else:
                        self.__check_attr(obj, k, v)

                except AttributeError:
                    continue
        return response
