sudo chmod -R 777 sites/ucb-aerospaceventures/code/web/sites/default/files
./sites/ucb-aerospaceventures/code/d --root=sites/ucb-aerospaceventures/code si boulder_profile  --db-url="mysql://root:pass@localhost:3306/ucbaerospaceventures" --site-name="ucb-aerospaceventures" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --site-mail=webexpress_noreply@colorado.edu --yes
ln -s ./vendor/bin/drush sites/ucb-aerospaceventures/code/d
composer require simplehtmldom/simplehtmldom --working-dir=sites/ucb-aerospaceventures/code --no-interaction
composer update --working-dir=sites/ucb-aerospaceventures/code --no-interaction
git clone https://github.com/CuBoulder/tiamat10-project-template.git sites/ucb-aerospaceventures/code
mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS ucbaerospaceventures;"
