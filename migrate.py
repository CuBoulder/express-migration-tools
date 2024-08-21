#!/usr/bin/env python3

import argparse
import subprocess
import os
import shutil
import sqlalchemy
import phpserialize
import shlex
import yaml


parser = argparse.ArgumentParser(description='Express Migration Tool')

parser.add_argument('-s', '--site', help='Sitename')
parser.add_argument('--extract-sql-from-remote', action='store_true', help='Extract SQL from Pantheon')
parser.add_argument('--extract-files-from-remote', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--extract-psa-from-remote', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--extract-psa-from-remote-localdev', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--shortcode-fix', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--create-local-training-site', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--delete-users', action='store_true', help='Delete users')
parser.add_argument('--enable-firstchild', action='store_true', help='Enable firstchild')

args = parser.parse_args()

def run_command(cmd):
    print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    #print(output.stdout)

    if len(output.stderr) > 0:
        print(output.stderr)

    return output

def create_local_db(sitename):
    print(f'Creating local DB "{sitename}"...')
    sitename_clean = sitename.replace('-', '')
    run_command(f'mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS {sitename_clean};"')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def extract_sql_from_remote(sitename):
    print(f'Extract remote SQL...')
    os.makedirs(f'sites/{sitename}', exist_ok=True)
    run_command(f'terminus remote:drush {sitename}.live -- sql-dump --skip-tables-list=cache,cache_* > sites/{sitename}/database.sql')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def install_drupal(sitename):
    print(f'Installing Drupal...')
    sitename_clean = sitename.replace('-', '')
    run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code si boulder_profile  --db-url="mysql://root:pass@localhost:3306/{sitename_clean}" --site-name="{sitename}" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --site-mail=webexpress_noreply@colorado.edu --yes')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def fetch_destination_connection_information(site):

    dstsite = 'ucbprod-' + site[4:]


    cmd_connection_info = f'terminus connection:info {dstsite}.live --format=yaml'
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)

    print(connection_info)

    return connection_info

def install_destination_drupal(sitename):
    print(f'Installing Destination Drupal...')

    dstsite = 'ucbprod-' + sitename[4:]

    install_cmd = f'terminus remote:drush {dstsite}.live -- si boulder_profile --site-name="{sitename}" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --site-mail=webexpress_noreply@colorado.edu --yes'
    print(install_cmd)
    run_command(install_cmd)


    # fetch_destination_connection_information(sitename)

    # sitename_clean = sitename.replace('-', '')

def install_training_destination_drupal(sitename):
    print(f'Installing Destination Drupal...')

    dstsite = sitename

    install_cmd = f'terminus remote:drush {dstsite}.live -- si boulder_profile --site-name="Express Training" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --site-mail=webexpress_noreply@colorado.edu --yes'
    print(install_cmd)
    run_command(install_cmd)

def fetch_destination_database(sitename):
    print(f'Fetching Destination Drupal DB...')

    # ci = fetch_destination_connection_information(sitename)
    # dstdb = ci['mysql_command']
    # print(dstdb)

    dstsite = 'ucbprod-' + sitename[4:]

    sqldump_cmd = f'terminus remote:drush {dstsite}.live -- sql-dump --skip-tables-list=cache,cache_* > sites/{sitename}/code/database-dst.sql'
    print(sqldump_cmd)
    run_command(sqldump_cmd)

def fetch_training_destination_database(sitename):
    print(f'Fetching Destination Drupal DB...')

    # ci = fetch_destination_connection_information(sitename)
    # dstdb = ci['mysql_command']
    # print(dstdb)

    dstsite = sitename

    sqldump_cmd = f'terminus remote:drush {dstsite}.live -- sql-dump --skip-tables-list=cache,cache_* > sites/{sitename}/code/database-training.sql'
    print(sqldump_cmd)
    run_command(sqldump_cmd)

def import_destination_database(sitename):
    print("Importing destination database...")

    sitename_clean = sitename.replace('-', '')

    import_cmd = f'mariadb -u root -ppass {sitename_clean} < sites/{sitename}/code/database-dst.sql'

    print(import_cmd)
    run_command(import_cmd)

def import_training_destination_database(sitename):
    print("Importing destination database...")

    sitename_clean = sitename.replace('-', '')

    import_cmd = f'mariadb -u root -ppass {sitename_clean} < sites/{sitename}/code/database-training.sql'

    print(import_cmd)
    run_command(import_cmd)




def create_drush_symlink(sitename):
    print(f'Creating drush symlink...')
    run_command(f'ln -s ./vendor/bin/drush sites/{sitename}/code/d')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def create_migrate_express_symlink(sitename):
    print(f'Creating migrate_express symlink...')
    run_command(f'ln -s ~/Projects/migrate_express sites/{sitename}/code/web/modules/custom/migrate_express')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def create_dataxml_symlink(sitename):
    print(f'Creating data.xml symlink...')
    run_command(f'ln -s ../../data.xml sites/{sitename}/code/web/data.xml')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def create_training_dataxml_symlink(sitename):
    print(f'Creating data.xml symlink...')
    cmd = f'ln -s ../../../ucb-{sitename[12:]}/data.xml sites/{sitename}/code/web/data.xml'
    print(cmd)
    run_command(cmd)
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def enable_firstchild(sitename):
    with engine.connect() as conn:
        try:
            menu_ids = []
            firstchild_result = conn.execute(sqlalchemy.text("select id from menu_link_content_data where link__uri = 'internal:/<none>';"))
            for result in firstchild_result:
                menu_link_content_data_sql = "update menu_link_content_field_revision set link__uri = 'route:<none>', link__options = 'a:1:{s:15:\"menu_firstchild\";a:1:{s:7:\"enabled\";i:1;}}' WHERE link__uri = 'internal:/<none>';"
                conn.execute(sqlalchemy.text(menu_link_content_data_sql))

                menutree_sql = "update menu_tree SET options = 'a:1:{s:15:\"menu_firstchild\";a:1:{s:7:\"enabled\";i:1;}}'  WHERE metadata like '%\"" + str(result.id) + "\"%';"
                conn.execute(sqlalchemy.text(menutree_sql))

            conn.execute(sqlalchemy.text("TRUNCATE cache_config;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_container;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_data;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_default;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_discovery;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_entity;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_menu;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_render;"))
            conn.execute(sqlalchemy.text("TRUNCATE cache_toolbar;"))

        except Exception as e:
            print(f"Exception: {e}")




# update menu_link_content_field_revision set link__uri = 'route:<none>', link__options = 'a:1:{s:15:"menu_firstchild";a:1:{s:7:"enabled";i:1;}}' WHERE link__uri = 'internal:/<none>';

def set_configuration(sitename):
    print(f'Set configuration variables...')

    with engine.connect() as conn:
        try:

            site_frontpage = ''
            frontpage_result = conn.execute(sqlalchemy.text("select value from variable where name = 'site_frontpage';"))
            for result in frontpage_result:
                site_frontpage = str(phpserialize.loads(result.value, decode_strings=True)).strip()

            print(f"{site_frontpage}")

            frontpagealias_result = conn.execute(sqlalchemy.text(f"select alias from url_alias where source = '{site_frontpage}';"))
            frontpagealias = ""
            for result in frontpagealias_result:
                frontpagealias = "/" + str(result.alias).strip()

            print(f'Source homepage is {site_frontpage}, mapped to {frontpagealias}.')
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set system.site page.front "/{site_frontpage}" --yes')



            site_info_body = ''
            site_info_body_result = conn.execute(sqlalchemy.text("select value from variable where name = 'site_info_body';"))
            for result in site_info_body_result:
                site_info_body = str(phpserialize.loads(result.value, decode_strings=True)['value']).strip()

            print(f"{site_info_body}")
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set ucb_site_configuration.contact_info general.0.value.value {shlex.quote(site_info_body)} --yes')
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set ucb_site_configuration.contact_info general.0.value.format "wysiwyg" --yes')
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set ucb_site_configuration.contact_info general.0.visible 1 --yes --input-format=yaml')
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set ucb_site_configuration.contact_info general_visible 1 --yes --input-format=yaml')

            cu_site_affiliation_options = ''
            cu_site_affiliation_options_result = conn.execute(sqlalchemy.text("select value from variable where name = 'cu_site_affiliation_options';"))
            for result in cu_site_affiliation_options_result:
                cu_site_affiliation_options = str(phpserialize.loads(result.value, decode_strings=True)).strip()

            print(f"Affiliation: {cu_site_affiliation_options}")
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set ucb_site_configuration.settings site_affiliation {cu_site_affiliation_options} --yes')



            cfg_gtm = ''
            gtm_result = conn.execute(sqlalchemy.text("select value from variable where name = 'google_container_id';"))
            for result in gtm_result:
                cfg_gtm = str(phpserialize.loads(result.value, decode_strings=True)).strip()
            if(len(cfg_gtm)):
                print(f'GTM: {cfg_gtm}')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set --input-format=yaml google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 tag_container_ids [GTM-M3DX2QP,{cfg_gtm}]  --yes')

                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.data_layer dataLayer --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.include_classes 0 --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.allowlist_classes "" --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.blocklist_classes "" --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.include_environment 0 --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.environment_id "" --yes')
                run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set google_tag.container.GTM-M3DX2QP.65de22067902c7.57590325 advanced_settings.gtm.{cfg_gtm}.environment_token "" --yes')




            sitename_result = conn.execute(sqlalchemy.text("select value from variable where name = 'site_name';"))
            cfg_sitename = ''
            for result in sitename_result:
                cfg_sitename = str(phpserialize.loads(result.value, decode_strings=True)).strip()


            print(f"Setting sitename to {cfg_sitename}")

            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set system.site name "{cfg_sitename}" --yes')
            # output = subprocess.run([cmd], shell=True, capture_output=True)
            # print(output.stdout)
            # print(output.stderr)

            thememap = {}
            thememap['cuclassic'] = 'default'  # Should not exist
            thememap['cuduo'] = 'default'  # Should not exist
            thememap['cuflat'] = 'default'  # Should not exist
            thememap['cuhighlight'] = 'highlight'
            thememap['cuivory'] = 'ivory'
            thememap['culayers'] = 'layers'
            thememap['cuminimal'] = 'minimal'
            thememap['cumodern'] = 'modern'
            thememap['curise'] = 'rise'
            thememap['cuseven'] = 'default'  # Should not exist
            thememap['cushadow'] = 'shadow'
            thememap['cusimple'] = 'simple'
            thememap['cuspirit2018'] = 'default'  # Should not exist
            thememap['cuspirit'] = 'spirit'
            thememap['cuswatch'] = 'swatch'
            thememap['cutradition'] = 'tradition'

            # 0 = black
            # 1 = white
            # 2 = light gray
            # 3 = dark gray




            themeheadercolormap = {}
            themeheadercolormap['highlight'] = 1
            themeheadercolormap['ivory'] = 0  # has an option
            themeheadercolormap['layers'] = 3
            themeheadercolormap['minimal'] = 1  # white logo?
            themeheadercolormap['modern'] = 0  # has an option
            themeheadercolormap['rise'] = 3  # has an option
            themeheadercolormap['shadow'] = 0
            themeheadercolormap['simple'] = 1  # has an option, white logo
            themeheadercolormap['spirit'] = 0  # has an option
            themeheadercolormap['swatch'] = 0
            themeheadercolormap['tradition'] = 0  # has an option

            'banner_color: white, black, light, dark'

            # use_breadcrumbs -> ucb_breadcrumb_nav
            # use_action_menu -> ucb_secondary_menu_position
            # headings -> todo


            print(f"Getting theme settings...")
            themename_result = conn.execute(sqlalchemy.text("select value from variable where name = 'theme_default';"));
            for result in themename_result:
                themename = str(phpserialize.loads(result.value, decode_strings=True)).strip()
            print(f'  {themename} found. Setting ucb_menu_style to "{thememap[themename]}".')

            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_menu_style "{thememap[themename]}" --yes')

            ucb_header_color = themeheadercolormap[thememap[themename]]
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_header_color "{ucb_header_color}" --yes')

            themesettings_result = conn.execute(sqlalchemy.text(f"select value from variable where name = 'theme_{themename}_settings';"));

            themesettings = {}

            for result in themesettings_result:
                themesettings = phpserialize.loads(result.value, decode_strings=True)

            brand_bar_color = '1'
            if 'brand_bar_color' in themesettings:
                if themesettings['brand_bar_color'] == 'white':
                    brand_bar_color = '0'
                if themesettings['brand_bar_color'] == 'black':
                    brand_bar_color = '1'

            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_campus_header_color "{brand_bar_color}" --yes')

            ucb_breadcrumb_nav = '1'
            if 'use_breadcrumbs' in themesettings:
                if themesettings['use_breadcrumbs'] == 0:
                    ucb_breadcrumb_nav = 0
                if themesettings['use_breadcrumbs'] == 1:
                    ucb_breadcrumb_nav = 1
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_breadcrumb_nav "{ucb_breadcrumb_nav}" --yes')

            ucb_secondary_menu_position = '0'
            if 'use_action_menu' in themesettings:
                print(themesettings['use_action_menu'])

                if themesettings['use_action_menu'] == 0:
                    ucb_secondary_menu_position = 'above'
                if themesettings['use_action_menu'] == 1:
                    ucb_secondary_menu_position = 'inline'
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_secondary_menu_position "{ucb_secondary_menu_position}" --yes')


            use_sticky_menu = '0'
            use_sticky_menu_result = conn.execute(sqlalchemy.text("select value from variable where name = 'use_sticky_menu';"))
            for result in use_sticky_menu_result:
                use_sticky_menu = str(phpserialize.loads(result.value, decode_strings=True)).strip()
            run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set boulder_base.settings ucb_sticky_menu "{use_sticky_menu}" --yes')
        except Exception as e:
            print(f"Exception: {e}")


def load_sql_to_local_db(sitename):
    print(f'Loading SQL to local source DB...')
    sitename_clean = sitename.replace('-', '')
    run_command(f'mariadb -u root -ppass {sitename_clean}src < sites/{sitename}/database.sql')
    run_command(f'mariadb -u root -ppass {sitename_clean}src < webform_fix.sql')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def load_sql_to_local_db_dst(sitename):
    print(f'Loading SQL to local source DB...')
    sitename_clean = sitename.replace('-', '')
    run_command(f'mariadb -u root -ppass {sitename_clean} < sites/{sitename}/database.sql')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def clone_template(sitename):
    print(f'Clone template...')
    run_command(f'git clone https://github.com/CuBoulder/tiamat10-project-template.git sites/{sitename}/code')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def composer_update(sitename):
    print(f'Running composer update...')
    run_command(f'composer update --working-dir=sites/{sitename}/code --no-interaction')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)
    run_command(f'composer require simplehtmldom/simplehtmldom --working-dir=sites/{sitename}/code --no-interaction')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def set_files_permissions(sitename):
    print(f'Setting files directory permissions...')
    run_command(f'sudo chmod -R 777 sites/{sitename}/code/web/sites/default/files')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def update_settings_file(sitename):
    print(f'Updating settings file...')

    sitename_clean = sitename.replace('-', '')

    os.chmod(f'sites/{sitename}/code/web/sites/default/settings.php', 0o644)

    migrate_db_config = f"""

    $databases['migrate']['default'] = array (
      'database' => '{sitename_clean}src',
      'username' => 'root',
      'password' => 'pass',
      'prefix' => '',
      'host' => 'localhost',
      'port' => '3306',
      'isolation_level' => 'READ COMMITTED',
      'namespace' => 'Drupal\\mysql\\Driver\\Database\\mysql',
      'driver' => 'mysql',
      'autoload' => 'core/modules/mysql/src/Driver/Database/mysql/',
    );
    """

    with open(f'sites/{sitename}/code/web/sites/default/settings.php', 'a') as settings:
        settings.write(migrate_db_config)
        settings.write("$settings['file_private_path'] = $app_root . 'sites/default/files/private';")


def update_training_settings_file(sitename):
    print(f'Updating settings file...')

    sitename_clean = sitename.replace('-', '')

    os.chmod(f'sites/{sitename}/code/web/sites/default/settings.php', 0o644)

    migrate_db_config = f"""

    $databases['migrate']['default'] = array (
      'database' => 'ucb{sitename_clean[11:]}src',
      'username' => 'root',
      'password' => 'pass',
      'prefix' => '',
      'host' => 'localhost',
      'port' => '3306',
      'isolation_level' => 'READ COMMITTED',
      'namespace' => 'Drupal\\mysql\\Driver\\Database\\mysql',
      'driver' => 'mysql',
      'autoload' => 'core/modules/mysql/src/Driver/Database/mysql/',
    );
    """

    print(migrate_db_config)

    with open(f'sites/{sitename}/code/web/sites/default/settings.php', 'a') as settings:
        settings.write(migrate_db_config)
        settings.write("$settings['file_private_path'] = $app_root . 'sites/default/files/private';")





def extract_files_from_remote(sitename):
    print('Extracting files...')
    os.makedirs(f'sites/{sitename}/files', exist_ok=True)

    run_command(f'terminus local:getLiveFiles {sitename}.live --overwrite')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

    run_command(f'tar -xzvf ~/pantheon-local-copies/files/{sitename}-files.tgz -C sites/{sitename}')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

    os.rename(f'sites/{sitename}/files_live', f'sites/{sitename}/files')

def generate_dataxml(sitename):
    print("Generating XML...")
    run_command(f'python express-extract.py --site={sitename}-src > sites/{sitename}/data.xml')
    #output = subprocess.run([cmd], shell=True, capture_output=True)
    #print(output.stdout)
    #print(output.stderr)

def delete_users(sitename):
    print('Deleting users...')
    output = run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code sqlq "SELECT GROUP_CONCAT(name) FROM users_field_data"')
    #output = subprocess.run([cmd], shell=True, capture_output=True)
    #print(str(output.stdout)[9:-5].split(','))

    print(output.stdout)
    users = str(output.stdout)[7:-2].split(',')

    for user in users:
        print(f"  Deleting {user}...")
        run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code user:cancel --reassign-content {user} --yes')
        # output = subprocess.run([cmd], shell=True, capture_output=True)
        # print(output.stdout)
        # print(output.stderr)
    # print(output.stderr)

def delete_homepage(sitename):
    print('Deleting default homepage')
    run_command(f'./sites/{sitename}/code/d entity:delete node 1 --root=sites/{sitename}/code --yes')



def create_users(sitename):
    print('Creating users...')

    web_users = []
    web_users.append('jesp3304')
    web_users.append('mibo7729')
    web_users.append('alco6164')
    web_users.append('joni1621')
    web_users.append('jako6198')
    web_users.append('titr7839')
    web_users.append('pabr5825')

    ux_users = []
    ux_users.append('linebarg')
    ux_users.append('niwa4700')
    ux_users.append('brokaw')
    ux_users.append('wetu1300')
    ux_users.append('crafts')

    service_manager_users = []
    service_manager_users.append('webexpress-manager')
    'site_manager'

    service_editor_users = []
    service_manager_users.append('webexpress-editor')
    'content_editor'




    for user in web_users:
        print(f"  Creating web user {user}...")
        run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code user:create {user}  --mail="{user}@colorado.edu" --password="nextest" --yes')
        run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code user:role:add developer  {user} --yes')

    for user in ux_users:
        print(f"  Creating UX user {user}...")
        run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code user:create {user} --mail="{user}@colorado.edu" --password="nextest" --yes')
        run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code user:role:add architect  {user} --yes')







def enable_migrate_express(sitename):
    print("Enable Migrate Express...")

    run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code en migrate_express migrate_devel --yes')




if args.delete_users:
    delete_users(args.site)

if args.extract_sql_from_remote:
    extract_sql_from_remote(args.site)

if args.extract_files_from_remote:
    extract_files_from_remote(args.site)


if args.enable_firstchild:
    sitename_clean = (args.site).replace('-', '')
    engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/{sitename_clean}?charset=utf8mb4", echo=False)

    enable_firstchild(args.site)


if args.create_local_training_site:
    create_local_db(args.site)
    clone_template(args.site)
    composer_update(args.site)
    create_drush_symlink(args.site)
    create_migrate_express_symlink(args.site)
    create_training_dataxml_symlink(args.site)
    install_drupal(args.site)

    install_training_destination_drupal(args.site)
    fetch_training_destination_database(args.site)
    import_training_destination_database(args.site)

    update_training_settings_file(args.site)
    delete_users(args.site)
    enable_migrate_express(args.site)
    set_files_permissions(args.site)

if args.extract_psa_from_remote:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
    create_local_db(args.site)
    create_local_db(args.site + '-src')
    load_sql_to_local_db(args.site)

    sitename_clean = (args.site+'-src').replace('-', '')
    engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/{sitename_clean}?charset=utf8mb4", echo=False)

    # clone_template(args.site)
    composer_update(args.site)
    create_drush_symlink(args.site)
    create_migrate_express_symlink(args.site)
    create_dataxml_symlink(args.site)
    install_drupal(args.site)

    update_settings_file(args.site)
    generate_dataxml(args.site)
    delete_users(args.site)
    #create_users(args.site)
    delete_homepage(args.site)
    enable_migrate_express(args.site)
    set_files_permissions(args.site)
    set_configuration(args.site)


if args.extract_psa_from_remote_localdev:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
    create_local_db(args.site)
    create_local_db(args.site + '-src')
    load_sql_to_local_db(args.site)

    sitename_clean = (args.site+'-src').replace('-', '')
    engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/{sitename_clean}?charset=utf8mb4", echo=False)

    clone_template(args.site)
    composer_update(args.site)
    create_drush_symlink(args.site)
    create_migrate_express_symlink(args.site)
    create_dataxml_symlink(args.site)
    install_drupal(args.site)

    # install_destination_drupal(args.site)
    # fetch_destination_database(args.site)
    # import_destination_database(args.site)

    update_settings_file(args.site)
    generate_dataxml(args.site)
    delete_users(args.site)
    #create_users(args.site)
    delete_homepage(args.site)
    enable_migrate_express(args.site)
    set_files_permissions(args.site)
    set_configuration(args.site)

if args.shortcode_fix:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
    create_local_db(args.site)
    clone_template(args.site)
    composer_update(args.site)
    create_drush_symlink(args.site)
    create_migrate_express_symlink(args.site)
    install_drupal(args.site)
    load_sql_to_local_db_dst(args.site)





'ln -s ../../data.xml data.xml'
'ln -s ./vendor/bin/drush sites/ucb-biden/d'
'mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS ucbbiden;"'
'mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS ucbbidensrc;"'
'ln -s sites/ucb-biden/code/web/ web'
'composer update --working-dir=sites/ucb-biden/code'
'ln -s ~/Projects/migrate_express sites/ucb-biden/code/web/modules/custom/migrate_express'
'git clone https://github.com/CuBoulder/tiamat10-project-template.git sites/ucb-biden/code'
'mariadb -u root -ppass ucbbidensrc < sites/ucb-biden/database.sql'
'./sites/ucb-biden/code/d --root=sites/ucb-biden/code si boulder_profile  --db-url="mysql://root:pass@localhost:3306/ucbbiden" --account-name="admin" --account-pass="tiamat.test"  --site-name="Web Express V2 Test Site" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --yes'
'./sites/ucb-biden/code/d --root=sites/ucb-biden/code en migrate_express --yes'

'python express-extract.py --site=ucb-biden-src > sites/ucb-biden/data.xml'

'./sites/ucb-biden/code/d --root=sites/ucb-biden/code config:set system.site page.front /home --yes'

'./sites/ucb-biden/code/d --root=sites/ucb-biden/code cr --yes'
'chmod -R 777 sites/ucb-biden/code/web/sites/default/files'