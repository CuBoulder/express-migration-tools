#!/usr/bin/env python

import yaml
import rich
import typer
import concurrent.futures
import subprocess
from rich import print

app = typer.Typer()

def run_command(cmd):
    print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    print(output.stdout)

    if len(output.stderr) > 0:
        print(output.stderr)

    return output

def create_site(site):
    # print(site['dst'])

    cmd_create_site = f'terminus site:create {site["dst"]} {site["dst"]} --org="University of Colorado Boulder" tiamat_production'

    # print(cmd_create_site)
    run_command(cmd_create_site)

def deploy_site(site):
    # print(site['dst'])


    cmd_deploy_site = f'terminus env:deploy {site["dst"]}.test --yes; and terminus env:deploy {site["dst"]}.live --yes'

    # print(cmd_deploy_site)
    run_command(cmd_deploy_site)
    



@app.command()
def prepare_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for _ in executor.map(create_site, sitelist['sites']):
                pass


@app.command()
def deploy_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for _ in executor.map(deploy_site, sitelist['sites']):
                pass
        

@app.command()
def prepare_site(name: str):
    print(name)

@app.command()
def apply_updates(name: str):
    print(name)

if __name__ == "__main__":
    app()
    