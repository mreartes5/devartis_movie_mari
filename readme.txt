install pyenv
    https://github.com/yyuu/pyenv

install virtualenv
install virtualenvwrapper
    http://virtualenvwrapper.readthedocs.org/en/latest/install.html

load dependencies using requirements.txt
    pip install -r requirements.txt
    pip freeze > requirements.txt

create virtualenv
    mkvirtualenv "name"
    workon "name"

activate python on virtualenv
    pyenv local 2.7.6

install django on virtualenv
    pip install django

initialize database
    python manage.py syncdb

import movies with a django command
    processing the ratings.list file to get movies details (the file is obtained from http://www.imdb.com/interfaces)
    create a django command to import the movies details and save it in database
    run the command created: python manage.py "command"


