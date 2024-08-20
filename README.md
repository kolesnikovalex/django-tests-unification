# django-tests-unification
this package allow to using method:
- _test_create
- _test_get
- _test_update
- _test_delete

All methods return response object from Client.request method


## Requirements
- python = "^3.10"
- django = "5.0.4"
- djangorestframework = "^3.15.1"


## _test_create
-make post request to self.client
- assert ststus_code
