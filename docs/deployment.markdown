deployment.markdown

Ok, I just pulled down the latest and greatest code from github.

Now, after shuffling directories around, I:


    sudo service apache2 restart 

    sudo chown -R www-data:www-data /var/www

    sudo ./manage.py collectstatic


     ImportError: Could not import settings 'myproject.settings'

make sure that wsgi.py gets updated

Now, debug = True doesn't work
Search does not work


http://173.255.119.115/admin/
 "Access denied for user 'root'@'localhost' (using password: NO)")
