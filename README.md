Traugott
==========================================================

React/Redux application for calculation of alcohol consumption


Setup:
----------------------------------------------------------

Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

Run Vagrant and login to box:

```
$ vagrant up
$ vagrant ssh
```

Update system packages:

```
$ sudo apt-get update
$ sudo apt-get upgrade -y
```

Remove default system NodeJS and NPM

```
sudo apt-get remove nodejs npm
```

Install latest NodeJS server, NPM and MongoDB

```
$ curl -sL https://deb.nodesource.com/setup_0.12 | sudo -E bash -
$ sudo apt-get install -y nodejs mongodb-server mongodb-clients build-essential
```

Install NPM packages and run server:

```
$ cd /home/vagrant/www/traugott/src/app
$ npm install
$ npm start
```

Install ShipIt tool for deployment

```
$sudo npm install --global shipit-cli shipit-deploy
```

If you are working on windows, use following command to avoid binary links

More info [there](http://perrymitchell.net/article/npm-symlinks-through-vagrant-windows/)
and [there](http://superuser.com/questions/124679/how-do-i-create-a-link-in-windows-7-home-premium-as-a-regular-user?answertab=votes#125981)

```
$ mkdir ~/node_modules
$ cd ~/node_modules
$ mkdir archimed
$ cd ./traugott
$ mkdir node_modules
$ cp /home/vagrant/www/traugott/src/app/package.json package.json
$ npm install package.json
$ cd /home/vagrant/www/traugott/src/app
$ ln -s ~/node_modules/traugott/node_modules node_modules
```

Open up [http://localhost:3000/](http://localhost:3000/) in your browser.
