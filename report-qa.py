from jinja2 import Environment, PackageLoader, select_autoescape
import rich
import yaml
from lxml import etree
from rich import print
import typer
import sqlalchemy
import subprocess
from bs4 import BeautifulSoup

app = typer.Typer()

parent_map = ''
root = ''

def run_command(cmd):
    # print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    # print(output.stdout)

    # if len(output.stderr) > 0:
    #     print(output.stderr)

    return output

@app.command()
def generate_linkchecker_info(name: str):

    address = ''
    if name[0:4] == 'ucb-':
        address = 'ucbprod-' + name[4:]

        cmd_linkchecker = f"linkchecker --no-warnings --check-extern --no-robots --no-follow-url='!live-{address}' -o HTML https://live-{address}.pantheonsite.io"
        # cmd_linkchecker = f'linkchecker --no-warnings --check-extern http://192.168.1.30'

        print(cmd_linkchecker)
        output = run_command(cmd_linkchecker)

        soup = BeautifulSoup(output.stdout, features="html.parser")
        body = soup.body

        # print(body.encode_contents().decode("utf-8"))

        siteinfo = {}
        siteinfo['text'] = body.encode_contents().decode("utf-8")

        return siteinfo


@app.command()
def generate_report(name: str):
    linkchecker_info = generate_linkchecker_info(name)

    env = Environment(
        loader=PackageLoader("report"),
        autoescape=select_autoescape()
    )
    template = env.get_template("report-qa.html")
    print(template.render(srcinfo=source_info, dstinfo=destination_info, linkinfo=linkchecker_info))

@app.command()
def generate_objects(name: str):
    linkchecker_info = generate_linkchecker_info(name)

    print("linkinfo:")
    print(linkchecker_info)





if __name__ == "__main__":
    app()