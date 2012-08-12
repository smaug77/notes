heroku run python manage.py dumpdata core --natural --indent 2 --format=yaml > temp.yaml
echo "this probably won't work because you need to remove the first line of temp.json"
python manage.py reset core
python manage.py loaddata temp.json
