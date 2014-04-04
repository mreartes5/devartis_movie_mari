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

intall django on virtualenv
    pip install django

initialize database
    python manage.py syncdb




