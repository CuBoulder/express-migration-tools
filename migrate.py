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


def extract_sql_from_remote(sitename):
    print(sitename)
    os.makedirs(f'sites/{sitename}', exist_ok=True)
    cmd = f'terminus remote:drush {sitename}.live -- sql-dump --skip-tables-list=cache,cache_* > sites/{sitename}/database.sql'
    output = subprocess.run([cmd], shell=True, capture_output=True)
    print(output.stdout)
    print(output.stderr)
    pass


def load_sql_to_local():
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


    pass


def load_files_to_local():
    pass



if args.extract_sql_from_remote:
    extract_sql_from_remote(args.site)

if args.extract_files_from_remote:
    extract_files_from_remote(args.site)

if args.extract_psa_from_remote:
    extract_sql_from_remote(args.site)
    extract_files_from_remote(args.site)
