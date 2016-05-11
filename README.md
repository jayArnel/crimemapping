# Crime Modelling and Prediction
## Libraries
NOTE: Some of this libraries may fail to install depending on the ubuntu version you have on your machine.
``` shell
sudo apt-get install binutils libproj-dev postgresql-9.4-postgis-2.1 postgresql-server-dev-9.4 postgresql-contrib-9.4 libatlas-base-dev libblas-dev
```

## Clone
``` shell
git clone git@github.com:jayArnel/crimemapping.git
cd crimemapping
```

## Create Virtualenv
``` shell
sudo pip install virtualenvwrapper
mkvirtualenv <name>
workon <name>
```

## Install Package Dependencies
``` shell
pip install -r requirements.txt
```

## Create the Database
``` shell
sudo su - postgres
createdb <dbname>
```
## Create User for the Database
``` shell
sudo su - postgres 
createuser -s -P <username>
    *setup password*
psql
GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
```

## Extend Database to postgis
``` shell
sudo su - postgres 
psql <dbname>
CREATE EXTENSION postgis;
```

## Setup Database with Django
create  `local_settings.py` file in `crimemapping` folder
``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '<dbname>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```


## Run Migrations
make sure your virtualenv `<env>` is activated by calling `workon <env>`
``` shell
python manage.py migrate
```

## Collect static files
``` shell
python manage.py collectstatic -l --no-input
```

## Setup Nginx
setup a local server in your machine via Nginx

### Install nginx
``` shell
sudo apt-get install nginx
```

### Setup Nginx configuration
create configuration file
``` shell
sudo nano /etc/nginx/sites-available/crimemapping
```
copy-paste configuration
``` nginx
upstream localhost {
    server localhost:8000;
}
server {
    listen 0.0.0.0:80;
    server_name localhost;

    keepalive_timeout 5;
    # path for static files
    root /path/to/project/storage; #! important! update this path
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://localhost;
            break;
        }
    }
}
```
enable configuration
``` shell
sudo ln -s /etc/nginx/sites-available/crimemapping /etc/nginx/sites-enabled/crimemapping
``
check for errors, then restart nginx
``` nginx
sudo nginx -t
sudo service nginx restart
```


