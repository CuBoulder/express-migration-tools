# Express Migration Tools

This is the set of scripts under development for use in our upcoming migration from Web Express Drupal 7 -> Web Express Drupal 10.

## Set up

1. Install the stack needed for Drupal sites and this codebase:
    1. install python
        - `brew install python`
        - this will likely install python@3.1X which you will use in the command line like `python3.1X` as needed for th e
    1. install php
        - `brew install php`
    2. intall a local mariadb instance and start it up
        - `brew install mariadb`
        - `brew services start mariadb`
    3. install a local nginx instance and start it up
        - `brew install ngninx`
        - `brew services start nginx`
    4. edit the nginx configuation file:
        - `nano /opt/homebrew/etc/nginx/nginx.conf`
        - add the following `server` definition inside the `html` body (this is a recommended Drupal nginx configuration, I can not remember from where, maybe drupal.org? I am sure you could configure it more briefly if you want to.)
    ```
    server {
        server_name localhost;
        listen 8080;
        root <PATH_TO_YOUR_PROJECT_DIRECTORY>/web; ## <-- Your only path reference.

        location = /favicon.ico {
            log_not_found off;
            access_log off;
        }

        location = /robots.txt {
            allow all;
            log_not_found off;
            access_log off;
        }

        # Very rarely should these ever be accessed outside of your lan
        location ~* \.(txt|log)$ {
            allow 192.168.0.0/16;
            deny all;
        }

        location ~ \..*/.*\.php$ {
            return 403;
        }

        location ~ ^/sites/.*/private/ {
            return 403;
        }

        # Block access to scripts in site files directory
        location ~ ^/sites/[^/]+/files/.*\.php$ {
            deny all;
        }

        # Allow "Well-Known URIs" as per RFC 5785
        location ~* ^/.well-known/ {
            allow all;
        }

        # Block access to "hidden" files and directories whose names begin with a
        # period. This includes directories used by version control systems such
        # as Subversion or Git to store control files.
        location ~ (^|/)\. {
            return 403;
        }

        location / {
            # try_files $uri @rewrite; # For Drupal <= 6
            try_files $uri /index.php?$query_string; # For Drupal >= 7
        }

        location @rewrite {
            #rewrite ^/(.*)$ /index.php?q=$1; # For Drupal <= 6
            rewrite ^ /index.php; # For Drupal >= 7
        }

        # Don't allow direct access to PHP files in the vendor directory.
        location ~ /vendor/.*\.php$ {
            deny all;
            return 404;
        }

        # Protect files and directories from prying eyes.
        location ~*
    \.(engine|inc|install|make|module|profile|po|sh|.*sql|theme|twig|tpl(\.php)?|xtmpl|yml)(~|\.sw[op]|\.bak|\.orig|\.save)?$|^(\.(?!well-known).*|Entries.*|Repository|Root|Tag|Template|composer\.(json|lock)|web$
        {
            deny all;
            return 404;
        }

        # In Drupal 8, we must also match new paths where the '.php' appears in
        # the middle, such as update.php/selection. The rule we use is strict,
        # and only allows this pattern with the update.php front controller.
        # This allows legacy path aliases in the form of
        # blog/index.php/legacy-path to continue to route to Drupal nodes. If
        # you do not have any paths like that, then you might prefer to use a
        # laxer rule, such as:
        #   location ~ \.php(/|$) {
        # The laxer rule will continue to work if Drupal uses this new URL
        # pattern with front controllers other than update.php in a future
        # release.
        location ~ '\.php$|^/update.php' {
            fastcgi_split_path_info ^(.+?\.php)(|/.*)$;
            # Ensure the php file exists. Mitigates CVE-2019-11043
            try_files $fastcgi_script_name =404;
            # Security note: If you're running a version of PHP older than the
            # latest 5.3, you should have "cgi.fix_pathinfo = 0;" in php.ini.
            # See http://serverfault.com/q/627903/94922 for details.
            include fastcgi_params;
            # Block httpoxy attacks. See https://httpoxy.org/.
            fastcgi_param HTTP_PROXY "";
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_intercept_errors on;
            # PHP 5 socket location.
            #fastcgi_pass unix:/var/run/php5-fpm.sock;
            # PHP 7 socket location.
            fastcgi_pass localhost:9000;
        }

        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            try_files $uri @rewrite;
            expires max;
            log_not_found off;
        }

        # Fighting with Styles? This little gem is amazing.
        # location ~ ^/sites/.*/files/imagecache/ { # For Drupal <= 6
        location ~ ^/sites/.*/files/styles/ { # For Drupal >= 7
            try_files $uri @rewrite;
        }

        # Handle private files through Drupal. Private file's path can come
        # with a language prefix.
        location ~ ^(/[a-z\-]+)?/system/files/ { # For Drupal >= 7
            try_files $uri /index.php?$query_string;
        }

        # Enforce clean URLs
        # Removes index.php from urls like www.example.com/index.php/my-page --> www.example.com/my-page
        # Could be done with 301 for permanent or other redirect codes.
        if ($request_uri ~* "^(.*/)index\.php/(.*)") {
            return 307 $1$2;
        }
    }
    ```
2. setup a new user in mariadb to use for migrating sites (you could probably just use your mac's admin account and password):
    1. type `mariadb -u root` in terminal
        - you should be granted the root user acces to the shell if this is the first time logging into mariadb shell. If not, I am not sure what to do...
    2. We are creating a user and granting this user all priviledges to all databases. be sure to change 'username' and 'userpassword' to whatever you want. Make a note of them.
        - `CREATE USER 'username'@'localhost' IDENTIFIED BY 'userpassword';`
        - `GRANT ALL PRIVILEGES ON *.* TO 'username'@localhost IDENTIFIED BY 'userpassword';`
3. clone the code base of this repo to a directory on your local computer
4. create a python virtual environment in this directory and activate it
    - `python3.1X -m venv .venv`
    - `source .venv/bin/activate`
    - once the virtual environment is active you can simply use the `python` and `pip` (python's package manager kind of like npm) without the version numbers appended.
5. install dependencies
    - `pip install -r requirements.txt`
6. Create a .env file in the root level of the project directory and add the following lines using the username and and userpassword from step 2.:
    ```
    DB_USER=<username>
    DB_PASSWORD= <userpassword>
    ```

## Steps to migrate a site

This assumes you already have the venv activated (see above) and that you are logged in via terminus.

1. copy a site to your local computer
    1. make sure you are in the root level of the project's directory
    2. type `python migrate.py --site <SITENAME> ----extract-psa-from-remote`
    3. this will take a little while but when it completes check in the `sites` directory to see if all the following has been created:
        - code directory
        - files directory
        - data.xml
        - database.sql
./d migrate:rollback --tag=express; and ./d pmu migrate_express; and ./d en migrate_express