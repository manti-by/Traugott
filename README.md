Churchill
==========================================================

Django application for calculation of alcohol consumption


Setup:
----------------------------------------------------------

1. Install app requirements

        $ pip install -r requirements.txt
        
2. Collect static, run migrations and create super user

        $ ./manage.py collectstatic --no-input
        $ ./manage.py migrate
    
3. Run dev server

        $ ./manage.py runserver