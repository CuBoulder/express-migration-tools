#!/usr/bin/env python3

import argparse
import subprocess
import os
import shutil

parser = argparse.ArgumentParser(description='Express Migration Tool')

parser.add_argument('-s', '--site', help='Sitename')
parser.add_argument('--extract-sql-from-remote', action='store_true', help='Extract SQL from Pantheon')
parser.add_argument('--extract-files-from-remote', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--extract-psa-from-remote', action='store_true', help='Extract files from Pantheon')
parser.add_argument('--delete-users', action='store_true', help='Delete users')

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
    run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code si boulder_profile  --db-url="mysql://root:pass@localhost:3306/{sitename_clean}" --account-name="admin" --account-pass="tiamat.test"  --site-name="{sitename}" install_configure_form.enable_update_status_module=NULL install_configure_form.enable_update_status_emails=NULL --yes')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


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

def set_homepage(sitename):
    print(f'Set homepage to /home...')
    run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code config:set system.site page.front /home --yes')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)


def load_sql_to_local_db(sitename):
    print(f'Loading SQL to local source DB...')
    sitename_clean = sitename.replace('-', '')
    run_command(f'mariadb -u root -ppass {sitename_clean}src < sites/{sitename}/database.sql')
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
    run_command(f'composer update --working-dir=sites/{sitename}/code')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def set_files_permissions(sitename):
    print(f'Setting files directory permissions...')
    run_command(f'sudo chmod -R 777 sites/{sitename}/code/web/sites/default/files')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

def extract_files_from_remote(sitename):
    print('Extracting files...')
    os.makedirs(f'sites/{sitename}/files', exist_ok=True)

    run_command(f'terminus local:getLiveFiles {sitename}.live --overwrite')
    # output = subprocess.run([cmd], shell=True, capture_output=True)
    # print(output.stdout)
    # print(output.stderr)

    run_command(f'tar -xzvf /home/tirazel/pantheon-local-copies/files/{sitename}-files.tgz -C sites/{sitename}')
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

def enable_migrate_express(sitename):
    print("Enable Migrate Express...")

    run_command(f'./sites/{sitename}/code/d --root=sites/{sitename}/code en migrate_express --yes')




if args.delete_users:
    delete_users(args.site)

if args.extract_sql_from_remote:
    extract_sql_from_remote(args.site)

if args.extract_files_from_remote:
    extract_files_from_remote(args.site)

if args.extract_psa_from_remote:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
    create_local_db(args.site)
    create_local_db(args.site + '-src')
    load_sql_to_local_db(args.site)
    clone_template(args.site)
    composer_update(args.site)
    create_drush_symlink(args.site)
    create_migrate_express_symlink(args.site)
    create_dataxml_symlink(args.site)
    install_drupal(args.site)
    generate_dataxml(args.site)
    delete_users(args.site)
    enable_migrate_express(args.site)
    set_homepage(args.site)
    set_files_permissions(args.site)


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