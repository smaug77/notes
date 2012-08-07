python manage.py dumpdata core --format=yaml> temp.yaml
git add temp.yaml
git commit -m 'uploading to heroku'
git push heroku
heroku run python manage.py reset core
heroku run python manage.py loaddata temp.yaml
