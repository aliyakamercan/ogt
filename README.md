```
git clone ....
cd ogt
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
source venv/bin/activate
python manage.py runserver
```

make sure to add
```
127.0.0.1  ogt.dev broken.ogt.dev pink.ogt.dev def.ogt.dev
```
to your /etc/hosts file


superuser is su/su

TODO:

remove items from inventory upon orders
write tests
