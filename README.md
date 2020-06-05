# PySpace Client

PySpace (working title) is an in-development programming-oriented space simulator. The eventual goal is to provide a sandbox environment to explore, mine, build, and fight along with other players. This is a client inteded to be used along with the server hosted on this same account

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run PySpace, you'll need the following

 - Python3.8
 - virtualenv

 Since this is the client program, you'll want to make sure to install and run
 the [PySpace Server](https://github.com/austinphilp/space-client) first.


### Installing

In order to use the PySpace Client, first clone the repository and cd into it

```
$ git clone https://github.com/austinphilp/space-client
$ cd pyspace
```

For a convenient installation and execution (until I get around to dockerizing the server), we've included a makefile with all the necessary logic included needed to perform the installation. First you'll want to create the virtual environment, then install pip dependencies. Both of these steps are contained in make recipes.

```
$ make venv
$ make install
```

### Modules
This client repository has a 3 usable modules, useful for controlling your ship
and examining your environment.

**Control Module**
The control module is simply a python CLI, initialized a `ship` variable. You can use these to control your ship, using the class in `models/ship`.

```
$ make control
```

**Scanner**
This module grabs sensor information from all of your ship's onboard sensors, displaying positional and vector data for any nearby bodies.

```
$ make scanner
```

**Screen**
This module displays detailed information regarding the status of your ship and its various components.

```
$ make screen
```

### Coding Style Tests

This project is PEP-8 compliant, in order to verify compliance, simply use the
following make recipe

```
make flake8
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Austin Philp** - *Initial work* - [AustinPhilp](https://github.com/austinphilp)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
