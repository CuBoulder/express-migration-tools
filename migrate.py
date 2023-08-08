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

args = parser.parse_args()


def create_local_db(sitename):
    sitename_clean = sitename.replace('-','')
    cmd = f'mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS {sitename_clean};"'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)

def extract_sql_from_remote(sitename):
    print(sitename)
    os.makedirs(f'sites/{sitename}', exist_ok=True)
    cmd = f'terminus remote:drush {sitename}.live -- sql-dump --skip-tables-list=cache,cache_* > sites/{sitename}/database.sql'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)

def install_drupal(sitename):
    pass

def delete_users(sitename):
    pass

def create_drush_symlink(sitename):
    pass

def create_migrate_express_symlink(sitename):
    pass


def load_sql_to_local_db(sitename):
    pass

def clone_template(sitename):
    cmd = f'git clone https://github.com/CuBoulder/tiamat10-project-template.git sites/{sitename}/code'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)

def set_files_permissions(sitename):
    pass

def extract_files_from_remote(sitename):
    os.makedirs(f'sites/{sitename}/files', exist_ok=True)

    cmd = f'terminus local:getLiveFiles {sitename}.live --overwrite'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)

    cmd = f'tar -xzvf /home/tirazel/pantheon-local-copies/files/{sitename}-files.tgz -C sites/{sitename}'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)

    os.rename(f'sites/{sitename}/files_live', f'sites/{sitename}/files')




if args.extract_sql_from_remote:
    extract_sql_from_remote(args.site)

if args.extract_files_from_remote:
    extract_files_from_remote(args.site)

if args.extract_psa_from_remote:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
    create_local_db(args.site)
    create_local_db(args.site + '-src')
    clone_template(args.site)


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