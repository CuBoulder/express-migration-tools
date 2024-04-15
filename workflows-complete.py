#!/usr/bin/env python

run_command(f'terminus workflow:list {sitename}.dev --format=json')
# output = subprocess.run([cmd], shell=True, capture_output=True)
# print(output.stdout)
# print(output.stderr)