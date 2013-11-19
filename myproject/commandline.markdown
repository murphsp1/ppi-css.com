## Start postgres

	postgres -D /usr/local/var/postgres 


## Start the local development server using extensions


	python manage.py runserver_plus   


## Database Migrations:


	./manage.py schemamigration css0 --auto
	./manage.py migrate css0   

