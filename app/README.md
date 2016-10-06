Traugott
==========================================================

React/Redux application for calculation of alcohol consumption


Setup:
----------------------------------------------------------

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
$ cd /vagrant/application
$ npm install
$ npm start
```


See [root readme](https://github.com/manti-by/traugott) for more info
