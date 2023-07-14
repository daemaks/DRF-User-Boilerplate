# Django REST Framework Boilerplate

This is a Django REST Framework project boilerplate that provides a starting point for building web APIs using Django and Django REST Framework. It includes a custom user model, a status (post) model, and tests to ensure the functionality of the API.

## Installation

1. Clone the repository:
```
git clone https://github.com/daemaks/DRF-User-Boilerplate
```
2. Change into the project directory:
```
cd DRF-User-Boilerplate
```
3. Create and activate a virtual environment (optional but recommended):
```
python3 -m venv venv
source venv/bin/activate
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```

5. Configure the environment variables:

- Copy the `.env_example` file in the `api` directory and rename it to `.env`.
- Open the `.env` file and update the values according to your configuration.
  - For example, you might set `SECRET_KEY`, `JWT_SECRET` or any other required environment variables.
  - Make sure to provide the correct database connection details, such as `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, if you're using a database.
  - Modify any other settings as necessary for your project.
- Save the changes to the `.env` file.

6. Apply the database migrations:
```
python manage.py migrate
```
7. Create a superuser (admin) account:
```
python manage.py createsuperuser
```
8. Start the development server:
```
python manage.py runserver
```
The API should now be accessible at `http://localhost:8000/`.

## Custom User Model

The boilerplate includes a custom user model defined in `api/user/models.py`. This model extends Django's built-in `AbstractUser` class and provides fields for first_name, last_name, email, and password. You can customize the user model further by adding or removing fields as needed.

## Status (Post) Model

The boilerplate also includes a `Status` model defined in `api/status/models.py`. This model represents a status or post in the API and includes fields such as content, user (foreign key to the custom user model), and created timestamp. You can modify this model or add additional models to suit your project's requirements.

## Testing

The boilerplate includes a set of tests defined in `tests/` to ensure the functionality of the API. You can run the tests using the following command:
```
pytest
```
Make sure to add more tests as you build out your API to maintain code quality and prevent regressions.