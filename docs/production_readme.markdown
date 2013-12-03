## Introduction ##
This longer-than-initially planned article walks one through the process of deploying a non-standard Django application on a virtual instance provisioned not from Amazon Web Services but from Google Compute Engine. This means we will be creating our own virtual machine in the cloud and installing all necessary software to have it serve content, run the Django application, and hanlde the database all in one. Clearly, I do not expect an overwhelming amount of traffic to this site. Also, note that Google Compute Engine is very different from Google App Engine.  

What makes this app "non-standard" is its use of both the Numpy and Scipy packages to perform fast computations. Numpy and Scipy are based on C and Fortran respectively and both have complicated compilation dependencies. Binaries may be available in some cases but are not always available for your preferred deployment environment. Most importantly, these two libraries prevented me from deploying my app to either Google App Engine (GAE) or to Heroku. I'm not saying that it is impossible to deploy Numpy- or Scipy-dependent apps on either service. However, neither service supports apps dependent on both Scipy and Numpy out-of-the-box although a limited amount of Googling suggests it can be be done.

In fact, GAE could have been an ideal solution if I had re-architected my app, separating the Django application from the computational code. I could run the Django application on GAE and allowed it to spin up a GCE instance as needed to perform the computations. One concern with this idea is the latency involved in spinning up the virtual instance for computation.  Google Compute Engine instances spring to life quickly but not instantaneously. Maybe I'll go down this path for version 2.0 if there is a need.

## Motivations ##
I wrote this post for two primary reasons, one ideological and one practical.  First, I believe that a large gap exists between available online tutorials that walk you through the deployment of a toy-application and the core documentation that exists for programming languages and web frameworks. 

### Tutorials vs Documentation
An ideal tutorial should be simple enough not to lose the novice but, by doing so, often does not prepare one for the pitfalls and mandatory debugging that the novice or expert will face. Further, a tutorial, with all steps sequentially laid out in detail for clarity, is not representative of how exploration occurs in the real world.

The core documentation is fantastic for the expert that already has a good understanding of how the larger pieces fit together. However, the core documentation obviously can't cover everything that one needs to know and must make numerous assumptions about a person's related skill set and mental models. Further, it is often very difficult to formulate the next question one must ask after reading the documention--you simply don't know what you don't know. Sample code that shows you how a particular example is implemented can be useful to help formulate this next question but it can also be a crutch, solving the immediate problem without 

Please note that this isn't to disparage the efforts of the tutorial writers or the language documenters in any way (thank you for your efforts).

### Practical Needs
Second, this is the document that I created as I worked my way through the deployment process. As I went, I found myself continually assembling information from a large variety of sources--both online and person-to-person--each of which either only partially applicable to my particular problem or addressing a small segment of the whole. Thus, there is an immediate intent to help the reader with any related problems.

More importantly, and wandering back to the philosophical side of the coin, this is my stab at bridging the gap between the too-simple-tutorials and the API documentation: capturing my thought process, the good and the bad, the right and the wrong, and exposing the particular set of attempts, failures, frustrations, and iterations that led me to the outcome that you will read about below (if you have the required stamina;). 

## Big Picture Lessons Learned ##

The single largest takeaway from this experience was the elusively obvious statement--be prepared to run through the process at least a few times. I don't think that most people expect to get something that they have never done before right the first time. However, I don't think that the full ramifications of this fact are appreciated until further reflection.


First, if the project is lengthy and complex or the work will be punctuated with numerous distractions, 

First, let's assume that the project is either lengthy or complex or that the work will be punctuated with numerous distractions.
Thus, each time you start over, you must repeat a set of steps, possibly in different programming languages, that were at least somewhat unknown to you before. 

recording the details of each and every step simply make it possible to recreate rapidly the progress to that point. Trust me, you probably will not remember the particular set of required flags for each command line entry you need to get everything working, especially when you got those flags wrong the first 5 or 6 times you tried. Either  

Second, when a particular step goes south (and at least one will), your documentation can become a spring board for working out your problem. Did you miss a step? Did you screw up a previous step? Did you 

When I taught more group classes, I had an "unlimited email" policy. I would answer any and every question emailed to me if the student followed a simple set of rules. I refused to answer any email that was simply a plee for help. The "I just don't get this problem" one line email got an equally short reply to the student.  For me to answer, the student must explain in writing the set of steps that got him or her to the current blocked state, the specific error or mistake that occurred, and some guesses as to what might have gone wrong. More often than not, the simple act of writing out this email was enough for the student to push forward. Make your assumptions explicit and often the problem will become self evident.




## Initial Configuration ##
One criticism that I have of **some** of the tutorial blogs that I have seen is that they don't always offer the intimate details of their production environments. I would like to see every technical blog come with a requirements.txt file.

To remedy that, here are all of the sordid details:

- gcutil version 1.11.0 - to connect to the GCE instance
- 



## Google Compute Engine
I will assume that you can provision your own instance in GCE either using gcutil at the command line or through the cloud services web interface provided by Google.

#need to configure GCE firewall settings
gcutil addfirewall http2 --description="Incoming http allowed." --allowed="tcp:http" --project="1040981951502"


## 1. Update the Instance and Install Tools ##
After the instance boots, we must ssh in to the instance for the first time via:


Next, we need to update the default packages install on the virtual instance:

    sudo apt-get update
    sudo apt-get upgrade

and install some basic needed development tools:

    sudo apt-get --yes install make
    sudo apt-get --yes install wget
    sudo apt-get --yes install git

and install some basic Python-related tools:

    sudo apt-get --yes install python-setuptools
    sudo easy_install pip
    sudo pip install virtualenv

Note that in many of my sudo apt-get commands I include --yes. This flag just prevents me from having to type "Y" to agree to the download of a file.

## 2. Install Numpy and Scipy (SciPy requires Fortran compiler) ##

To install SciPy, Python's general purpose scientific computing library from which we need a single function, we need the Fortran compiler
    
    sudo apt-get --yes install gfortran

and then we need Numpy and Scipy and everything else

    sudo apt-get --yes install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

Finally, we need to add ProDy, a protein dynamics and sequence analysis package for Python.

    sudo pip install prody


## Install and Configure the Database (MySQL) ##

    sudo apt-get --yes install mysql-server

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
You have seemingly two choices for your web server, either the tried and true Apache (now up to version 2+) or nginx. <a href="http://wiki.nginx.org/Main" target="_blank">Nginex</a> is supposed to be the new sexy when it comes to web servers but this newness comes at a price of less documentation/tutorials online. Thus, let's play it safe and go with Apach2.



### First Attempt ###

First things first, we need to install apache2 and mod_wsgi. Mod_wsgi is an Apache HTTP server module that provides a WSGI compliant interface for web applications developed in Python. 

    sudo apt-get --yes install apache2 libapache2-mod-wsgi

This seems to be causing a good number of problems. In my Django error logs I see:

    [Mon Nov 25 13:25:27 2013] [error] [client 108.21.2.20] Premature end of script headers: wsgi.py

and in my 

    cat /var/log/apache2/error.log

I see things like:

    [Sun Nov 24 16:15:02 2013] [warn] mod_wsgi: Compiled for Python/2.7.2+.
    [Sun Nov 24 16:15:02 2013] [warn] mod_wsgi: Runtime using Python/2.7.3.

with the occasional segfault:

    [Mon Nov 25 00:02:55 2013] [notice] child pid 12532 exit signal Segmentation fault (11)
    [Mon Nov 25 00:02:55 2013] [notice] seg fault or similar nasty error detected in the parent process

### Second Attempt ###
A little bit of Googling suggests that this could be the result of a number of issues with mod_wsgi

Initially, I simulataneously installed libapache2-mod-wsgi but this potentially caused a large number of pr

    libapache2-mod-wsgi


    sudo apt-get install apache2-prefork-dev

Now, we need to grab mod_wsgi:

    wget https://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz

    tar -zxvf mod_wsgi-3.4.tar.gz
    cd mod_wsgi-3.4
    ./configure
    make
    sudo make install

Once mod_wsgi is intalled, the apache server needs to be told about it. On Apache 2, this is done by adding the load declaration and any configuration directives to the /etc/apache2/mods-available/ directory.

The load declaration for the module needs to go on a file named wsgi.load (in /etc/apache2/mods-available/ directory), which contains only this:

    LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

Then you have to activate the wsgi module with:

    a2enmod wsgi

Note: a2enmod stands for "apache2 enable mod", this executable create the symlink for you. Actually a2enmod wsgi is equivalent to:

    cd /etc/apache2/mods-enabled
    ln -s ../mods-available/wsgi.load
    ln -s ../mods-available/wsgi.conf # if it exists



By default, the following page is served by the install:

    /usr/share/apache2/default-site/index.html

Now we need to update the virtual hosts settings on the server.  For Debian, this is here:
/etc/apache2/sites-enabled/000-default 


Restart the service

    sudo service apache2 restart 



sudo chown -R www-data:www-data /var/www








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

## Configuring Apache for Our Django Project ##

First, let's disable the 

    sudo a2dissite default



There will be aliases in the virtual host configuration file that let the apache server know about this structure. Fortunately, I have included the ppi-css.conf file in the repository and it must be moved into position:

    sudo cp /var/www/ppi-css.com/django/ppi-css.com/ppi-css.conf /etc/apache2/sites-available/ppi-css.com

Next, we must enable the site using the following command:

    sudo a2ensite ppi-css.com

and we must reload the apache2 service (remember this command as you will probably be using it alot)
    
    sudo service apache2 reload

Now, when I restarted or reloaded the apache2 service, I get the following error message:

    ERROR MESSAGES:
    [....] Restarting web server: apache2apache2: apr_sockaddr_info_get() failed for (none)
    apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName
     ... waiting apache2: apr_sockaddr_info_get() failed for (none)
    apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName
    . ok 
    Setting up ssl-cert (1.0.32) ...
    hostname: Name or service not known

To remove this, I simply added the following line:

    ServerName localhost

to the /etc/apache2/apache2.conf file using vi. A quick 

    sudo service apache2 reload

shows that the error message no longer appeared.

## Install a Few More Python Packages ##

Remove all of the various bits and pieces for numpy and scipy from the requirements file and then do:

    sudo pip install -r /var/www/ppi-css.com/django/ppi-css.com/requirements.txt


## Database Migrations ##

Before we can perform the needed database migrations, we need to update the database section of settings.py. It should look like below:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'USER': 'root',    
            'PASSWORD': 'INSERT_YOUR_PASSWORD',
            'HOST': '',         # Set to empty string for localhost. 
            'PORT': '',         # Set to empty string for default.
        }
    }

    python /var/www/ppi-css.com/django/ppi-css.com/manage.py syncdb
    python /var/www/ppi-css.com/django/ppi-css.com/manage.py migrate


## Deploying Your Static Files ##
Static files, your css, javascript, images, and other unchanging files, can be problematic for new Django developers. When developing, Django is more than happy to serve your static files for you given their 

The key to this is your settings.py file. In this file, we see:

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = ''      #os.path.join(PROJECT_ROOT, 'static')

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/static/'

    # Additional locations of static files
    STATICFILES_DIRS = (
        #os.path.join(PROJECT_ROOT,'static'),
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )      

For production, STATIC_ROOT must contain the directory where Apache2 will serve static content from. In this case, it should look like this:

    STATIC_ROOT = '/var/www/ppi-css.com/htdocs/static'

For development, STATIC_ROOT looked like:

    STATIC_ROOT = ''

Next, Django comes with a handy mechanism to round up all of your static files (in the case that they are spread out in separate app directories if you have a number of apps in a single project) and push them to a single parent directory when you go into production.

    ./manage.py collectstatic

Be very careful when going into production.  If any of the directories listed in the STATICFILES_DIRS variable do not exist on your production server, collectstatic will fail and will not do so gracefully. The <a href="https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/" target="_blank">official Django documentation</a> has a pretty good description of the entire process.



MUST UPDATE wsgi.py with directory paths!

What about media path??


Update settings.py
    MEDIA_ROOT = "/var/www/ppi-css.com/htdocs/media/" #os.path.join(PROJECT_ROOT, 'media')


    ALLOWED_HOSTS = [
            '.ppi-css.com', 
            'ppi-css.com',
    ]

WHERE wsgi.py is
/home/seanmurphy/myproject/myproject/myproject

WHERE STATIC IS:
/home/seanmurphy/myproject/myproject/myproject/myapp/static


http://192.158.29.226/myapp/init_table_data_load/

but need to update the original source to have a proper path

From the command line in the directory with "manage.py" type:


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



## Some Debuggin Hints ##

Inevitably, things won't work on your remote server. Obviously leaving your application in Debug mode is ok for a very brief time while you are trying to deploy but there are other things to check as well.


Is server running?
sudo service apache2 status

What do the apache error logs say?
cat /var/log/apache2/error.log


cat /var/www/ppi-css.com/logs/error.log 

Also, it is never a bad idea to log into MySQL and take a look at the django_test database

gcutil --project="1040981951502" pull test2 /home/seanmurphy/myproject.tar.gz ./

gcutil --service_version="v1beta16" --project="1040981951502" ssh  --zone="europe-west1-a" "test2"


## Virtual Environment - Where Did It Go? ##
If you noticed, I did have a requirements.txt file in my project. When I started doing local development on my trusty Mac Book Air, I used <a href="https://pypi.python.org/pypi/virtualenv" target="_blank">virtualenv</a>, an amazing tool. However, I had some difficulties getting Numpy and Scipy properly compiled and included in the virtualenv on my server whereas it was pretty simple to get them up and running in the system's default Python installation. Conversing with some of my more Django-experienced friends, they reassured me that while this wasn't a best practice, it wasn't a mortal sin either.








You need to do two things

In the Amazon Web Service admin panel, create an elastic IP in the same region as your instance and associate that IP with your that instance (IPs cost nothing while they are associated with an instance, but do cost if not).
Add a A record to the DNS record of your domain mapping the domain to the elastic IP address assigned in (1). 

Your domain provide should either give you some way to set the A record (the IP address), or it will give you a way to edit the nameservers of your domain.




## Getting to Know Git and Git Hub ##
Git or another code versioning tool is a fact of life for any developer. While the learning curve for the novice may be steep (or vertical), it is essential to climb this mountain as quickly as possible.

As powerful as GIT can be, I found myself using only a few commands.

First, I used git add with several different flags to stage files before committing. To stage all new and modified files (but not deleted files), use:

    git add .

To stage all modified and deleted files (but not new files), use:

    git add -u

Or, if you want to be lazy and want to stage everything everytime (new, modified, and deleted files), use:

    git add -A

Next, the staged files must be committed and then pushed to GitHub.

    git commit -m "insert great string for documentation here"
    git push -u origin master


## Commands in Local Development Environment ##
While Django isn't the most lightweight web framework in Python (hello Flask and others), "launching" the site in the local development environment is pretty simple. Compare the command line commands needed below to the rest of the blog. (Note that I am running OS X 10.9 Mavericks on a Mac Book Air with 8 GB of 1600 MHz DDR 3.)

First, start the local postgres server:

    postgres -D /usr/local/var/postgres 

Next start the local development web server using the <a href="https://code.google.com/p/django-command-extensions/wiki/RunServerPlus" target="_blank">django-command-extensions</a> that enables debugging of the site in the browser.

    python manage.py runserver_plus   


Once a model has changed, we needed to make a migration using South and then apply it with the two commands below:

    ./manage.py schemamigration css0 --auto
    ./manage.py migrate css0   

## References ##
There are a ton of different tutorials out there to help you with all aspects of deployment. Of course, piecing together the relevant parts may take some time.

<a href="https://developers.google.com/compute/docs/quickstart" target="_blank">A Simple Tutorial for GCE</a> - This is a very basic tutorial that doesn't get into the details of getting a very simple configuration up and running on GCE. 

<a href="http://www.control-escape.com/web/configuring-apache2-debian.html" target="_blank">Some Background on Apache Configuration Files on Debian</a> - Understanding the apache2 configuration files is important for getting this to work correctly and it would appear that Debian does things a bit non-standard.  

<a href="https://library.linode.com/web-servers/apache/installation/debian-7-wheezy" target="_blank">Apache 2 Web Server on Debian 7 (Wheezy)</a>

<a href="http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/" target="_blank">Deploy Django on Apache with Virtualenv and mod_wsgi</a>

<a href="http://www.djangobook.com/en/2.0/chapter12.html" target="_blank">The Django Book - Deploying Django, Chapter 12</a>

<a href="http://www.apreche.net/complete-single-server-django-stack-tutorial/" target="_blank">Complete Single Server Django Stack Tutorial</a>

<a href="http://adambard.com/blog/start-to-finish-serving-mysql-backed-django-w/" target="_blank">Start to Finish - Serving Django with UWSGI/NGINX on EC2</a>

<a href="http://pragmaticstartup.wordpress.com/2011/04/02/non-techie-guide-to-setting-up-django-apache-mysql-on-amazon-ec2/" target="_blank">Non-techie Guide to setting up Django, Apache, MySQL on Amazon EC2</a>

<a href="http://nickpolet.com/blog/1/" target="_blank">Deploying Django on Amazon EC2 Server</a>

<a href="http://blog.hguochen.com/blog/2013/09/deploying-python-django-on-ec2-linux-instance/" target="_blank">Deploying Python, Django on EC2 Linux Instance

<a href="https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/" target="_blank">How to use Django with Apache and mod_wsgi</a>

<a href="http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/" target="_blank">Setting up Django with Nginx, Gunicorn, virtualenv, supervisor and PostgreSQL</a>