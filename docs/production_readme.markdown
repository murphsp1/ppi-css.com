


## Introduction ##






## 0. Initial Configuration ##

I have noticed a great deal of tutorial blogs don't offer much in the way of detailed environment specifications used for the tutorial and do no want to go down the same path.



static IP = 162.222.181.45



## 1. Update the Instance and Install Tools ##
After the instance boots, we must ssh in to the instance for the first time via:


Next, we need to update the default packages install on the virtual instance:

    sudo apt-get update
    sudo apt-get upgrade

and install some basic needed development tools:

    sudo apt-get install make
    sudo apt-get install wget
    sudo apt-get install git

and install some basic Python-related tools:

    sudo apt-get install python-setuptools
    sudo easy_install pip
    sudo pip install virtualenv

## 2. Install Numpy and Scipy (SciPy requires Fortran compiler) ##

To install SciPy, Python's general purpose scientific computing library from which we need a single function, we need the Fortran compiler
    
    sudo apt-get install gfortran

and then we need Numpy and Scipy and everything else

    sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

Finally, we need to add ProDy, a protein dynamics and sequence analysis package for Python.

    sudo pip install prody

Remove all of the various bits and pieces for numpy and scipy from the requirements file and then do:

    sudo pip install -r ./requirements.txt


## Install and Configure the Database (MySQL) ##

    sudo apt-get install mysql-server

The installation process should prompt you to create a root password. Please do so for security purposes.

Next, we are going to execute a script to secure the MySQL installation:

    mysql_secure_installation

You already have a root password from the installation process but otherwise answer "Y" to every question.

With the DB installed, we now need to create our database for Django (mine is creatively called django_test). Please note that there must not be a space between "--password=" and your password on the command line.

    mysql --user=root --password=INSERT PASSWORD
    mysql> create database django_test;
    mysql> quit;

Finally for this step we need the MySQL database connector for Python which will be used by our Django app:

    sudo apt-get install python-mysqldb

Note: why did I got with MySQL instead of Postgres? The simple reason was that it took fewer steps to get the MySQL server up and running than the Postgres server. I actually run Postgres on my development machine.


## Install the Web Server (Apache2) ##
You have seemingly two choices for your web server, either the tried and true Apache (now up to version 2+) or nginx. <a href="http://wiki.nginx.org/Main" target="_blank">Nginex</a> is supposed to be the new sexy when it comes to web servers but 


### A Simple Tutorial for GCE ###
This is a very basic tutorial that doesn't get into the details of getting a very simple configuration up and running on GCE. 

https://developers.google.com/compute/docs/quickstart

### Some Background on Apache Configuration Files on Debian ###
Understanding the apache2 configuration files is important for getting this to work correctly and it would appear that Debian does things a bit non-standard.  See here for more details:

http://www.control-escape.com/web/configuring-apache2-debian.html


    sudo apt-get install apache2 

    libapache2-mod-wsgi

    sudo apt-get install apache2-prefork-dev


By default, the following page is served by the install:

    /usr/share/apache2/default-site/index.html

Now we need to update the virtual hosts settings on the server.  For Debian, this is here:
/etc/apache2/sites-enabled/000-default 


Restart the service

    sudo service apache2 restart 

ERROR MESSAGES:
[....] Restarting web server: apache2apache2: apr_sockaddr_info_get() failed for (none)
apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName
 ... waiting apache2: apr_sockaddr_info_get() failed for (none)
apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName
. ok 
Setting up ssl-cert (1.0.32) ...
hostname: Name or service not known

### Need to do Configuration Work ###

sudo vi /etc/apache2/sites-available/default
plus edit the wsgi.py file

http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/






## Setup the Overall Directory Structure on the Remote Server ##

I have seen many conflicting recommendations in online tutorials about how to best layout a Django application in development. It would appear that after you have built your first dozen or so Django projects, you start formulating your own opinions and create a standard project structure for yourself. 

Obviously, this experiential knowledge is not available to someone building and deploying one of their first sites 

And, your directory structure directly impacts yours app's routings and the daunting-at-first settings.py file. If you move around a few directories, things tend to stop working.

The picture gets even murkier when you go from development to production and I have found much less discussion on best practices here. Luckily, I could ping on my friend Ben Bengfort and tap into his devops knowledge.  The directory structure on the remote server looks like this as recommended by Ben Bengfort. 

    /var/www/ppi-css.com
    /var/www/ppi-css.com/htdocs/static
    /var/www/ppi-css.com/htdocs/media
    /var/www/ppi-css.com/django
    /var/www/ppi-css.com/logs

Apache will see the htdocs directory as the main directory from which to serve files.

static will contain the collected set of static files (images, css, javascript, and more) and media will contain uploaded documents.

logs will contain relevant apache log files.

django will contain the cloned copy of the Django project from Git Hub.

The following shell commands get things setup correctly:

    sudo mkdir /var/www/ppi-css.com
    sudo mkdir /var/www/ppi-css.com/htdocs
    sudo mkdir /var/www/ppi-css.com/htdocs/static
    sudo mkdir /var/www/ppi-css.com/htdocs/media
    sudo mkdir /var/www/ppi-css.com/django
    sudo mkdir /var/www/ppi-css.com/logs
    cd /var/www/ppi-css.com/django
    sudo git clone https://github.com/murphsp1/ppi-css.com.git

There will be aliases in the virtual host configuration file that let the apache server know about this structure.





 sudo cp ppi-css.conf /etc/apache2/sites-available/ppi-css.com

    sudo a2ensite ppi-css.com

Enabling site ppi-css.com.
To activate the new configuration, you need to run:
  service apache2 reload
    
    sudo service apache2 reload

Then I added the following line:

ServerName localhost

to the /etc/apache2/apache.conf file




## Grab the Django App from GitHub



edit the settings to reflect new database


WHERE wsgi.py is
/home/seanmurphy/myproject/myproject/myproject

WHERE STATIC IS:
/home/seanmurphy/myproject/myproject/myproject/myapp/static


http://192.158.29.226/myapp/init_table_data_load/

but need to update the original source to have a proper path

From the command line in the directory with "manage.py" type:

    python manage.py syncdb
    python manage.py migrate






You need to do two things

In the Amazon Web Service admin panel, create an elastic IP in the same region as your instance and associate that IP with your that instance (IPs cost nothing while they are associated with an instance, but do cost if not).
Add a A record to the DNS record of your domain mapping the domain to the elastic IP address assigned in (1). 

Your domain provide should either give you some way to set the A record (the IP address), or it will give you a way to edit the nameservers of your domain.








#need to remove scipy and numpy from requirements file
#otherwise they really don't seem to install properly
#also, must install psycopg2 separately

sudo apt-get install python-virtualenv


sudo pip install -r ./requirements.txt 






#need to setup appache webserver


/home/seanmurphy/myproject/myproject/myproject

## GCE - Only Need to Do 
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







# New Debug 'cause server ain't working

Is server running?
sudo service apache2 status

What do the apache error logs say?
cat /var/log/apache2/error.log

gcutil --project="1040981951502" pull test2 /home/seanmurphy/myproject.tar.gz ./

gcutil --service_version="v1beta16" --project="1040981951502" ssh  --zone="europe-west1-a" "test2"


# Every Deployment

need to restart apache2
	
	sudo service apache2 restart
	
	./manage.py schemamigration css0 --auto
	s  


log in and drop the table in the database

	mysql -u root -pPASSWORD -h HOSTNAMEORIP django_test

	drop table _______;
css0_scores

need to give permission to write to the directory for the user that will be writing files

drwxrwxrwx 2 seanmurphy seanmurphy   4096 Nov 20 18:51 .

drwxr-xr-x 3 seanmurphy seanmurphy   4096 Nov 20 15:35 ..

-rw-r--r-- 1 **www-data   www-data   136748 Nov 20 18:51 1FC2.pdb**

-rw-r--r-- 1 seanmurphy seanmurphy   6148 Nov 20 15:35 .DS_Store


Things to fix. Deployments generally suck. Something always breaks. 

Initial table data load is NOT working ... which is really odd.