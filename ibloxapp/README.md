Infoblox Test:

Dated: 06-09-2020
Author: Deepa G Pillai

Endpoints used in the project:
1. Registration
2. To generate token for user
3. To access refresh token
4. To list all data based on condition(s) provided in the requirement
5. To add new data

Api's to used:
1. /api/register
2. /api/auth/token
3. /api/auth/token/refresh
4. /auth/all
5. /api/new


Requirements:
1. psycopg2-binary
2. django==3.0
3. djangorestframework==3.1.1
4. djangorestframework_simplejwt


Note to use application:
1. Clone the application(master branch)
2. Create virtual environment for python(python3 -m venv <virtual environment name>)
3. Activate the virtual environment(<Virtual environment name>/Scripts/activate (in windows))
4. Install requirements mentioned in the requirement.txt file (pip install -r requirements.txt)
5. In windows, set the project in any IDE(pycharm) with newly created Venv
6. Create postgre dB(infodB) and add migrations(python manage.py makemigrations - for creating new migrations
                                                python manage.py migrate - to apply migrations)
7. Create superuser (python manage.py createsuperuser)
8. Apply styles to django ui(python manage.py collectstatic, (optional) )
9. To run the application (python manage.py runserver)