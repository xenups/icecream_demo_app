Room Rest App

Simple rest app using [ICECREAM](https://github.com/xenups/ICECREAM "ICECREAM")


## Quickstart:

   	#install requirements:
    pip install -r requirements.txt
    
	#make migration
	python manage.py  makemigrations init
	
	#to migrate
	alembic upgrade head
	
	#runing server
    python manage.py runserver 

 
and access to http://localhost:8888/api

##
To Add Room

    curl --location --request POST 'http://127.0.0.1:8888/rooms' \
    --header 'Content-Type: application/json' \
    --data-raw '{
     "name":"room_name"
    }'

##
To Get All Rooms

    curl --location --request GET 'http://127.0.0.1:8888/rooms' \
    --data-raw ''

##
To Get a Room by id:

     curl --location --request GET 'http://127.0.0.1:8888/rooms/1' \
     --header 'Content-Type: application/json' \
     --data-raw ''

##
To Filter a Rooms:

     curl --location --request GET 'http://127.0.0.1:8888/rooms/filter?query={%22sort%22:%22name-%22,}' \
     --data-raw ''