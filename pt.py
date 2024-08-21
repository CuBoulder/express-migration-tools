#!/usr/bin/env python

import yaml
import rich
import typer
import concurrent.futures
import subprocess
# from rich import print

app = typer.Typer()

def run_command(cmd):
    print('Commands: ' + cmd)
    output = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    print(output.stdout)

    if len(output.stderr) > 0:
        print(output.stderr)

    return output

def fetch_connection_information(site):

    cmd_connection_info = f'terminus connection:info {site["dst"]}.live --format=yaml'
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)
    return connection_info


def fetch_training_connection_information(site):

    cmd_connection_info = f'terminus connection:info {site["training"]}.live --format=yaml'
    print(cmd_connection_info)
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)
    return connection_info

def fetch_git_info(site):

    cmd_connection_info = f'terminus connection:info {site["dst"]}.dev --format=yaml'
    connection_info = yaml.safe_load(run_command(cmd_connection_info).stdout)
    return connection_info['git_command']

def block_on_workflows(site):
    pass

def wake_site(site):

    cmd_wake_site = f'terminus env:wake {site["dst"]}.live'
    print(cmd_wake_site)

    run_command(cmd_wake_site)

def wake_src_site(site):

    cmd_wake_site = f'terminus env:wake {site["src"]}.live'
    print(cmd_wake_site)

    run_command(cmd_wake_site)

def wake_training_site(site):

    cmd_wake_site = f'terminus env:wake {site["training"]}.live'
    print(cmd_wake_site)

    run_command(cmd_wake_site)

def remote_backup(site):
    cmd_remote_backup = f'terminus backup:create {site["dst"]}.live'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)

def remote_training_backup(site):
    cmd_remote_backup = f'terminus backup:create {site["training"]}.live'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)

def remote_source_backup(site):
    cmd_remote_backup = f'terminus backup:create {site["src"]}.live'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)

def remote_source_disable_saml(site):
    cmd_remote_backup = f'terminus remote:drush {site["src"]}.live -- pm-disable simplesamlphp_auth --yes'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)


def remote_source_enable_saml(site):
    cmd_remote_backup = f'terminus remote:drush {site["src"]}.live -- en cu_saml --yes'

    print(cmd_remote_backup)
    run_command(cmd_remote_backup)


def clear_upstream_cache(site):
    cmd_clear_upstream_cache = f'terminus site:upstream:clear-cache {site["dst"]}'

    print(cmd_clear_upstream_cache)
    run_command(cmd_clear_upstream_cache)

def clear_training_upstream_cache(site):
    cmd_clear_upstream_cache = f'terminus site:upstream:clear-cache {site["training"]}'

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

def generate_prelaunch_report(site):
    cmd_prelaunch_generate_report = f'python report.py generate-report {site["src"]} > sites/{site["src"]}/migration-report.html'
    print(cmd_prelaunch_generate_report)
    run_command(cmd_prelaunch_generate_report)

def store_report(site):

    wake_site(site)

    connection_info = fetch_connection_information(site)

    cmd_upload_report = f"{connection_info['sftp_command']} <<< 'put sites/{site['src']}/migration-report.html /files/migration-report.html'"
    print(cmd_upload_report)
    run_command(cmd_upload_report)

    cmd_store_report = f'terminus remote:drush {site["dst"]}.live -- ucb_drush_commands:store-report'
    print(cmd_store_report)
    run_command(cmd_store_report)

def run_c404(site):
    cmd_run_c404 = f'terminus remote:drush {site["dst"]}.live -- c404'
    print(cmd_run_c404)
    run_command(cmd_run_c404)


def configure_smtp(site):
    password = ""
    cmd_smtp_password_set = f'terminus remote:drush {site["dst"]}.live -- config:set smtp.settings smtp_password "{password}" --yes'
    print(cmd_smtp_password_set)
    run_command(cmd_smtp_password_set)

def configure_beacon(site):
    cmd_beacon_set = f'terminus remote:drush {site["dst"]}.live -- config:set ucb_admin_menus.configuration admin_helpscout_beacon_id 7aeb6f1c-247c-4a83-b44f-4cee2784bb63 -y'
    print(cmd_beacon_set)
    run_command(cmd_beacon_set)

def configure_training_beacon(site):
    cmd_beacon_set = f'terminus remote:drush {site["training"]}.live -- config:set ucb_admin_menus.configuration admin_helpscout_beacon_id 7aeb6f1c-247c-4a83-b44f-4cee2784bb63 -y'
    print(cmd_beacon_set)
    run_command(cmd_beacon_set)

def execute_cron(site):
    cmd_execute_cron = f'terminus remote:drush {site["dst"]}.live -- cron'
    print(cmd_execute_cron)
    run_command(cmd_execute_cron)

def set_sitemap_baseurl(site):
    cmd_sitemap_baseurl_set = f'terminus remote:drush {site["dst"]}.live -- config:set simple_sitemap.settings base_url https://www.colorado.edu/{site["path"]} -y'
    print(cmd_sitemap_baseurl_set)
    run_command(cmd_sitemap_baseurl_set)

def deploy_update(site):

    clear_upstream_cache(site)

    cmd_update_apply = f'terminus  upstream:updates:apply {site["dst"]}.dev --accept-upstream'
    print(cmd_update_apply)
    run_command(cmd_update_apply)

    cmd_update_deploy_test = f'terminus  env:deploy {site["dst"]}.test'
    print(cmd_update_deploy_test)
    run_command(cmd_update_deploy_test)

    cmd_update_deploy_live = f'terminus  env:deploy {site["dst"]}.live'
    print(cmd_update_deploy_live)
    run_command(cmd_update_deploy_live)

    cmd_enable_modules = f'terminus remote:drush {site["dst"]}.live -- en media_alias_display media_entity_file_replace media_file_delete menu_block ckeditor5_paste_filter scheduler layout_builder_iframe_modal linkit administerusersbyrole google_tag menu_firstchild responsive_preview anchor_link smtp recaptcha_v3 rebuild_cache_access ucb_migration_shortcodes ckeditor5_bootstrap_accordion ucb_drush_commands --yes'
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


def deploy_training_update(site):

    clear_training_upstream_cache(site)

    cmd_update_apply = f'terminus  upstream:updates:apply {site["training"]}.dev --accept-upstream'
    print(cmd_update_apply)
    run_command(cmd_update_apply)

    cmd_update_deploy_test = f'terminus  env:deploy {site["training"]}.test'
    print(cmd_update_deploy_test)
    run_command(cmd_update_deploy_test)

    cmd_update_deploy_live = f'terminus  env:deploy {site["training"]}.live'
    print(cmd_update_deploy_live)
    run_command(cmd_update_deploy_live)

    cmd_enable_modules = f'terminus remote:drush {site["training"]}.live -- en media_alias_display media_entity_file_replace media_file_delete menu_block ckeditor5_paste_filter scheduler layout_builder_iframe_modal linkit administerusersbyrole google_tag menu_firstchild responsive_preview anchor_link smtp recaptcha_v3 rebuild_cache_access ucb_migration_shortcodes ckeditor5_bootstrap_accordion ucb_drush_commands --yes'
    print(cmd_enable_modules)
    run_command(cmd_enable_modules)

    cmd_features_import = f'terminus remote:drush {site["training"]}.live -- features:import cu_boulder_content_types --yes'
    print(cmd_features_import)
    run_command(cmd_features_import)

    cmd_config_import = f'terminus remote:drush {site["training"]}.live -- config:import --partial --source=/code/web/profiles/custom/boulder_profile/config/install --yes'
    print(cmd_config_import)
    run_command(cmd_config_import)

    cmd_updatedb = f'terminus remote:drush {site["training"]}.live -- updb --yes'
    print(cmd_updatedb)
    run_command(cmd_updatedb)

    cache_training_rebuild(site)




def cache_rebuild(site):

    cmd_cache_rebuild = f'terminus remote:drush {site["dst"]}.live -- cr'
    print(cmd_cache_rebuild)

    run_command(cmd_cache_rebuild)

def cache_training_rebuild(site):

    cmd_cache_rebuild = f'terminus remote:drush {site["training"]}.live -- cr'
    print(cmd_cache_rebuild)

    run_command(cmd_cache_rebuild)

def set_plan_basic(site):
    cmd_set_plan_basic = f'terminus plan:set {site["dst"]} plan-basic_small-contract-annual-1'
    print(cmd_set_plan_basic)

    run_command(cmd_set_plan_basic)

def unlock_pantheon_site(site):
    cmd_unlock_pantheon_site = f'terminus lock:disable {site["src"]}.live'
    print(cmd_unlock_pantheon_site)

    run_command(cmd_unlock_pantheon_site)

def set_domain(site):
    cmd_set_domain = f'terminus domain:add {site["dst"]}.live {site["dst"]}.agcdn.colorado.edu'
    print(cmd_set_domain)

    run_command(cmd_set_domain)

def set_domain_masking_config(site):
    cmd_set_domain_masking_domain = f'terminus remote:drush {site["dst"]}.live -- config:set pantheon_domain_masking.settings domain www.colorado.edu --yes'
    print(cmd_set_domain_masking_domain)
    run_command(cmd_set_domain_masking_domain)

    cmd_set_domain_masking_subpath = f'terminus remote:drush {site["dst"]}.live -- config:set pantheon_domain_masking.settings subpath {site["path"]} --yes'
    print(cmd_set_domain_masking_subpath)
    run_command(cmd_set_domain_masking_subpath)

def set_domain_masking_enable(site):
    cmd_set_domain_masking_enable = f'terminus remote:drush {site["dst"]}.live -- config:set pantheon_domain_masking.settings enabled yes --yes'
    print(cmd_set_domain_masking_enable)
    run_command(cmd_set_domain_masking_enable)


def add_tag(site):

    cmd_add_tag = f'terminus tag:add {site["dst"]} "University of Colorado Boulder" -- "upstream-tiamat"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

    cmd_add_tag = f'terminus tag:add {site["dst"]} "University of Colorado Boulder" -- "migration-in-progress"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

    cmd_add_tag = f'terminus tag:add {site["dst"]} "University of Colorado Boulder" -- "ucb-colorado"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

    cmd_add_tag = f'terminus tag:add {site["dst"]} "University of Colorado Boulder" -- "cohort-control"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

def add_training_tag(site):

    cmd_add_tag = f'terminus tag:add {site["training"]} "University of Colorado Boulder" -- "upstream-tiamat"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

    cmd_add_tag = f'terminus tag:add {site["training"]} "University of Colorado Boulder" -- "migration-training"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

    cmd_add_tag = f'terminus tag:add {site["training"]} "University of Colorado Boulder" -- "cohort-control"'
    print(cmd_add_tag)
    run_command(cmd_add_tag)

def print_site(site):
    print(f"https://www.colorado.edu/{site['path']}, https://live-{site['dst']}.pantheonsite.io")

def user_config(site):

    wake_site(site)

    web_users = []
    web_users.append('jesp3304')
    web_users.append('mibo7729')
    web_users.append('alco6164')
    web_users.append('joni1621')
    web_users.append('jako6198')
    web_users.append('titr7839')
    web_users.append('pabr5825')

    ux_users = []
    ux_users.append('linebarg')
    ux_users.append('brokaw')
    ux_users.append('wetu1300')
    ux_users.append('crafts')

    service_manager_users = []
    service_manager_users.append('webexpress-manager')
    'site_manager'

    service_editor_users = []
    service_editor_users.append('webexpress-editor')
    'content_editor'

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



def user_training_config(site):

    wake_site(site)

    web_users = []
    web_users.append('jesp3304')
    web_users.append('mibo7729')
    web_users.append('alco6164')
    web_users.append('joni1621')
    web_users.append('jako6198')
    web_users.append('titr7839')
    web_users.append('pabr5825')

    ux_users = []
    ux_users.append('linebarg')
    ux_users.append('brokaw')
    ux_users.append('wetu1300')
    ux_users.append('crafts')

    service_manager_users = []
    service_manager_users.append('webexpress-manager')
    'site_manager'

    service_editor_users = []
    service_editor_users.append('webexpress-editor')
    'content_editor'

    for user in web_users:
        cmd_add_user = f'terminus remote:drush {site["training"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["training"]}.live -- user:role:add developer  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in ux_users:
        cmd_add_user = f'terminus remote:drush {site["training"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["training"]}.live -- user:role:add architect  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in service_manager_users:
        cmd_add_user = f'terminus remote:drush {site["training"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["training"]}.live -- user:role:add site_manager  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)

    for user in service_editor_users:
        cmd_add_user = f'terminus remote:drush {site["training"]}.live -- user:create {user}  --mail="{user}@colorado.edu" --yes'
        print(cmd_add_user)
        run_command(cmd_add_user)

        cmd_add_role = f'terminus remote:drush {site["training"]}.live -- user:role:add content_editor  {user} --yes'
        print(cmd_add_role)
        run_command(cmd_add_role)




def saml_config(site):
    git_cmd = fetch_git_info(site)

    cmd_fetch_repo = f'cd ./siterepos && {git_cmd}'
    print(cmd_fetch_repo)
    run_command(cmd_fetch_repo)

    cmd_update_saml_config = f'cd ./siterepos/{site["dst"]} && cp -r ~/Projects/private-config/* . && git add -A && git commit -m "Add config" && git push'
    print(cmd_update_saml_config)
    run_command(cmd_update_saml_config)




def upload_local_files(site):
    wake_site(site)

    connection_info = fetch_connection_information(site)

    sftp_parts = connection_info['sftp_command'].split(" ")[3].split('@')

    rclone_remote_create_command = f'rclone config create {site["dst"]} sftp host={sftp_parts[1]} user={sftp_parts[0]} port=2222 use_ssh_agent=false key_file=/home/$USER/.ssh/id_rsa md5sum_command=none sha1sum_command=none'
    print(rclone_remote_create_command)
    run_command(rclone_remote_create_command)

    rclone_sync_command = f'cd ./sites/{site["src"]}/code/web/sites/default/files &&  rclone sync . {site["dst"]}:files --size-only -v'
    print(rclone_sync_command)
    run_command(rclone_sync_command)


def upload_training_local_files(site):
    wake_training_site(site)

    connection_info = fetch_training_connection_information(site)
    if connection_info is None:
        return

    sftp_parts = connection_info['sftp_command'].split(" ")[3].split('@')

    rclone_remote_create_command = f'rclone config create {site["training"]} sftp host={sftp_parts[1]} user={sftp_parts[0]} port=2222 use_ssh_agent=false key_file=/home/$USER/.ssh/id_rsa md5sum_command=none sha1sum_command=none'
    print(rclone_remote_create_command)
    run_command(rclone_remote_create_command)

    rclone_sync_command = f'cd ./sites/{site["training"]}/code/web/sites/default/files &&  rclone sync . {site["training"]}:files --size-only -v'
    print(rclone_sync_command)
    run_command(rclone_sync_command)

def upload_local_database(site):
    # print(site['dst'])

    wake_site(site)

    connection_info = fetch_connection_information(site)

    cmd_upload_local_database = f'cd ./sites/{site["src"]}/code && {connection_info["mysql_command"]} < database.sql'

    print(cmd_upload_local_database)
    run_command(cmd_upload_local_database)

def upload_training_local_database(site):
    # print(site['dst'])

    wake_training_site(site)

    connection_info = fetch_training_connection_information(site)
    if connection_info is None:
        return

    cmd_upload_local_database = f'cd ./sites/{site["training"]}/code && {connection_info["mysql_command"]} < database.sql'

    print(cmd_upload_local_database)
    run_command(cmd_upload_local_database)


def remove_local_databases(site):
    dst_sitename_clean = site['src'].replace('-', '')
    src_sitename_clean = dst_sitename_clean + 'src'

    cmd_remove_src_database = f'mariadb -u root -ppass --execute="drop database {src_sitename_clean};"'
    print(cmd_remove_src_database)
    run_command(cmd_remove_src_database)

    cmd_remove_dst_database = f'mariadb -u root -ppass --execute="drop database {dst_sitename_clean};"'
    print(cmd_remove_dst_database)
    run_command(cmd_remove_dst_database)


def remove_training_local_databases(site):
    training_sitename_clean = site['training'].replace('-', '')


    cmd_remove_training_database = f'mariadb -u root -ppass --execute="drop database {training_sitename_clean};"'
    print(cmd_remove_training_database)
    run_command(cmd_remove_training_database)



def export_local_database(site):
    # print(site['dst'])

    sitename_clean = site['src'].replace('-', '')

    cmd_export_local_database = f'cd ./sites/{site["src"]}/code && mysqldump -u root -ppass {sitename_clean} > database.sql'

    print(cmd_export_local_database)
    run_command(cmd_export_local_database)

def export_training_local_database(site):
    # print(site['dst'])

    sitename_clean = site['training'].replace('-', '')

    cmd_export_local_database = f'cd ./sites/{site["training"]}/code && mysqldump -u root -ppass {sitename_clean} > database.sql'

    print(cmd_export_local_database)
    run_command(cmd_export_local_database)


def configure_modules(site):
    # print(site['dst'])

    cmd_configure_modules = f'cd ./sites/{site["src"]}/code && ./d pmu migrate_devel migrate_express --yes'

    print(cmd_configure_modules)
    run_command(cmd_configure_modules)

def configure_training_modules(site):
    # print(site['dst'])

    cmd_configure_training_modules = f'cd ./sites/{site["training"]}/code && ./d pmu migrate_devel migrate_express --yes'

    print(cmd_configure_training_modules)
    run_command(cmd_configure_training_modules)

def convert_shortcodes(site):
    # print(site['dst'])

    cmd_enable_modules = f'cd ./sites/{site["src"]}/code && ./d en ucb_migration_shortcodes migrate_express --yes'
    print(cmd_enable_modules)
    run_command(cmd_enable_modules)

    cmd_configure_shortcodes = f'cd ./sites/{site["src"]}/code && ./d migrate_express:shortcode-convert blah'
    print(cmd_configure_shortcodes)
    run_command(cmd_configure_shortcodes)

    cmd_disable_modules = f'cd ./sites/{site["src"]}/code && ./d pmu ucb_migration_shortcodes shortcode --yes'
    print(cmd_disable_modules)
    run_command(cmd_disable_modules)

def correct_firstchild(site):
    print(site['dst'])

    cmd_enable_modules = f'./migrate.py --enable-firstchild --site={site["src"]}'
    print(cmd_enable_modules)
    run_command(cmd_enable_modules)


def migrate_import(site):
    # print(site['dst'])


    cmd_configure_modules = f'cd ./sites/{site["src"]}/code && ./d en migrate_express --yes'

    print(cmd_configure_modules)
    run_command(cmd_configure_modules)


    try_limit = 5
    tries = 0

    cmd_migrate_import = f'cd ./sites/{site["src"]}/code && ./d migrate:import --tag=express --execute-dependencies 2>&1 | tee -a migrateoutput.txt'

    print(cmd_migrate_import)

    while tries < try_limit:
        tries += 1
        print(f"Try: {tries}")
        output = run_command(cmd_migrate_import)
        if output.returncode == 0:
            break

def migrate_users_import(site):
    # print(site['dst'])

    try_limit = 5
    tries = 0

    cmd_migrate_import = f'cd ./sites/{site["src"]}/code && ./d migrate:import express_users --execute-dependencies 2>&1 | tee -a migrateoutput.txt'

    print(cmd_migrate_import)

    while tries < try_limit:
        tries += 1
        print(f"Try: {tries}")
        output = run_command(cmd_migrate_import)
        if output.returncode == 0:
            break

def migrate_training_import(site):
    # print(site['dst'])

    try_limit = 5
    tries = 0

    cmd_migrate_training_import = f'cd ./sites/{site["training"]}/code && ./d migrate:import express_users --execute-dependencies 2>&1 | tee -a migrateoutput.txt'

    print(cmd_migrate_training_import)

    while tries < try_limit:
        tries += 1
        print(f"Try: {tries}")
        output = run_command(cmd_migrate_training_import)
        if output.returncode == 0:
            break


def create_site(site):
    # print(site['dst'])

    cmd_create_site = f'terminus site:create {site["dst"][0:51]} {site["dst"][0:51]} --org="University of Colorado Boulder" tiamat_production'

    print(cmd_create_site)
    run_command(cmd_create_site)

def deploy_site(site):
    # print(site['dst'])


    cmd_deploy_site = f'terminus env:deploy {site["dst"]}.test --yes && terminus env:deploy {site["dst"]}.live --yes'

    # print(cmd_deploy_site)
    run_command(cmd_deploy_site)
    
def download_site(site):


    wake_src_site(site)


    cmd_download_site = f'./migrate.py --extract-psa-from-remote --site={site["src"]}'

    print(cmd_download_site)

    try:
        run_command(cmd_download_site)
    except:
        print("Problem: " + str(cmd_download_site))

def create_training_site(site):
    cmd_create_training_site = f'./migrate.py --create-local-training-site --site={site["training"]}'
    print(cmd_create_training_site)

    try:
        run_command(cmd_create_training_site)
    except:
        print("Problem: " + str(cmd_create_training_site))


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
def saml_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(saml_config, sitelist['sites']):
                pass


@app.command()
def download_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for _ in executor.map(download_site, sitelist['sites']):
                pass

@app.command()
def create_training_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(create_training_site, sitelist['sites']):
                pass

@app.command()
def migrate_import_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(migrate_import, sitelist['sites']):
                pass

@app.command()
def migrate_users_import_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(migrate_users_import, sitelist['sites']):
                pass

@app.command()
def migrate_training_import_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(migrate_training_import, sitelist['sites']):
                pass


@app.command()
def configure_modules_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(configure_modules, sitelist['sites']):
                pass

@app.command()
def configure_training_modules_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(configure_training_modules, sitelist['sites']):
                pass

@app.command()
def convert_shortcodes_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for _ in executor.map(convert_shortcodes, sitelist['sites']):
                pass

@app.command()
def correct_firstchild_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for _ in executor.map(correct_firstchild, sitelist['sites']):
                pass

@app.command()
def export_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(export_local_database, sitelist['sites']):
                pass

@app.command()
def export_training_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(export_training_local_database, sitelist['sites']):
                pass


@app.command()
def upload_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(upload_local_database, sitelist['sites']):
                pass

@app.command()
def upload_training_local_database_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(upload_training_local_database, sitelist['sites']):
                pass

@app.command()
def upload_local_files_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(upload_local_files, sitelist['sites']):
                pass

@app.command()
def upload_training_local_files_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(upload_training_local_files, sitelist['sites']):
                pass

@app.command()
def cache_rebuild_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(cache_rebuild, sitelist['sites']):
                pass

@app.command()
def execute_cron_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(execute_cron, sitelist['sites']):
                pass

@app.command()
def set_sitemap_baseurl_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(set_sitemap_baseurl, sitelist['sites']):
                pass

@app.command()
def remove_local_databases_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(remove_local_databases, sitelist['sites']):
                pass

@app.command()
def remove_training_local_databases_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(remove_training_local_databases, sitelist['sites']):
                pass

@app.command()
def user_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(user_config, sitelist['sites']):
                pass

@app.command()
def user_training_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(user_training_config, sitelist['sites']):
                pass

@app.command()
def remote_backup_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_backup, sitelist['sites']):
                pass

@app.command()
def remote_source_backup_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_source_backup, sitelist['sites']):
                pass

@app.command()
def remote_source_disable_saml_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_source_disable_saml, sitelist['sites']):
                pass

@app.command()
def remote_source_enable_saml_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_source_enable_saml, sitelist['sites']):
                pass

@app.command()
def remote_training_backup_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(remote_training_backup, sitelist['sites']):
                pass

@app.command()
def deploy_update_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(deploy_update, sitelist['sites']):
                pass

@app.command()
def configure_smtp_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(configure_smtp, sitelist['sites']):
                pass

@app.command()
def configure_beacon_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(configure_beacon, sitelist['sites']):
                pass

@app.command()
def configure_training_beacon_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(configure_training_beacon, sitelist['sites']):
                pass

@app.command()
def deploy_training_update_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(deploy_training_update, sitelist['sites']):
                pass


@app.command()
def deploy_environment_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            for _ in executor.map(deploy_environment, sitelist['sites']):
                pass

@app.command()
def add_tag_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(add_tag, sitelist['sites']):
                pass

@app.command()
def add_training_tag_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(add_training_tag, sitelist['sites']):
                pass

@app.command()
def set_plan_basic_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(set_plan_basic, sitelist['sites']):
                pass

@app.command()
def set_domain_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(set_domain, sitelist['sites']):
                pass

@app.command()
def set_domain_masking_config_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(set_domain_masking_config, sitelist['sites']):
                pass

@app.command()
def set_domain_masking_enable_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(set_domain_masking_enable, sitelist['sites']):
                pass

@app.command()
def generate_prelaunch_report_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for _ in executor.map(generate_prelaunch_report, sitelist['sites']):
                pass

@app.command()
def store_report_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(store_report, sitelist['sites']):
                pass

@app.command()
def run_c404_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in executor.map(run_c404, sitelist['sites']):
                pass

@app.command()
def unlock_pantheon_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            for _ in executor.map(unlock_pantheon_site, sitelist['sites']):
                pass

@app.command()
def print_site_sitelist(name: str):
    with open(name) as input:
        sitelist = yaml.safe_load(input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for _ in executor.map(print_site, sitelist['sites']):
                pass
        

@app.command()
def prepare_site(name: str):
    print(name)

@app.command()
def apply_updates(name: str):
    print(name)

if __name__ == "__main__":
    app()
    