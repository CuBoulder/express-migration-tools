from io import StringIO, BytesIO
import argparse
import re
from itertools import chain
from glob import iglob
import os
import subprocess
import sqlalchemy


def run_command(cmd, stdin=None, stdout=None):
    print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, text=True, stdin=stdin, stdout=stdout)
    #print(output.stdout)

    # if len(output.stderr) > 0:
    #     print(output.stderr)

    return output

context_metrics = {}

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

            # print(f'Generating xml...')
            # with open(f'xml/{xmlname}', 'wb') as outfile:
            #     run_command(f'python ../express-extract.py --site={dbname}', stdout=outfile)

            engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/{dbname}?charset=utf8mb4", echo=False)
            with engine.connect() as conn:
                context_count_result = conn.execute(sqlalchemy.text("select count(*) from context;"))
                for count in context_count_result:
                    print(f"{dbname} context rules: " + str(count[0]))

                    if count[0] in context_metrics:
                        context_metrics[count[0]] += 1
                    else:
                        context_metrics[count[0]] = 1





            print(f'Deleting local DB "{dbname}"...')
            run_command(f'mariadb -u root -ppass -e "DROP DATABASE {dbname};"')

print(context_metrics)
