#!/usr/bin/env python

import yaml

# import rich
import typer
import concurrent.futures
import subprocess
from rich import print

app = typer.Typer()


def run_command(cmd):
    print("Commands: " + cmd)
    output = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    print(output.stdout)

    if len(output.stderr) > 0:
        print(output.stderr)

    return output


def fetch_connection_information(site):

    cmd_connection_info = f'terminus connection:info {site["dst"]}.live --format=yaml'
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)
    return connection_info


def fetch_git_info(site):

    cmd_connection_info = f'terminus connection:info {site["dst"]}.dev --format=yaml'
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)
    return connection_info["git_command"]


def block_on_workflows(site):
    pass


def wake_site(site):

    cmd_wake_site = f'terminus env:wake {site["dst"]}.live'
    print(cmd_wake_site)

    run_command(cmd_wake_site)


def remote_backup(site):
    cmd_remote_backup = f'terminus backup:create {site["dst"]}.live'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)


def clear_upstream_cache(site):
    cmd_clear_upstream_cache = f'terminus site:upstream:clear-cache {site["dst"]}'

    print(cmd_clear_upstream_cache)
    run_command(cmd_clear_upstream_cache)


def deploy_environment(site):

    clear_upstream_cache(site)

    cmd_update_apply = f'terminus  upstream:updates:apply {site["dst"]}.dev'
    print(cmd_update_apply)
    run_command(cmd_update_apply)

    cmd_update_deploy_test = f'terminus  env:deploy {site["dst"]}.test'
    print(cmd_update_deploy_test)
    run_command(cmd_update_deploy_test)

    cmd_update_deploy_live = f'terminus  env:deploy {site["dst"]}.live'
    print(cmd_update_deploy_live)
    run_command(cmd_update_deploy_live)


def deploy_update(site):

    clear_upstream_cache(site)

    cmd_update_apply = f'terminus  upstream:updates:apply {site["dst"]}.dev'
    print(cmd_update_apply)
    run_command(cmd_update_apply)

    cmd_update_deploy_test = f'terminus  env:deploy {site["dst"]}.test'
    print(cmd_update_deploy_test)
    run_command(cmd_update_deploy_test)

    cmd_update_deploy_live = f'terminus  env:deploy {site["dst"]}.live'
    print(cmd_update_deploy_live)
    run_command(cmd_update_deploy_live)

    cmd_enable_modules = f'terminus remote:drush {site["dst"]}.live -- en media_alias_display media_entity_file_replace media_file_delete menu_block ckeditor5_paste_filter scheduler layout_builder_iframe_modal linkit administerusersbyrole google_tag menu_firstchild responsive_preview anchor_link smtp recaptcha_v3 rebuild_cache_access --yes'
    print(cmd_enable_modules)
    run_command(cmd_enable_modules)

    cmd_features_import = f'terminus remote:drush {site["dst"]}.live -- features:import cu_boulder_content_types --yes'
    print(cmd_features_import)
    run_command(cmd_features_import)

    cmd_config_import = f'terminus remote:drush {site["dst"]}.live -- config:import --partial --source=/code/web/profiles/custom/boulder_profile/config/install --yes'
    print(cmd_config_import)
    run_command(cmd_config_import)

    cmd_updatedb = f'terminus remote:drush {site["dst"]}.live -- updb --yes'
    print(cmd_updatedb)
    run_command(cmd_updatedb)

    cache_rebuild(site)


def cache_rebuild(site):

    cmd_cache_rebuild = f'terminus remote:drush {site["dst"]}.live -- cr'
    print(cmd_cache_rebuild)

    run_command(cmd_cache_rebuild)


def add_tag(site):

    cmd_add_tag = f'terminus tag:add {site["dst"]} "University of Colorado Boulder" -- "upstream-tiamat"'
    print(cmd_add_tag)

    run_command(cmd_add_tag)


def print_site(site):
    print(
        f"https://www.colorado.edu/{site['path']}, https://live-{site['dst']}.pantheonsite.io"
    )


def user_config(site):

    wake_site(site)

    web_users = []
    web_users.append("jesp3304")
    web_users.append("mibo7729")
    web_users.append("alco6164")
    web_users.append("joni1621")
    web_users.append("jako6198")
    web_users.append("titr7839")
    web_users.append("pabr5825")

    ux_users = []
    ux_users.append("linebarg")
    ux_users.append("niwa4700")
    ux_users.append("brokaw")
    ux_users.append("wetu1300")
    ux_users.append("crafts")

    service_manager_users = []
    service_manager_users.append("webexpress-manager")
    "site_manager"

    service_editor_users = []
    service_editor_users.append("webexpress-editor")
    "content_editor"

    for user in web_users:
        cmd_add_user = f'terminus remote:drush {site["dst"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["dst"]}.live -- user:role:add developer  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in ux_users:
        cmd_add_user = f'terminus remote:drush {site["dst"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["dst"]}.live -- user:role:add architect  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in service_manager_users:
        cmd_add_user = f'terminus remote:drush {site["dst"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["dst"]}.live -- user:role:add site_manager  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in service_editor_users:
        cmd_add_user = f'terminus remote:drush {site["dst"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["dst"]}.live -- user:role:add content_editor  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)


def saml_config(site):
    git_cmd = fetch_git_info(site)

    cmd_fetch_repo = f"cd ./siterepos && {git_cmd}"
    print(cmd_fetch_repo)
    run_command(cmd_fetch_repo)

    cmd_update_saml_config = f'cd ./siterepos/{site["dst"]} && cp -r ~/Projects/private-config/* . && git add -A && git commit -m "Add config" && git push'
    print(cmd_update_saml_config)
    run_command(cmd_update_saml_config)


def upload_local_files(site):
    wake_site(site)

    connection_info = fetch_connection_information(site)

    sftp_parts = connection_info["sftp_command"].split(" ")[3].split("@")

    # print(sftp_parts)

    lftp_command = f'lftp -c "open sftp://{sftp_parts[0]}:dummypass@{sftp_parts[1]}:2222; mirror --continue --reverse --delete --parallel=5 . files --verbose"'

    cmd_upload_local_files = (
        f'cd ./sites/{site["src"]}/code/web/sites/default/files && {lftp_command}'
    )

    print(cmd_upload_local_files)
    run_command(cmd_upload_local_files)


def upload_local_database(site):
    # print(site['dst'])

    wake_site(site)

    connection_info = fetch_connection_information(site)

    cmd_upload_local_database = f'cd ./sites/{site["src"]}/code && {connection_info["mysql_command"]} < database.sql'

    print(cmd_upload_local_database)
    run_command(cmd_upload_local_database)


def remove_local_databases(site):
    dst_sitename_clean = site["src"].replace("-", "")
    src_sitename_clean = dst_sitename_clean + "src"

    cmd_remove_src_database = (
        f'mariadb -u root -ppass --execute="drop database {src_sitename_clean};"'
    )
    print(cmd_remove_src_database)
    run_command(cmd_remove_src_database)

    cmd_remove_dst_database = (
        f'mariadb -u root -ppass --execute="drop database {dst_sitename_clean};"'
    )
    print(cmd_remove_dst_database)
    run_command(cmd_remove_dst_database)


def export_local_database(site):
    # print(site['dst'])

    sitename_clean = site["src"].replace("-", "")

    cmd_export_local_database = f'cd ./sites/{site["src"]}/code && mysqldump -u root -ppass {sitename_clean} > database.sql'

    print(cmd_export_local_database)
    run_command(cmd_export_local_database)


def configure_modules(site):
    # print(site['dst'])

    cmd_configure_modules = (
        f'cd ./sites/{site["src"]}/code && ./d pmu migrate_devel migrate_express'
    )

    print(cmd_configure_modules)
    run_command(cmd_configure_modules)


def migrate_import(site):
    # print(site['dst'])

    try_limit = 5
    tries = 0

    cmd_migrate_import = f'cd ./sites/{site["src"]}/code && ./d migrate:import --tag=express --execute-dependencies'

    print(cmd_migrate_import)

    while tries < try_limit:
        tries += 1
        print(f"Try: {tries}")
        output = run_command(cmd_migrate_import)
        if output.returncode == 0:
            break


def create_site(site):
    # print(site['dst'])

    cmd_create_site = f'terminus site:create {site["dst"]} {site["dst"]} --org="University of Colorado Boulder" tiamat_production'

    print(cmd_create_site)
    run_command(cmd_create_site)


def deploy_site(site):
    # print(site['dst'])

    cmd_deploy_site = f'terminus env:deploy {site["dst"]}.test --yes && terminus env:deploy {site["dst"]}.live --yes'

    # print(cmd_deploy_site)
    run_command(cmd_deploy_site)


def download_site(site):
    cmd_download_site = f'./migrate.py --extract-psa-from-remote --site={site["src"]}'

    print(cmd_download_site)

    try:
        run_command(cmd_download_site)
    except:
        print("Problem: " + str(cmd_download_site))


@app.command()
def prepare_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for _ in executor.map(create_site, sitelist["sites"]):
                pass


@app.command()
def deploy_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for _ in executor.map(deploy_site, sitelist["sites"]):
                pass


@app.command()
def saml_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for _ in executor.map(saml_config, sitelist["sites"]):
                pass


@app.command()
def download_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for _ in executor.map(download_site, sitelist["sites"]):
                pass


@app.command()
def migrate_import_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(migrate_import, sitelist["sites"]):
                pass


@app.command()
def configure_modules_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(configure_modules, sitelist["sites"]):
                pass


@app.command()
def export_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(export_local_database, sitelist["sites"]):
                pass


@app.command()
def upload_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(upload_local_database, sitelist["sites"]):
                pass


@app.command()
def upload_local_files_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(upload_local_files, sitelist["sites"]):
                pass


@app.command()
def cache_rebuild_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(cache_rebuild, sitelist["sites"]):
                pass


@app.command()
def remove_local_databases_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(remove_local_databases, sitelist["sites"]):
                pass


@app.command()
def user_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(user_config, sitelist["sites"]):
                pass


@app.command()
def remote_backup_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_backup, sitelist["sites"]):
                pass


@app.command()
def deploy_update_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for _ in executor.map(deploy_update, sitelist["sites"]):
                pass


@app.command()
def deploy_environment_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(deploy_environment, sitelist["sites"]):
                pass


@app.command()
def add_tag_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(add_tag, sitelist["sites"]):
                pass


@app.command()
def print_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for _ in executor.map(print_site, sitelist["sites"]):
                pass


@app.command()
def prepare_site(name: str):
    print(name)


@app.command()
def apply_updates(name: str):
    print(name)


if __name__ == "__main__":
    app()
