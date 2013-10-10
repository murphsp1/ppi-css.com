sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git

sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv

#Throw on a fortran compiler for attempting to install scipy in virtualenv
sudo apt-get install gfortran

sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose



#Install the web server to serve pages
sudo apt-get install apache2 libapache2-mod-wsgi



/usr/share/apache2/default-site/index.html:<p>This is the default web page for this server.</p>


#Install Mysql

sudo apt-get install mysql-server
mysql_secure_installation
sudo apt-get install python-mysqldb

mysql --user=root --password=spm5555
mysql> create database django_test;

I then had to remove stuff from requirements including psycopg2


git clone https://github.com/murphsp1/myproject.git

edit the settings to reflect new database


WHERE wsgi.py is
/home/seanmurphy/myproject/myproject/myproject

WHERE STATIC IS:
/home/seanmurphy/myproject/myproject/myproject/myapp/static


http://192.158.29.226/myapp/init_table_data_load/

but need to update the original source to have a proper path


python manage.py syncdb
python manage.py migrate



sudo vi /etc/apache2/sites-available/default
plus edit the wsgi.py file

http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/



You need to do two things

In the Amazon Web Service admin panel, create an elastic IP in the same region as your instance and associate that IP with your that instance (IPs cost nothing while they are associated with an instance, but do cost if not).
Add a A record to the DNS record of your domain mapping the domain to the elastic IP address assigned in (1). 

Your domain provide should either give you some way to set the A record (the IP address), or it will give you a way to edit the nameservers of your domain.








#need to remove scipy and numpy from requirements file
#otherwise they really don't seem to install properly
#also, must install psycopg2 separately

sudo apt-get install python-virtualenv


sudo pip install -r ./requirements.txt 


#need to install webserver and mod-wsgi



#need to setup appache webserver


/home/seanmurphy/myproject/myproject/myproject

#need to configure GCE firewall settings
gcutil addfirewall http2 --description="Incoming http allowed." --allowed="tcp:http" --project="1040981951502"




references:
http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/


The Django Book
Deploying Django
http://www.djangobook.com/en/2.0/chapter12.html



Complete Single Server Django Stack Tutorial
http://www.apreche.net/complete-single-server-django-stack-tutorial/

START TO FINISH - SERVING DJANGO WITH UWSGI/NGINX ON EC2
http://adambard.com/blog/start-to-finish-serving-mysql-backed-django-w/

Non-techie Guide to setting up Django, Apache, MySQL on Amazon EC2
http://pragmaticstartup.wordpress.com/2011/04/02/non-techie-guide-to-setting-up-django-apache-mysql-on-amazon-ec2/

Deploying Django on Amazon EC2 Server
http://nickpolet.com/blog/1/

Deploying Python, Django on ec2 linux instance
http://blog.hguochen.com/blog/2013/09/deploying-python-django-on-ec2-linux-instance/

How to use Django with Apache and mod_wsgi
https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/


Setting up Django with Nginx, Gunicorn, virtualenv, supervisor and PostgreSQL
http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/


#need to install postgres ...
sudo apt-get install postgresql
sudo apt-get install libpq-dev
sudo pip install psycopg2

#need to setup postgres db and accounts
sudo passwd postgres   #update postgres user passwrd

seanmurphy@(none):~/myproject/myproject/myproject$ sudo su - postgres
sudo: unable to resolve host (none)
postgres@(none):~$ createdb test

postgres@(none):~$ createuser -P
Enter name of role to add: hello_django
Enter password for new role: 
Enter it again: 
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n

vi /etc/postgresql/9.1/main/pg_hba.conf

