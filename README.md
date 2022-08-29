# Vnexpress News Article Scraper and Management

## Description:
---
This project was made to scrape the VnExpress's Giao Duc section and scrape all the title and short summary of all news titles

## Installation
---

The application can either be deployed using Docker or run locally

- Docker

```bazaar
docker-compose up --build
```

- Local

```bazaar
pip install -r requirements.txt
```

For this project you need to have an .env file in order for the project to run correctly

The .env file should have the following variables:

```bazaar
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
SECRET_KEY=
BROKER_URL=
CELERY_RESULT_BACKEND=
REDIS_HOST_PORT=
REDIS_PASSWORD=
MYSQL_HOST=
MYSQL_PORT=
MYSQL_HOST_PORT=
DJANGO_HOST_PORT=
JWT_EXP_MINUTE=
```

## Running
---
For Local:
1) You can start the app with:
```bazaar
python3 manage.py runserver
```
2) Turn on Celery's worker (on a seperate terminal) with:
```bazaar
celery -A project_main.celery worker -l INFO
```
3) Turn on Redis:

For Linux
```bazaar
sudo services redi-server start
```

For MacOS
```bazaar
brew services start redis
```

## Testing
---
The application can be tested via Postman through these urls as follows:

### 1) Login (POST):
```http://localhost:8000/auth/login```

Provide a the necessary information into the BODY:
```bazaar
{
    "username": "<insert username here>",
    "password": "<insert password here>"
}
```

### 2) Logout (POST):

Provide the JWT token generated from the Login method

### 3) Create, Read, Update, Delete and Scrape

- Read (GET):
  - Paginated list of new article: 
  
      ```http://localhost:8000/article/?page=<int>```
  - Search: 
      
      ```http://localhost:8000/article/?search=<str>```
  - Get detailed article: 
  
      ```http://localhost:8000/article/details/<uuid>```
---
- Create (POST): ```http://localhost:8000/article/```
  - Provide a the necessary information into the BODY:
```bazaar
{
    "title": "",
    "descirption": "",
    "url": ""
}
```
---
- Update (POST): ```http://localhost:8000/article/<pk>```
  - Provide a the necessary information into the BODY:
```bazaar
{
    "title": "",
    "descirption": "",
    "url": ""
}
```
---
- Delete (POST): ```http://localhost:8000/article/<pk>```
---
- Scrape (GET): ```http://localhost:8000/scrape/```


MIT License

Copyright (c) 2022 Dennis Dinh Hung