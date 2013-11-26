The commands needed to launch various components on the development machine.

## Start postgres

	postgres -D /usr/local/var/postgres 


## Start the local development server using extensions


	python manage.py runserver_plus   


## Database Migrations:


	./manage.py schemamigration css0 --auto
	./manage.py migrate css0   

## Relevant GIT commands

I find I only use the following three commit commands:

	git add .

or

    git add -u

or

    git add -A
	git commit -m "blah blah blah"
	git push -u origin master