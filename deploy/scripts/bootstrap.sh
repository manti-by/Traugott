#!/bin/bash
header () {
    echo "--------------------------------------------------------------------------------"
    echo $1
    echo "--------------------------------------------------------------------------------"
}

TARGET=${1:'vagrant'}
APP_NAME='default'
APP_PATH=$(realpath $(pwd)'/../../app/')
ROOT_PATH=$(realpath $(pwd)'/../../')

header "Updating system"
sudo apt-get update && sudo apt-get upgrade -y

header "Install required libraries"
sudo apt-get install -y git python-pip python-dev
if [ $TARGET == 'staging' ]; then
    sudo apt-get install -y nginx supervisor postgresql libpq-dev
fi

header "Install python packages"
sudo pip install -r $ROOT_PATHrequirements.txt

if [ $TARGET == 'staging' ]; then
    header "Create database and user for project"
    sudo -u postgres bash -c "psql -c \"CREATE DATABASE $APP_NAME;\""
    sudo -u postgres bash -c "psql -c \"CREATE USER $APP_NAME WITH PASSWORD 'password';\""
    sudo -u postgres bash -c "psql -c \"ALTER ROLE $APP_NAME SET client_encoding TO 'utf8';\""
    sudo -u postgres bash -c "psql -c \"ALTER ROLE $APP_NAME SET default_transaction_isolation TO 'read committed';\""
    sudo -u postgres bash -c "psql -c \"ALTER ROLE $APP_NAME SET timezone TO 'UTC';\""
    sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $APP_NAME TO $APP_NAME;\""
fi

header "Copy app settings"
cp $APP_PATHcore/settings/$TARGET.py.example $APP_PATHcore/settings/$TARGET.py

header "Migrate, collect static files, create admin user"
python $APP_PATHmanage.py migrate --settings=core.settings.$TARGET.py
python $APP_PATHmanage.py collectstatic --noinput --settings=core.settings.$TARGET.py

if [ $TARGET == 'staging' ]; then
    header "Update server configs"
    ln -s $ROOT_PATHdeploy/confs/uwsgi.ini.$TARGET $ROOT_PATHdeploy/confs/uwsgi.ini
    sudo ln -s $ROOT_PATHdeploy/confs/nginx.conf.$TARGET /etc/nginx/sites-available/$APP_NAME.conf
    sudo ln -s $ROOT_PATHdeploy/confs/supervisor.conf.$TARGET /etc/supervisor/conf.d/$APP_NAME.conf
    sudo service nginx restart
    sudo supervisorctl restart $APP_NAME
else
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python $APP_PATHmanage.py shell --settings=core.settings.$TARGET.py
    echo "Usage: python manage.py runserver 0.0.0.0:8000 --settings=core.settings.$TARGET.py"
fi

header "All operations have done"
