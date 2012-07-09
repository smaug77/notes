pep8 core
pylint core
coverage run manage.py test core
coverage report --show-missing --include="core/*"
