Churchill
==========================================================

Django application for calculation of alcohol consumption

[![CircleCI](https://img.shields.io/github/workflow/status/manti-by/churchill/Backend/master)](https://github.com/manti-by/churchill/actions)
[![Status](https://img.shields.io/website/https/manti.by)](https://churchill.manti.by)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/churchill/master/LICENSE)

Setup:
----------------------------------------------------------

1. Install app requirements

        $ pip install -r requirements/dev.txt
        
2. Collect static, run migrations and create super user

        $ ./manage.py collectstatic --no-input
        $ ./manage.py migrate
    
3. Run dev server

        $ ./manage.py runserver