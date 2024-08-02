#!/usr/bin/env python3

import subprocess
import json
import tempfile
import argparse
import os
import tarfile
import posixpath
import stat
import yaml
from pathlib import Path
import time
from stat import S_ISDIR, S_ISREG
import random
import concurrent.futures
import tarfile
import shutil
import pprint
import jinja2
import threading
import re
import sys

from typing import List


def multiaction(site):
    name = site

    backupcmd = f'terminus backup:create {name}.live'
    updatecmd = f'bash sbupdate.bash {name}'

    # print(backupcmd)

    output = subprocess.run([backupcmd], shell=True, capture_output=True)
    if(len(str(output.stdout)) > 0):
        print(f"Site - {name} - stdout:" + str(output.stdout))
    if (len(str(output.stderr)) > 0):
        print(f"Site - {name} - stderr:" + str(output.stderr))





sites = []

with open('sandboxlist') as input:
    for line in input:
        sites.append(line.strip())

# output = subprocess.run([f'terminus org:site:list "University of Colorado Boulder" --tag=ucb-colorado --tag=upstream-express --format=json'], shell=True, capture_output=True)
# psites = json.loads(output.stdout)
# for x in psites:
#     #print(psites[x]['name'])
#     sites.append(psites[x]['name'])

# print(sites)



with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    for _ in executor.map(multiaction, sites):
        pass





