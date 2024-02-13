# Project Overview

This project is a web application designed to manage inventory items. It utilizes Django REST Framework for the backend with a PostgreSQL database. The frontend design mockups are created using Figma. This project is completed as part of the Kaizntree backend challenge.

## Installation

Follow these steps to set up the project environment and run the application:

**Python Installation**: Ensure Python is installed on your system and added to PATH during installation.

**Verify Python Installation**: Confirm Python installation by running `python --version` in the terminal.

**Python Dependencies**: Install all the requirements using the following commands

        python3.10 -m pip install -r requirements.txt
        python3.10 -m pip install django-filter
        python3.10 -m pip install django-cors-headers
        python3.10 -m pip install django-rest-swagger
        python3.10 -m pip install django-rest-passwordreset
        python3.10 -m pip install psycopg2-binary
        python3.10 -m pip install whitenoise

**PostgreSQL Installation**: Download and install PostgreSQL from the official website.

        sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
        wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        sudo apt install postgresql postgresql-contrib
        sudo systemctl start postgresql.service
        sudo systemctl enable postgresql.service

**Create Database**: Create a PostgreSQL database named `kaizn`.

        CREATE DATABASE kaizn;


**Redis Server**: Install redis-server and start the server
        
        curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
        sudo apt-get install redis
        redis-server --port 6380 &


**Run Migrations**: Run database migrations using 

        python3.10 manage.py makemigrations
        python3.10 manage.py migrate

**Run Application**: Start the Django development server with `python3.10 manage.py runserver`.

## API Documentation

The API endpoints are documented using Swagger. You can access the interactive endpoints documentation [here](http://34.228.169.188:8000/v1/api_docs/)

## Frontend Mockups

The frontend design mockups are available on Figma. View the mockups [here](https://www.figma.com/file/fjzPIi67Jk7WgW3gjeA0Tk/Kaizntree-Full-Stack-Interview-UI-Template?type=whiteboard&node-id=44-64&t=HhPvAZnRd4QYe75i-0).

## Unit Testing

To test the API endpoints, use the following commands:

- `python manage.py test auth_api`
- `python manage.py test item_api`

## Technological Choices

- **PostgreSQL**: Chosen for its robustness in handling complex data relationships and queries. 
- **JWT for Authentication**: JWT tokens are used for authentication due to their compactness, stateless nature, and secure digital signatures.

## Frontend URL

*TBD*
