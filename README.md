# Late Blight Readme

Welcome to our project! This README will guide you through setting up the project, understanding its structure, and how to contribute.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Contributing](#contributing)
6. [License](#license)

## Project Overview

This application is solely made to serve a purpose of providing the late blight probabilities of various locations on a user's mobile devices
this acts as a server. You need to change the url to the server in mobile device in order to sync it with the mobile interface.
For now the app is published by Kathmandu University as a name 'Late Blight' in google playstore serving it from the Kathmandu University's server located at Panchkhal.

## Installation

To run this project locally, follow these steps:


1. Navigate to the project directory:

    ```
    cd Late_Blight
    ```

2. Install dependencies:
    (as there are some lib that depends in torch)

    ```
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

    pip install torch-scatter torch-sparse --no-index -f https://data.pyg.org/whl/torch-2.3.0+cu118.html

    pip install -r requirements.txt
    ```

3. Make and Apply migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Create a superuser (optional):

    ```
    python manage.py createsuperuser
    ```

5. Start the development server:

    ```
    python manage.py runserver
    ```

6. Access the project at `http://localhost:8000` in your web browser.

## Usage

Once the project is set up, you can start using it. Here are some common tasks you might want to perform:

- Access the admin interface: Navigate to `http://localhost:8000/admin` and log in using the superuser credentials you created.
- Main server's api endpoints are
```
/api/user-info/
/prediction/lateblight/all
/prediction/lateblight/data?lat=28&long=80
```

## Project Structure

Our project follows a typical Django project structure:



- `project_name/`: Contains the main project settings and configuration.
- `app_name1/`, `app_name2/`, etc.: Each represent individual Django apps within the project.
- `templates/`: Contains HTML templates used by the project.
- `static/`: Contains static files such as CSS, JavaScript


## License

Kathmandu University ICIMOD joint project