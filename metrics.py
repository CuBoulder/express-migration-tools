from io import StringIO, BytesIO
import argparse
import re
from itertools import chain
from glob import iglob
import os
import subprocess


def run_command(cmd, stdin=None, stdout=None):
    print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, text=True, stdin=stdin, stdout=stdout)
    #print(output.stdout)

    # if len(output.stderr) > 0:
    #     print(output.stderr)

    return output

for subdir, dirs, files in os.walk('.'):
    for file in files:
        if file[0:4] == 'ucb-':
            print(file)

            dbname = 'metrics' + file[0:-4].replace('-', '')
            xmlname = 'metrics-' + file[0:-4] + '.xml'


            print(f'Creating local DB "{dbname}"...')
            run_command(f'mariadb -u root -ppass -e "CREATE DATABASE IF NOT EXISTS {dbname};"')

            print(f'Loading local DB "{dbname}"...')
            with open(f'{file}', 'rb') as infile:
                run_command(f'mariadb -u root -ppass {dbname}', stdin=infile)

            print(f'Generating xml...')
            with open(f'xml/{xmlname}', 'wb') as outfile:
                run_command(f'python ../express-extract.py --site={dbname}', stdout=outfile)


            print(f'Deleting local DB "{dbname}"...')
            run_command(f'mariadb -u root -ppass -e "DROP DATABASE {dbname};"')


