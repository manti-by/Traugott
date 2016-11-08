Churchill
==========================================================

Django application for calculation of alcohol consumption


Setup:
----------------------------------------------------------

1. Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

2. Run Vagrant and login to box:

        $ vagrant up
        $ vagrant ssh

3. Update system packages:

        $ sudo apt-get update
        $ sudo apt-get upgrade -y

4. Install app requirements

        $ cd app/
        $ sudo pip install -r requirements.txt
        
5. Collect static, run migrations and create super user

        $ ./manage.py collectstatic --no-input
        $ ./manage.py migrate
        $ ./manage.py createsuperuser --username admin --email admin@test.com
    
6. Run dev server

        $ ./manage.py runserver 0.0.0.0:8000