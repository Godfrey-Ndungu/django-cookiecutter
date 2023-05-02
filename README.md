<h1 align="center" id="title">Django cookiecutter</h1>


<p id="description">Django-Cookiecutter is a quick-start project template for building Django web applications with the Django Rest Framework Postgres Redis Celery CircleCI GitLab CI and Docker. This project template provides a solid foundation for building scalable and maintainable web applications with Django and its ecosystem.</p>

<h2>🛠️ Installation Steps:</h2>

<p>1. clone the repo</p>

```
git clone git@github.com:Godfrey-Ndungu/django-cookiecutter.git
```

<p>2. cd django-cookiecutter</p>

<p>3. make makefile.sh executable</p>

```
chmod +x makefile.sh
```

<p>4. Run makefile</p>

```
./makefile.sh
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Django
*   Django-rest-framework
*   swager-ui
*   redis
*   postgresql
*   docker
*   celery


## Local Environment Variables

The following environment variables are required to run this project locally. Please set them with appropriate values:

`SECRET_KEY`

`ALLOWED_HOSTS`

`DEBUG`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`


## Production Environment Variables

`SECRET_KEY`

`ALLOWED_HOSTS`

`DEBUG`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`

`AWS_ACCESS_KEY_ID`

`AWS_SECRET_ACCESS_KEY`

`AWS_STORAGE_BUCKET_NAME`

`AWS_QUERYSTRING_AUTH`

`AWS_DEFAULT_ACL`

`AWS_S3_SIGNATURE_VERSION`

`AWS_S3_OBJECT_PARAMETERS`

`PUBLIC_MEDIA_LOCATION`

`MEDIAFILES_LOCATION`

`AWS_CLOUDFRONT_DOMAIN`



## Run Locally

Clone the project

```bash
  chmod +x makefile.sh
  ./makefile.sh
```


## Run Tests

Clone the project

```bash
  tox
```


