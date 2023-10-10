#LMS-system for DRF

The project allows you to upload and manage your courses and lessons, and receive notifications for updates in courses.

Requirements:\
amqp==5.1.1\
asgiref==3.7.2\
async-timeout==4.0.3\
billiard==4.1.0\
celery==5.3.4\
certifi==2023.7.22\
charset-normalizer==3.2.0\
click==8.1.7\
click-didyoumean==0.3.0\
click-plugins==1.1.1\
click-repl==0.3.0\
colorama==0.4.6\
cron-descriptor==1.4.0\
Django==4.2.4\
django-celery-beat==2.5.0\
django-filter==23.2\
django-timezone-field==6.0.1\
djangorestframework==3.14.0\
djangorestframework-simplejwt==5.3.0\
dnspython==2.4.2\
drf-yasg==1.21.7\
idna==3.4\
inflection==0.5.1\
kombu==5.3.2\
packaging==23.1\
Pillow==10.0.0\
prompt-toolkit==3.0.39\
psycopg2-binary\
PyJWT==2.8.0\
python-crontab==3.0.0\
python-dateutil==2.8.2\
python-dotenv==1.0.0\
pytz==2023.3\
PyYAML==6.0.1\
redis==5.0.0\
requests==2.31.0\
six==1.16.0\
sqlparse==0.4.4\
stripe==6.5.0\
typing_extensions==4.7.1\
tzdata==2023.3\
uritemplate==4.1.1\
urllib3==2.0.4\
vine==5.0.0\
wcwidth==0.2.6\

.env
This application needs you to create ".env" file. Then you need to set all constants. The structure is contained in .env.example file.

Docker
To start in Docker you will need installed Docker on your device. To start run the following commands:
`docker build -t drf-homework .` - builds image for this app in Docker
`docker run drf-homework` - launches a container with the saved docker image