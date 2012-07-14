python manage.py dumpdata core > temp.json
git add temp.json
git commit -m 'uploading to heroku'
git push heroku
heroku run python manage.py reset core
heroku run python manage.py loaddata temp.json
