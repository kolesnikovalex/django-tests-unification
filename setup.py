from setuptools import setup, find_packages

setup(
    name='django_tests_unification',
    version='0.1.0',
    author='Aleksandr',
    author_email='kolesnikov.alex.nik@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url='https://github.com/kolesnikovalex/django-tests-unification/',
    license='GNU General Public License (GPL)',
    description='Packages for unification django tests process',
    long_description='Packages for unification django tests process',
    install_requires=[
        "Django>=5.0.2",
        "djangorestframework>=3.15.1",
    ],
)
