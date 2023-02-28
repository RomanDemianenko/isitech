# REPOSITORY: iSi Technology testing

## ABOUT
This repository hosts the code for a rest API implementation of the Users create/delete threads with other Users, send 
messages, getting information about threads and messages.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and 
testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

These instructions are valid for Mac or Linux. 

You need to install following software:
* [Docker](https://docs.docker.com/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Installing

Clone git-repositories:
```bash
git@github.com:RomanDemianenko/isitech.git
```

Change the work directory to cloned project root dir:

```
cd isitech
```

**Run the project**
```bash
docker-compose up
```
Run in daemon mode (in the background) 
```bash
 docker-compose up -d
``` 
If this is not your first run and you have changed the requirements, rebuild the existing images.
```bash
 docker-compose up --build
```

### Project resources
**Local uri**

- http://localhost:8000/api/ - Backed API
- http://localhost:8000/admin/ - Admin Panel


## Built With

* [Docker](https://docs.docker.com/install/) – used for auto-deployment and 
  management the applications and create containers.
* [Docker-compose](https://docs.docker.com/compose/install/) – used for running 
  multiple Docker containers and build and manage them local.
* [Django](https://www.djangoproject.com/) – API, ORM.
