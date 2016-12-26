# Web dK

A small online shop that sells gaming gears

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

App Engine SDK for Python. Instruction and download link can be found [here](https://cloud.google.com/appengine/docs/python/download)

```
Please choose 'Optionally, you can also download the original App Engine SDK for Python.'
```

### Installing

No installation is required

## Building and running locally

Add google-appengine-sdk to your PATH

```
export PATH=$PATH:DIRECTORY_PATH/google_appengine_1.9.49/
```

Start the local development web server by running the following command from the project directory

```
dev_appserver.py ./
```

Visit [http://localhost:8080/](http://localhost:8080/) in your web browser to view the app

## Deployment

Instruction to deploy to Google Appengine (Google Cloud Platform) can be found [here](https://cloud.google.com/appengine/docs/python/getting-started/deploying-the-application)

## Built With

* [Webapp2](https://webapp2.readthedocs.io/en/latest/) - The web framework used
* [Jinja2](https://maven.apache.org/) - Templating engine for Python.
* [Bootstrap3](http://getbootstrap.com/) - For styling

