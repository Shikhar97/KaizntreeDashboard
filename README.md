# Project Overview

This project is a web application designed to manage inventory items. It utilizes Django REST Framework for the backend with a PostgreSQL database. The frontend design mockups are created using Figma. This project is completed as part of the Kaizntree backend challenge.

## Installation

Follow these steps to set up the project environment and run the application:

1. **Python Installation**: Ensure Python is installed on your system and added to PATH during installation.

2. **Verify Python Installation**: Confirm Python installation by running `python --version` in the terminal.

3. **PostgreSQL Installation**: Download and install PostgreSQL from the official website.

4. **Set PostgreSQL Password**: Set a password for the default PostgreSQL user during installation.

5. **Python Dependencies**: Install all the requirements using `python3.10 -m pip install -r requirements.txt`.

6. **Create Database**: Create a PostgreSQL database named `kaizn`.

10. **Run Migrations**: Run database migrations using `python3.10 manage.py makemigrations` and `python3.10 manage.py migrate`.

11. **Run Application**: Start the Django development server with `python3.10 manage.py runserver`.

## API Documentation

The API endpoints are documented using Swagger. You can access the interactive endpoints documentation [here](http://localhost:8000/v1/api_docs/)

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
