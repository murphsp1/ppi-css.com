deployment.markdown

Ok, I just pulled down the latest and greatest code from github.

Now, after shuffling directories around, I:


    sudo service apache2 restart 

    sudo chown -R www-data:www-data /var/www

    sudo ./manage.py collectstatic


     ImportError: Could not import settings 'myproject.settings'

make sure that wsgi.py gets updated


[Tue Dec 03 15:54:33 2013] [error] OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: NO)")
[Tue Dec 03 15:56:38 2013] [error] Internal Server Error: /css0/get_table_data/



Now, debug = True doesn't work
Search does not work


http://173.255.119.115/admin/
 "Access denied for user 'root'@'localhost' (using password: NO)")
