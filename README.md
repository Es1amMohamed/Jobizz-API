
# Jobizz-API

Jobizz API is a web application built using Python and Django. It allows users to register as individuals or companies. Companies can post job vacancies, and job seekers can apply for these jobs.


## Features

User Registration and Authentication:
- Users can register as either job seekers or companies.
- JWT authentication is used to secure the API endpoints.
Job Posting and Management:

- Companies can post new job vacancies, including details such as job title, description, and company size.

- Companies can manage their job postings.

Job Application:

- Job seekers can browse and apply for job vacancies.

- Applications are tracked and managed through the API.

Filtering and Searching:

- Jobs can be filtered by company size, company name, and job title, making it easier for job seekers to find relevant opportunities.

Permissions and Security:

- Different permissions for job seekers and companies ensure that users can only access and modify data relevant to their roles.
- Secure JWT-based authentication to protect user data and API endpoints.

## Technologies Used
- Python: The core programming language used for the development of the application.
- Django: The web framework used for building the backend of the application.
- Django REST Framework: Utilized for creating RESTful APIs.
- Django Filters: Used for implementing filtering capabilities in the API.
- JWT (JSON Web Tokens): Used for secure user authentication.
- PostgreSQL: The database system used for storing application data.
## Installation

Clone the repository:
- git clone https://github.com/Es1amMohamed/Jobizz-API 
- cd Jobizz-API

Create and activate a virtual environment:
- python -m venv venv
- source venv/bin/activate  
- on Windows usevenv\Scripts\activate
Install the dependencies:
- pip install -r requirements.txt
Setup the database:
- python manage.py makemigrations
- python manage.py migrate
Create a superuser (optional):
- python manage.py createsuperuser
Run the local server:
- python manage.py runserver


## Contribution:
We welcome contributions to the development of this project. If you would like to contribute, please open a pull request, and we will review it promptly.
## Support
For support, email eslammohamemetwaly@gmail.com or visit my LinkedIn https://www.linkedin.com/in/eslam-mohamed-aa3b87239/
