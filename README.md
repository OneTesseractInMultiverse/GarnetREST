# GarnetREST

Author: Pedro Guzmán (pedro@subvertic.com)

Version: 1.0.0

License: MIT License

## About GarnetREST

An implementation of a Flask-based Boilerplate for REST APIs and REST-based Microservices. The 
idea behind GarnetREST is to provide a base organization schema and some basic functionality that is 
present in most Web API Applications based on RESTful principles. GarnetREST provides:

* Support for MongoDB (Soon a version for Neo4j Graph Database will also be available)
* Support for Json Web Token (JWT) Generation and Authentication
* User account creation and management out-of-the-box

====

## Installation

GarnetREST incorporates a set of cryptographic tools built-in. These tools are built on top of
PyNaCl which is a Python binding for libsodium which is a cryptographic library developed by several 
renowned cryptographers including Daniel J. Bernstein.

First you must install libsodium using one of the following methods:

* Mac OSX (Using homebrew): 

```bash
brew install libsodium
```

* Linux (APT):
```bash
#!/bin/bash
sudo add-apt-repository ppa:chris-lea/libsodium;
sudo echo "deb http://ppa.launchpad.net/chris-lea/libsodium/ubuntu trusty main" >> /etc/apt/sources.list;
sudo echo "deb-src http://ppa.launchpad.net/chris-lea/libsodium/ubuntu trusty main" >> /etc/apt/sources.list;
sudo apt-get update && sudo apt-get install libsodium-dev;
```

Or if you want to build it from source just download the sources from [here](https://download.libsodium.org/libsodium/releases/) 
and extract it. Then move into the extracted folder and run:

```bash
./configure
make
make check
sudo make install
```

* On Windows you can find pre-built libraries [here](https://download.libsodium.org/libsodium/releases/)



