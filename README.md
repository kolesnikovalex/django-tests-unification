# django-tests-unification
this package allow to using method:
- _test_create
- _test_get
- _test_update
- _test_delete

All methods return response object from Client.request method


## Requirements
- Django
- djangorestframework


## _test_create
-make post request to self.client
- assert ststus_code
