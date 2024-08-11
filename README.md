# Django_Recipe_App

- ## Live Hosted Link =>  https://django-recipe-app.onrender.com (Note: This is deployed on render which is a free service & for the first api call you have to wait for 50 seconds)

- ## To check the project in Local System follow the below steps. 

- ### clone the github repo from the url => https://github.com/IntriguedSayan/Django_Recipe_App.git

- ### Then follow the commands
```
cd Django_Recipe_App/Django_Recipe_App
```

- Before doing these make sure Docker is installed and Docker desktop is running
```
docker-compose build
```

```
docker-compose up
```
- Once the containers are running, you'll need to apply any pending migrations. Open a new terminal window and run:

```
docker-compose exec web python manage.py migrate
```

- ### Aceess the project at => http://127.0.0.1:9000/