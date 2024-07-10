import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv
import dicttoxml
import time
import re
import sys
import tinycss2
import pprint
import yaml
import copy
import datetime
import dateutil
from bs4 import BeautifulSoup
import cssutils



from lxml import etree
from io import StringIO, BytesIO


def translate_inline_styles(value):
    cssmap = {}
    cssmap['text-align: center'] = 'text-align-center'
    cssmap['float: left'] = 'align-left'  # Wrap in div
    cssmap['float: right'] = 'align-right'  # Wrap div

    'font-size'

    'beautifulsoup'
    'tinycss2'
    'soup.find_all(style=True)'


def extract_subfields(field):
    fd_columninfo_result = conn.execute(sqlalchemy.text(f"select column_name as 'subfield' from information_schema.COLUMNS where table_schema = DATABASE() AND table_name = 'field_data_{field}' limit 100 offset 7;"))
    subfields = []
    subfields.append('entity_id')
    subfields.append('delta')
    for item in fd_columninfo_result:
        subfields.append(item.subfield)
    return subfields


def extract_fields(type, id, revision_id):


    fields = {}
    fci_result = conn.execute(sqlalchemy.text(f"select a.id, a.field_id, a.field_name, a.entity_type, a.bundle, b.type from field_config_instance a, field_config b where bundle = '{type}' AND a.field_name = b.field_name;"))
    for fci_item in fci_result:
        field = {}
        # field['bundle'] = fci_item.bundle
        # field['entity_type'] = fci_item.entity_type
        field['field_name'] = fci_item.field_name
        field['type'] = fci_item.type


        columns = extract_subfields(fci_item.field_name)

        data = []

        fd_result = conn.execute(sqlalchemy.text(f"select {', '.join(columns)} from field_data_{fci_item.field_name} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))

        for fd_item in fd_result.mappings():
            field_item = {}
            for colname in columns:
                field_item[colname] = fd_item[colname]

            if 'entity_id' in field_item and 'delta' in field_item:
                field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"
            data.append(field_item)

        field['data'] = data
        fields[field['field_name']] = field

    return fields


node_typemap = {}

# Module: cu_publication

#  Node: issue

node_issue_fields = []
node_issue_fields.append({'name': 'body', 'type': 'node', 'bundle': 'issue'})
node_issue_fields.append({'name': 'field_issue_image', 'type': 'node', 'bundle': 'issue'})
node_issue_fields.append({'name': 'field_issue_image_insert', 'type': 'node', 'bundle': 'issue'})
node_issue_fields.append({'name': 'field_issue_section_articles', 'type': 'field_collection_item', 'bundle': 'field_issue_section'})
node_issue_fields.append({'name': 'field_issue_section_display', 'type': 'field_collection_item', 'bundle': 'field_issue_section'})
node_issue_fields.append({'name': 'field_issue_section_title', 'type': 'field_collection_item', 'bundle': 'field_issue_section'})
node_issue_fields.append({'name': 'field_issue_section', 'type': 'node', 'bundle': 'issue'})
node_typemap['issue'] = node_issue_fields


# Module: cu_faq

#  Node: faqs

node_faqs_fields = []
node_faqs_fields.append({'name': 'body', 'type': 'node', 'bundle': 'faqs'})
node_faqs_fields.append({'name': 'field_qa', 'type': 'field_collection_item', 'bundle': 'field_qa_collection'})
node_faqs_fields.append({'name': 'field_qa_answer', 'type': 'field_collection_item', 'bundle': 'field_qa'})
node_faqs_fields.append({'name': 'field_qa_question', 'type': 'field_collection_item', 'bundle': 'field_qa'})
node_faqs_fields.append(
    {'name': 'field_qa_collection_title', 'type': 'field_collection_item', 'bundle': 'field_qa_collection'})
node_faqs_fields.append({'name': 'field_qa_collection', 'type': 'node', 'bundle': 'faqs'})
node_typemap['faqs'] = node_faqs_fields

# Module: photo_gallery

#  Node: photo_gallery

node_photo_gallery_fields = []
node_photo_gallery_fields.append({'name': 'body', 'type': 'node', 'bundle': 'photo_gallery'})
node_photo_gallery_fields.append({'name': 'field_photo', 'type': 'node', 'bundle': 'photo_gallery'})
node_typemap['photo_gallery'] = node_photo_gallery_fields

# Module: cu_newsletter

#  Node: newsletter

node_newsletter_fields = []
node_newsletter_fields.append({'name': 'body', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_ad_image', 'type': 'field_collection_item', 'bundle': 'field_newsletter_ad_promo'})
node_newsletter_fields.append({'name': 'field_newsletter_ad_link', 'type': 'field_collection_item', 'bundle': 'field_newsletter_ad_promo'})
node_newsletter_fields.append({'name': 'field_newsletter_ad_promo', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_intro_image', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_display', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section'})
node_newsletter_fields.append({'name': 'field_newsletter_more_link', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section'})
node_newsletter_fields.append({'name': 'field_newsletter_section_content', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section'})
node_newsletter_fields.append({'name': 'field_newsletter_articles', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section_content'})
node_newsletter_fields.append({'name': 'field_nl_section_content_body', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section_content'})
node_newsletter_fields.append({'name': 'field_nl_section_content_image', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section_content'})
node_newsletter_fields.append({'name': 'field_nl_section_content_title', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section_content'})
node_newsletter_fields.append({'name': 'field_newsletter_section_title', 'type': 'field_collection_item', 'bundle': 'field_newsletter_section'})
node_newsletter_fields.append({'name': 'field_newsletter_section', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_block_body', 'type': 'field_collection_item', 'bundle': 'field_newsletter_text_block'})
node_newsletter_fields.append({'name': 'field_newsletter_block_title', 'type': 'field_collection_item', 'bundle': 'field_newsletter_text_block'})
node_newsletter_fields.append({'name': 'field_newsletter_text_block', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_title', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_type', 'type': 'node', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_design', 'type': 'taxonomy_term', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_footer', 'type': 'taxonomy_term', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_name_image', 'type': 'taxonomy_term', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_path', 'type': 'taxonomy_term', 'bundle': 'newsletter'})
node_newsletter_fields.append({'name': 'field_newsletter_social_links', 'type': 'taxonomy_term', 'bundle': 'newsletter'})
node_typemap['newsletter'] = node_newsletter_fields





def get_field_collection_names(nodetype, fieldname):
    inner_collection_items = []
    for field in node_typemap[nodetype]:
        if field['bundle'] == fieldname and field['type'] == 'field_collection_item':
            inner_collection_items.append(field['name'])
    return inner_collection_items

def extract_field(type, fieldname, id, revision_id):
    field = {}
    field['field_name'] = fieldname
    field['type'] = type

    columns = extract_subfields(fieldname)

    data = []

    #print(f"select {', '.join(columns)} from field_data_{fieldname} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';")

    fd_result = conn.execute(sqlalchemy.text(
        f"select {', '.join(columns)} from field_data_{fieldname} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))

    for fd_item in fd_result.mappings():
        field_item = {}

        field_item['collection'] = []

        for colname in columns:
            field_item[colname] = fd_item[colname]

        if 'entity_id' in field_item and 'delta' in field_item:
            field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"



        data.append(field_item)
    field['data'] = data
    return field

def extract_fields2(type, id, revision_id):

    # print(f"EXTRACT_FIELDS2 A type: {type} id: {id} revision_id: {revision_id}")



    if type in node_typemap:

        field_names = node_typemap[type]

        fields = {}

        for fname in field_names:

            if fname['type'] == 'node':

                field = {}
                field['field_name'] = fname['name']
                field['type'] = type




                columns = extract_subfields(fname['name'])

                collection_fields = []
                for f2 in field_names:
                    if f2['type'] == 'field_collection_item' and f2['bundle'] == fname['name']:
                        collection_fields.append(f2)
                data = []

                # print(f"EXTRACT_FIELDS2 B type: {type} id: {id} revision_id: {revision_id}")
                #
                # print(f"TEST 1: {field['field_name']}")
                # print(collection_fields)
                # print(f"select {', '.join(columns)} from field_data_{fname['name']} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';")
                #

                fd_result = conn.execute(sqlalchemy.text(
                    f"select {', '.join(columns)} from field_data_{fname['name']} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))

                for fd_item in fd_result.mappings():

                    # print(f"TEST 2: {field['field_name']}")


                    field_item = {}

                    field_item['collection'] = []

                    for colname in columns:
                        field_item[colname] = fd_item[colname]

                    if 'entity_id' in field_item and 'delta' in field_item:
                        field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"

                    fci_item_fields = []



                    for fci_item in collection_fields:

                        # print(fci_item)

                        fci_columns = extract_subfields(fci_item['name'])

                        fci_id_column = fname['name'] + '_value'
                        fci_revision_column = fname['name'] + '_revision_id'

                        fci_query = f"select {', '.join(fci_columns)} from field_data_{fci_item['name']} where entity_type = '{fci_item['type']}' AND bundle = '{fci_item['bundle']}' AND entity_id = '{field_item[fci_id_column]}' AND revision_id = '{field_item[fci_revision_column]}';"
                        fci_result = conn.execute(sqlalchemy.text(fci_query))
                        for fcif in fci_result.mappings():
                            fci_data = {}
                            fcif_item = {}
                            for fcif_colname in fci_columns:
                                fcif_item[fcif_colname] = fcif[fcif_colname]

                                if fci_item[
                                    'name'] == 'field_callout_title' and fcif_colname == 'field_callout_title_url':

                                    if fcif_item[fcif_colname].find('#') != -1:
                                        fcif_item[fcif_colname] = fcif_item[fcif_colname].split('#')[0]

                                    if fcif_item[fcif_colname] in urlaliasmap:
                                        fcif_item[fcif_colname] = f"internal:/{urlaliasmap[fcif_item[fcif_colname]]}"
                            fci_data[fci_item['name']] = fcif_item

                            inner_collection_item_names = get_field_collection_names(type, fci_item['name'])



                            if len(inner_collection_item_names) > 0:
                                # print(inner_collection_item_names)

                                collection = {}

                                for item_name in inner_collection_item_names:

                                    #print(fci_data[fci_item['name']])
                                    fci_data[fci_item['name']]['id'] = str(fci_data[fci_item['name']]['entity_id']) + '_' + str(fci_data[fci_item['name']]['delta'])
                                    # print('test')
                                    # 
                                    # print(fci_data)





                                    local_id = fci_data[fci_item['name']][fci_item['name'] + '_value']
                                    local_revision_id = fci_data[fci_item['name']][fci_item['name'] + '_revision_id']
                                    # collection[item_name] = f'{item_name}, {local_id}, {local_revision_id}'
                                    collection[item_name] = extract_field(fci_item['name'], item_name, local_id, local_revision_id)



                                fci_data[fci_item['name']]['collection'] = collection

                                if fci_item['name'] == 'field_newsletter_section_content':
                                    # print('field_newsletter_section_content found')
                                    # pprint.pp(fci_data['field_newsletter_section_content']['collection']['field_nl_section_content_body']['data'])
                                    if len(fci_data['field_newsletter_section_content']['collection']['field_nl_section_content_body']['data']) > 0:
                                        pass
                                    else:
                                        fci_data['field_newsletter_section_article'] = fci_data.pop('field_newsletter_section_content')






                            fci_data['id'] = f"{field_item['entity_id']}_{field_item['delta']}"
                            field_item['collection'].append(fci_data)

                    if len(field_item['collection']) == 0:
                        del field_item['collection']


                    data.append(field_item)
                field['data'] = data


                if field['field_name'] == 'field_newsletter_ad_promo':
                    simple_ads = {}

                    # pprint.pp(field)

                    for idx, x in enumerate(field['data']):
                        # print(idx)
                        if 'collection' in field['data'][idx]:
                            # print(f"Index {idx}")
                            # print(field['data'][idx]['collection'])

                            for y in field['data'][idx]['collection']:

                                if 'field_newsletter_ad_image' in y:
                                    # print("test 1")
                                    # print(y['field_newsletter_ad_image']['field_newsletter_ad_image_fid'])
                                    if idx == 0:
                                        simple_ads['field_newsletter_promo_image_one'] = y['field_newsletter_ad_image']['field_newsletter_ad_image_fid']
                                    if idx == 1:
                                        simple_ads['field_newsletter_promo_image_two'] = y['field_newsletter_ad_image']['field_newsletter_ad_image_fid']
                                if 'field_newsletter_ad_link' in y:
                                    # print(y['field_newsletter_ad_link']['field_newsletter_ad_link_url'])
                                    if idx == 0:
                                        simple_ads['field_newsletter_promo_link_one'] = y['field_newsletter_ad_link']['field_newsletter_ad_link_url']
                                    if idx == 1:
                                        simple_ads['field_newsletter_promo_link_two'] = y['field_newsletter_ad_link']['field_newsletter_ad_link_url']
                    # print(simple_ads)
                    field['data'] = simple_ads
                        # image_fid
                        # pprint.pp(d)

                fields[field['field_name']] = field
        return fields


# Load fontawesome map

fa_map = {}
fa_shims = {}

with open('icons.yml') as f:
    fa_map = yaml.load(f, Loader=yaml.SafeLoader)
    
with open('shims.json') as f:
    shims_array = json.load(f)
    for shim in shims_array:
        fa_shims[shim[0]] = {}
        style = shim[1]
        if style == 'far':
            fa_shims[shim[0]]['style'] = 'regular'
        elif style == 'fab':
            fa_shims[shim[0]]['style'] = 'brands'
        else:
            fa_shims[shim[0]]['style'] = 'solid'

        fa_shims[shim[0]]['name'] = shim[2]





parser = argparse.ArgumentParser(description='Express Migration Tool')

parser.add_argument('-s', '--site', help='Sitename')

args = parser.parse_args()

sitename_clean = args.site.replace('-', '')


engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/{sitename_clean}?charset=utf8mb4", echo=False)

with (engine.connect() as conn):

    output = {}

    theme_result = conn.execute(sqlalchemy.text("select value from variable where name = 'theme_default';"))

    for x in theme_result:
        output['theme'] = str(phpserialize.loads(x[0], decode_strings=True))

    # Extract url_alias table
    urlaliasmap = {}
    urlalias_result = conn.execute(sqlalchemy.text("select pid, source, alias from url_alias;"))
    for x in urlalias_result:
        urlaliasmap[x.source] = x.alias



    urlaliases = []
    urlalias_result = conn.execute(sqlalchemy.text("select pid, source, alias from url_alias;"))
    for x in urlalias_result:
        urlalias = {}
        urlalias['pid'] = x.pid
        urlalias['source'] = x.source
        urlalias['alias'] = x.alias
        urlaliases.append(urlalias)
    output['urlaliases'] = urlaliases


    filemap = {}
    filemap['images'] = ['image/jpeg', 'image/png', 'image/gif']
    filemap['documents'] = ['application/pdf',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            'application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'application/msword',
                            'application/vnd.openxmlformats-officedocument.presentationml.presentation']
    filemap['video'] = []
    filemap['audio'] = []

    files = {}
    files['images'] = []
    files['videos'] = []
    files['audio'] = []
    files['documents'] = []


    files_result = conn.execute(sqlalchemy.text("select fid, uid, filename, uri, filemime, filesize, status, timestamp, type from file_managed;"))
    for x in files_result:
        file = {}
        file['fid'] = x.fid
        file['uid'] = x.uid
        file['filename'] = x.filename
        file['uri'] = x.uri
        file['filemime'] = x.filemime
        file['filesize'] = x.filesize
        file['status'] = x.status
        file['timestamp'] = x.timestamp
        file['type'] = x.type

        if x.uri[:6] == 'public':
            file['filepath'] = '../../files/' + x.uri[9:]
        elif x.uri[:7] == 'private':
            file['filepath'] = '../../files/private/' + x.uri[10:]


        if x.filemime in filemap['images']:
            fp_result = conn.execute(sqlalchemy.text(f"select focal_point from focal_point where fid = '{file['fid']}';"))
            for fp in fp_result:
                file['focal_point'] = f"{file['fid']},{fp.focal_point}"
            files['images'].append(file)
        if x.filemime in filemap['video']:
            files['video'].append(file)
        if x.filemime in filemap['audio']:
            files['audio'].append(file)
        if x.filemime in filemap['documents']:
            files['documents'].append(file)

    output['files'] = files

    users = []

    users_result = conn.execute(sqlalchemy.text("select uid, name, mail, created, access, login, status from users;"))
    for x in users_result:

        skiplist = []
        # skiplist.append('alco6164')
        # skiplist.append('mibo7729')
        # skiplist.append('jesp3304')
        # skiplist.append('fraziere')
        # skiplist.append('jesp3304')
        # skiplist.append('wetu1300')
        # skiplist.append('linebarg')
        # skiplist.append('brokaw')
        # skiplist.append('crafts')
        skiplist.append('')

        if x[1] in skiplist or x[0] == 1:
            continue

        user = {}
        user['uid'] = x[0]
        user['name'] = x[1]
        user['mail'] = x[2]
        user['created'] = x[3]
        user['access'] = x[4]
        user['login'] = x[5]
        user['status'] = x[6]

        roles = []

        roles_result = conn.execute(sqlalchemy.text(f"select r.name from users u, users_roles ur, role r WHERE u.uid = ur.uid AND ur.rid = r.rid AND u.uid = '{x[0]}';"))

        rolemap = {}
        rolemap['site_owner'] = ['site_owner', 'site_manager']
        rolemap['site_editor'] = ['content_editor']
        rolemap['content_editor'] = ['content_editor']
        rolemap['edit_only'] = ['content_editor']
        rolemap['edit_my_content'] = ['edit_own_content']
        rolemap['form_manager'] = ['webform_editor']
        rolemap['administrator'] = ['architect']
        rolemap['developer'] = ['developer']
        rolemap['access_manager'] = []
        rolemap['configuration_manager'] = ['site_manager']
        rolemap['campaign_manager'] = []
        rolemap['form_submitter'] = []


        for y in roles_result:

            roles.extend(rolemap[y[0]])

        user['roles'] = roles

        if len(roles) > 0:
            users.append(user)
    output['users'] = users




    # Beans

    bean_types = {}

    # Module: cu_block_section

    #  Bean: block_section

    bean_block_section_fields = []
    bean_block_section_fields.append({'name': 'field_block_section_bg_effect', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_bg_image', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_bg_image_m', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_bg_image_t', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_content_bg', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_mobile_pad', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_padding', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_block_section_tablet_pad', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_blocks_section_blocks', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_hero_unit_bg_color', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_hero_unit_overlay', 'type': 'bean', 'bundle': 'block_section'})
    bean_block_section_fields.append({'name': 'field_hero_unit_text_color', 'type': 'bean', 'bundle': 'block_section'})
    bean_types['block_section'] = bean_block_section_fields

    # Module: cu_slider

    #  Bean: slider

    bean_slider_fields = []
    bean_slider_fields.append({'name': 'field_slider_design_style', 'type': 'bean', 'bundle': 'slider'})
    bean_slider_fields.append({'name': 'field_slider_size', 'type': 'bean', 'bundle': 'slider'})
    bean_slider_fields.append({'name': 'field_slider_caption', 'type': 'field_collection_item', 'bundle': 'field_slider_slide'})
    bean_slider_fields.append({'name': 'field_slider_image', 'type': 'field_collection_item', 'bundle': 'field_slider_slide'})
    bean_slider_fields.append({'name': 'field_slider_link', 'type': 'field_collection_item', 'bundle': 'field_slider_slide'})
    bean_slider_fields.append({'name': 'field_slider_teaser', 'type': 'field_collection_item', 'bundle': 'field_slider_slide'})
    bean_slider_fields.append({'name': 'field_slider_slide', 'type': 'bean', 'bundle': 'slider'})
    bean_types['slider'] = bean_slider_fields

    # Module: cu_video_reveal

    #  Bean: video_reveal

    bean_video_reveal_fields = []
    bean_video_reveal_fields.append({'name': 'field_video_reveal_image', 'type': 'bean', 'bundle': 'video_reveal'})
    bean_video_reveal_fields.append({'name': 'field_video_reveal_text', 'type': 'bean', 'bundle': 'video_reveal'})
    bean_video_reveal_fields.append({'name': 'field_video_reveal_url', 'type': 'bean', 'bundle': 'video_reveal'})
    bean_types['video_reveal'] = bean_video_reveal_fields

    # Module: cu_block_row

    #  Bean: block_row

    bean_block_row_fields = []
    bean_block_row_fields.append({'name': 'field_block_row_block', 'type': 'field_collection_item', 'bundle': 'field_block_row_collection'})
    bean_block_row_fields.append({'name': 'field_block_row_collection', 'type': 'bean', 'bundle': 'block_row'})
    bean_block_row_fields.append({'name': 'field_block_row_distribution', 'type': 'bean', 'bundle': 'block_row'})
    bean_block_row_fields.append({'name': 'field_block_row_match_height', 'type': 'bean', 'bundle': 'block_row'})
    bean_types['block_row'] = bean_block_row_fields

    # Module: cu_block

    #  Bean: block

    bean_block_fields = []
    bean_block_fields.append({'name': 'field_block_photo', 'type': 'bean', 'bundle': 'block'})
    bean_block_fields.append({'name': 'field_block_text', 'type': 'bean', 'bundle': 'block'})
    bean_types['block'] = bean_block_fields

    # Module: cu_block_to_bean

    #  Bean: block_wrapper

    bean_block_wrapper_fields = []
    bean_block_wrapper_fields.append({'name': 'field_block_wrapper_reference', 'type': 'bean', 'bundle': 'block_wrapper'})
    bean_types['block_wrapper'] = bean_block_wrapper_fields

    # bean_campus_news_bundle_fields = []
    # bean_campus_news_bundle_fields.append('field_campus_news_audience')
    # bean_campus_news_bundle_fields.append('field_campus_news_category')
    # bean_campus_news_bundle_fields.append('field_campus_news_display')
    # bean_campus_news_bundle_fields.append('field_campus_news_items')
    # bean_campus_news_bundle_fields.append('field_campus_news_unit')
    # bean_types['campus_news_bundle'] = bean_campus_news_bundle_fields
    #
    # bean_collection_grid_fields = []
    # bean_collection_grid_fields.append('field_collection_body')
    # bean_collection_grid_fields.append('field_collection_category')
    # bean_collection_grid_fields.append('field_collection_category_bg')
    # bean_collection_grid_fields.append('field_collection_display_summary')
    # bean_collection_grid_fields.append('field_collection_filter_effect')
    # bean_collection_grid_fields.append('field_collection_filter_type')
    # bean_collection_grid_fields.append('field_collection_grid_categories')
    # bean_collection_grid_fields.append('field_collection_grid_category')
    # bean_collection_grid_fields.append('field_collection_grid_label')
    # bean_collection_grid_fields.append('field_collection_grid_type')
    # bean_collection_grid_fields.append('field_collection_image')
    # bean_collection_grid_fields.append('field_collection_multiselect')
    # bean_collection_grid_fields.append('field_collection_preview')
    # bean_collection_grid_fields.append('field_collection_thumbnail')
    # bean_collection_grid_fields.append('field_collection_type')
    # bean_types['collection_grid'] = bean_collection_grid_fields
    #

    # Module: cu_content_sequence

    #  Bean: content_sequence

    bean_content_sequence_fields = []
    bean_content_sequence_fields.append({'name': 'field_cont_seq_body', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_date', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_display_date', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_display_end_date', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_end_date', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_group', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_photos', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_title', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_video', 'type': 'field_collection_item', 'bundle': 'field_cont_seq_content'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_content', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_description', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_display', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_photos', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_content_sequence_fields.append({'name': 'field_cont_seq_scale', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_content_sequence_fields.append({'name': 'field_cont_sequence_title', 'type': 'bean', 'bundle': 'content_sequence'})
    bean_types['content_sequence'] = bean_content_sequence_fields

    # Module: cu_feature_callout

    #  Bean: feature_callout

    bean_feature_callout_fields = []
    bean_feature_callout_fields.append({'name': 'field_callout_columns', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_image_size', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_style', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_image', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_feature_callout_fields.append({'name': 'field_callout_text', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_feature_callout_fields.append({'name': 'field_callout_title', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_feature_callout_fields.append({'name': 'field_callouts', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_types['feature_callout'] = bean_feature_callout_fields

    # Module: cu_hero_unit

    #  Bean: hero_unit

    bean_hero_unit_fields = []
    bean_hero_unit_fields.append({'name': 'field_hero_unit_bg_color', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_headline', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_image', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_link', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_link_color', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_overlay', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_size', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_size_priority', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_text', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_text_align', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_hero_unit_fields.append({'name': 'field_hero_unit_text_color', 'type': 'bean', 'bundle': 'hero_unit'})
    bean_types['hero_unit'] = bean_hero_unit_fields

    # Module: express_localist_bundle

    #  Bean: localist_events

    bean_localist_events_fields = []
    bean_localist_events_fields.append({'name': 'field_localist_all_instances', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_content_match', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_days_ahead', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_filters', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_filters_excluded', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_groups', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_hide_descriptions', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_hide_images', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_hide_past_events', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_hide_times', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_link', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_minical_layout', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_new_window', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_places', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_render_html', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_results', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_show_featured', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_show_sponsored', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_skip_recurring', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_start_date', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_style', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_tags', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_truncate_desc', 'type': 'bean', 'bundle': 'localist_events'})
    bean_localist_events_fields.append({'name': 'field_localist_widget_type', 'type': 'bean', 'bundle': 'localist_events'})
    bean_types['localist_events'] = bean_localist_events_fields


    # Module: people_content_type

    #  Bean: people_list_block

    bean_people_list_block_fields = []
    bean_people_list_block_fields.append({'name': 'field_people_block_thumbnail', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_1', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_2', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_3', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_list_department', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_list_person_type', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_types['people_list_block'] = bean_people_list_block_fields

    # Module: cu_video_hero_unit

    #  Bean: video_hero_unit

    bean_video_hero_unit_fields = []
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_headline', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_image', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_link', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_link_color', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_text', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_text_align', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_unit_text_color', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_video_overlay', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_hero_video_size', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_video_hero_unit_fields.append({'name': 'field_video_hero_url', 'type': 'bean', 'bundle': 'video_hero_unit'})
    bean_types['video_hero_unit'] = bean_video_hero_unit_fields

    # Module: people_content_type

    #  Bean: people_list_block

    bean_people_list_block_fields = []
    bean_people_list_block_fields.append({'name': 'field_people_block_thumbnail', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_1', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_2', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_filter_3', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_list_department', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_people_list_block_fields.append({'name': 'field_people_list_person_type', 'type': 'bean', 'bundle': 'people_list_block'})
    bean_types['people_list_block'] = bean_people_list_block_fields

    # Module: cu_expandable

    #  Bean: expandable

    bean_expandable_fields = []
    bean_expandable_fields.append({'name': 'field_expandable_display', 'type': 'bean', 'bundle': 'expandable'})
    bean_expandable_fields.append({'name': 'field_expandable_block', 'type': 'field_collection_item', 'bundle': 'field_expandable_section'})
    bean_expandable_fields.append({'name': 'field_expandable_block_titles', 'type': 'field_collection_item', 'bundle': 'field_expandable_section'})
    bean_expandable_fields.append({'name': 'field_expandable_text', 'type': 'field_collection_item', 'bundle': 'field_expandable_section'})
    bean_expandable_fields.append({'name': 'field_expandable_title', 'type': 'field_collection_item', 'bundle': 'field_expandable_section'})
    bean_expandable_fields.append({'name': 'field_expandable_section', 'type': 'bean', 'bundle': 'expandable'})
    bean_expandable_fields.append({'name': 'field_expandable_section_open', 'type': 'bean', 'bundle': 'expandable'})
    bean_expandable_fields.append({'name': 'field_expandable_select_prompt', 'type': 'bean', 'bundle': 'expandable'})
    bean_types['expandable'] = bean_expandable_fields

    # Module: cu_article

    #  Bean: article_feature

    bean_article_feature_fields = []
    bean_article_feature_fields.append({'name': 'field_article_exclude_category', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_exclude_tag', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_feature_category', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_feature_display', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_feature_filter', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_feature_image_size', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_feature_show_cat', 'type': 'bean', 'bundle': 'article_feature'})
    bean_article_feature_fields.append({'name': 'field_article_link', 'type': 'bean', 'bundle': 'article_feature'})
    bean_types['article_feature'] = bean_article_feature_fields

    #  Bean: article_grid

    bean_article_grid_fields = []
    bean_article_grid_fields.append({'name': 'field_article_exclude_category', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_exclude_tag', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_grid_category', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_grid_filter', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_grid_items', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_grid_more_link', 'type': 'bean', 'bundle': 'article_grid'})
    bean_article_grid_fields.append({'name': 'field_article_grid_summary', 'type': 'bean', 'bundle': 'article_grid'})
    bean_types['article_grid'] = bean_article_grid_fields

    #  Bean: article_slider

    bean_article_slider_fields = []
    bean_article_slider_fields.append({'name': 'field_article_exclude_category', 'type': 'bean', 'bundle': 'article_slider'})
    bean_article_slider_fields.append({'name': 'field_article_exclude_tag', 'type': 'bean', 'bundle': 'article_slider'})
    bean_article_slider_fields.append({'name': 'field_article_slider_category', 'type': 'bean', 'bundle': 'article_slider'})
    bean_article_slider_fields.append({'name': 'field_article_slider_filter', 'type': 'bean', 'bundle': 'article_slider'})
    bean_types['article_slider'] = bean_article_slider_fields

    #  Bean: articles

    bean_articles_fields = []
    bean_articles_fields.append({'name': 'field_article_display', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_exclude_category', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_exclude_tag', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_items_display', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_link', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_list_category', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_pager', 'type': 'bean', 'bundle': 'articles'})
    bean_articles_fields.append({'name': 'field_article_term', 'type': 'bean', 'bundle': 'articles'})
    bean_types['articles'] = bean_articles_fields

    # Module: cu_social_links

    #  Bean: social_links

    bean_social_links_fields = []
    bean_social_links_fields.append({'name': 'field_social_links_arrangement', 'type': 'bean', 'bundle': 'social_links'})
    bean_social_links_fields.append({'name': 'field_social_links_body', 'type': 'bean', 'bundle': 'social_links'})
    bean_social_links_fields.append({'name': 'field_social_link_type', 'type': 'field_collection_item', 'bundle': 'field_social_links_collection'})
    bean_social_links_fields.append({'name': 'field_social_link_url', 'type': 'field_collection_item', 'bundle': 'field_social_links_collection'})
    bean_social_links_fields.append({'name': 'field_social_links_collection', 'type': 'bean', 'bundle': 'social_links'})
    bean_social_links_fields.append({'name': 'field_social_links_homepage_url', 'type': 'bean', 'bundle': 'social_links'})
    bean_social_links_fields.append({'name': 'field_social_links_size', 'type': 'bean', 'bundle': 'social_links'})
    bean_types['social_links'] = bean_social_links_fields

    # Module: express_collections_bundle

    #  Bean: collection_grid

    bean_collection_grid_fields = []
    bean_collection_grid_fields.append({'name': 'field_collection_display_summary', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_filter_effect', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_filter_type', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_category_bg', 'type': 'field_collection_item', 'bundle': 'field_collection_grid_categories'})
    bean_collection_grid_fields.append({'name': 'field_collection_grid_category', 'type': 'field_collection_item', 'bundle': 'field_collection_grid_categories'})
    bean_collection_grid_fields.append({'name': 'field_collection_grid_label', 'type': 'field_collection_item', 'bundle': 'field_collection_grid_categories'})
    bean_collection_grid_fields.append({'name': 'field_collection_grid_categories', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_grid_category', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_grid_type', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_collection_grid_fields.append({'name': 'field_collection_multiselect', 'type': 'bean', 'bundle': 'collection_grid'})
    bean_types['collection_grid'] = bean_collection_grid_fields

    beans = []
    bean_result = conn.execute(sqlalchemy.text("select bid, vid, delta, label, title, type, view_mode, data, uid, created, changed from bean;"))
    bean_types_map = {}
    for x in bean_result:
        bean = {}
        bean['bid'] = x.bid
        bean['vid'] = x.vid
        bean['delta'] = x.delta
        bean['label'] = x.label
        bean['title'] = x.title
        bean['type'] = x.type
        bean['view_mode'] = x.view_mode
        bean['data'] = x.data
        bean['uid'] = x.uid
        bean['created'] = x.created
        bean['changed'] = x.changed

        bean['display_title'] = 'true'

        if len(bean['title'].strip()) == 0:
            bean['title'] = bean['label']
            bean['display_title'] = 'false'





        bean_fields = []



        #bean['fields'] = extract_fields(b.type, b.bid, b.vid)


        # beans.append(bean)


        if x.type in bean_types:

            field_names = bean_types[x.type]

            fields = {}

            for fname in field_names:

                if fname['type'] == 'bean':

                    field = {}
                    field['field_name'] = fname['name']
                    field['type'] = bean['type']

                    columns = extract_subfields(fname['name'])

                    collection_fields = []
                    for f2 in field_names:
                        if f2['type'] == 'field_collection_item' and f2['bundle'] == fname['name']:
                            collection_fields.append(f2)
                    data = []

                    fd_result = conn.execute(sqlalchemy.text(
                        f"select {', '.join(columns)} from field_data_{fname['name']} where bundle = '{bean['type']}' AND entity_id = '{bean['bid']}' AND revision_id = '{bean['vid']}';"))

                    for fd_item in fd_result.mappings():
                        field_item = {}

                        field_item['collection'] = []

                        # if fname['name'] == 'field_localist_start_date':
                        #     print("date test A")
                        #     print(fd_item['field_localist_start_date_value'])
                        #     print("date test B")

                        for colname in columns:
                            field_item[colname] = fd_item[colname]

                        if 'entity_id' in field_item and 'delta' in field_item:
                            field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"

                        fci_item_fields = []

                        for fci_item in collection_fields:
                            fci_columns = extract_subfields(fci_item['name'])

                            fci_id_column = fname['name'] + '_value'
                            fci_revision_column = fname['name'] + '_revision_id'

                            fci_query = f"select {', '.join(fci_columns)} from field_data_{fci_item['name']} where entity_type = '{fci_item['type']}' AND bundle = '{fci_item['bundle']}' AND entity_id = '{field_item[fci_id_column]}' AND revision_id = '{field_item[fci_revision_column]}';"
                            fci_result = conn.execute(sqlalchemy.text(fci_query))
                            for fcif in fci_result.mappings():
                                fci_data = {}
                                fcif_item = {}
                                for fcif_colname in fci_columns:
                                    fcif_item[fcif_colname] = fcif[fcif_colname]

                                    if fci_item['name'] == 'field_callout_title' and fcif_colname == 'field_callout_title_url':

                                        if fcif_item[fcif_colname].find('#') != -1:
                                            fcif_item[fcif_colname] = fcif_item[fcif_colname].split('#')[0]

                                        if fcif_item[fcif_colname] in urlaliasmap:
                                            fcif_item[fcif_colname] = f"internal:/{urlaliasmap[fcif_item[fcif_colname]]}"
                                fci_data[fci_item['name']] = fcif_item

                                fci_data['id'] = f"{field_item['entity_id']}_{field_item['delta']}"
                                field_item['collection'].append(fci_data)

                        if len(field_item['collection']) == 0:
                            del field_item['collection']

                        data.append(field_item)
                    field['data'] = data
                    fields[field['field_name']] = field

            # #testtest
            # if 'field_hero_unit_link' in fields:
            #     if 'data' in fields['field_hero_unit_link']:
            #         for data in fields['field_hero_unit_link']['data']:
            #             if 'field_hero_unit_link_url' in data:
            #                 if str(data['field_hero_unit_link_url'][0:5]) == 'node/':
            #                     data['field_hero_unit_link_url'] = 'internal:/' + data['field_hero_unit_link_url']
            #                 if str(data['field_hero_unit_link_url'][0:1]) == '/':
            #                     data['field_hero_unit_link_url'] = 'internal:' + data['field_hero_unit_link_url']

            # if bean['type'] == 'feature_callout':
                # pprint.pprint(fields)
                # print('test 0')
                #
                # if 'field_callouts' in fields:
                #     if 'data' in fields['field_callouts']:
                #         for d1 in fields['field_callouts']['data']:
                #             # pprint.pp(d1)
                #             if 'collection' in d1:
                #                 for c1 in d1['collection']:
                #                     if 'field_callout_title' in c1:
                #                         if 'field_callout_title_url' in c1['field_callout_title']:
                #                             if str(c1['field_callout_title']['field_callout_title_url']) == '':
                #                                 c1['field_callout_title'].pop('field_callout_title_url')
                #                             elif str(c1['field_callout_title']['field_callout_title_url'][0:5]) == 'node/':
                #                                 c1['field_callout_title']['field_callout_title_url'] = 'internal:/' + c1['field_callout_title']['field_callout_title_url']
                #                             elif str(c1['field_callout_title']['field_callout_title_url'][0:1]) == '/':
                #                                 c1['field_callout_title']['field_callout_title_url'] = 'internal:' + c1['field_callout_title']['field_callout_title_url']
                #                             elif str(c1['field_callout_title']['field_callout_title_url'][0:7]) == 'mailto:':
                #                                 pass
                #                             elif str(c1['field_callout_title']['field_callout_title_url'][0:4]) == 'tel:':
                #                                 pass
                #                             elif ':' not in str(c1['field_callout_title']['field_callout_title_url']) and '.' not in str(c1['field_callout_title']['field_callout_title_url']):
                #                                 c1['field_callout_title']['field_callout_title_url'] = 'internal:/' + c1['field_callout_title']['field_callout_title_url']
                #

            bean['fields'] = fields

        if bean['type'] == 'feature_callout':
            #print(bean['fields']['field_callout_style']['data'][0]['field_callout_style_value'])

            if len(bean['fields']['field_callout_style']['data']) > 0:
                if bean['fields']['field_callout_style']['data'][0]['field_callout_style_value'] in ['large_teaser', 'large_teaser_alt', 'teaser', 'tiles', 'tiles_alt', 'feature', 'tiles_large']:
                    bean['type'] = 'content_row'

        if bean['type'] == 'block_wrapper':
            if len(bean['fields']['field_block_wrapper_reference']['data']) > 0:
                webform_nid = bean['fields']['field_block_wrapper_reference']['data'][0]['field_block_wrapper_reference_value'][13:]
                bean['fields']['field_block_wrapper_reference']['data'][0]['field_block_wrapper_reference_value'] = webform_nid
            else:
                print("Block wrapper data empty", file=sys.stderr)

        if bean['type'] == 'localist_events':
            eventdata = {}
            eventdata['schools'] = 'ucboulder'

            eventfields = []
            eventfields.append({'field': 'field_localist_results', 'param': 'num'})
            eventfields.append({'field': 'field_localist_days_ahead', 'param': 'days'})
            eventfields.append({'field': 'field_localist_show_featured', 'param': 'picks'})
            eventfields.append({'field': 'field_localist_show_sponsored', 'param': 'sponsored'})
            eventfields.append({'field': 'field_localist_content_match', 'param': 'match'})
            eventfields.append({'field': 'field_localist_hide_past_events', 'param': 'hide_past'})
            eventfields.append({'field': 'field_localist_hide_descriptions', 'param': 'hidedesc'})
            eventfields.append({'field': 'field_localist_truncate_desc', 'param': 'expand_descriptions'})
            eventfields.append({'field': 'field_localist_render_html', 'param': 'html_descriptions'})
            eventfields.append({'field': 'field_localist_hide_images', 'param': 'hideimage'})
            eventfields.append({'field': 'field_localist_hide_times', 'param': 'show_times'})
            eventfields.append({'field': 'field_localist_new_window', 'param': 'target_blank'})
            eventfields.append({'field': 'field_localist_skip_recurring', 'param': 'skip_recurring'})
            eventfields.append({'field': 'field_localist_all_instances', 'param': 'all_instances'})
            eventfields.append({'field': 'field_localist_style', 'param': 'template'})

            eventfields.append({'field': 'field_localist_places', 'param': 'venues'})
            eventfields.append({'field': 'field_localist_filters', 'param': 'types'})
            eventfields.append({'field': 'field_localist_filters_excluded', 'param': 'exclude_types'})
            eventfields.append({'field': 'field_localist_groups', 'param': 'groups'})
            eventfields.append({'field': 'field_localist_tags', 'param': 'tags'})
            eventfields.append({'field': 'field_localist_start_date', 'param': 'start'})

            for f in eventfields:
                if len(bean['fields'][f['field']]['data']) > 0:
                    if f['field'] == 'field_localist_places' or f['field'] == 'field_localist_groups' or f['field'] == 'field_localist_tags':
                        eventdata[f['param']] = []
                        for x in bean['fields'][f['field']]['data']:
                            eventdata[f['param']].append(x[f['field'] + "_value"])
                        eventdata[f['param']] = ','.join(eventdata[f['param']])
                    else:
                        eventdata[f['param']] = bean['fields'][f['field']]['data'][0][f['field'] + "_value"]



            if 'types' not in eventdata:
                eventdata['types'] = 0

            if 'exclude_types' not in eventdata:
                eventdata['exclude_types'] = 0

            if 'start' in eventdata:
                eventdata['start'] = dateutil.parser.parse(str(eventdata['start'])).strftime("%Y-%m-%d")

            params = ""
            for param in eventdata:
                if str(eventdata[param]) != '0':
                    params += f"{param}={eventdata[param]}&"

            # print(params)

            params = params[:-1]
            params += "&show-types=0"
            url = f'<script type="text/javascript" src="https://calendar.colorado.edu/widget/view?{params}"></script>'

            bean['fields']['url'] = url




        # Block Style Mapping
        # [exbd_icon] => field_bs_icon
        # [exbd_icon_position] => field_bs_icon_position
        # [exbd_icon_color] => field_bs_icon_color
        # [exbd_icon_size] => field_bs_icon_size
        # [exbd_heading] => field_bs_heading
        # [exbd_heading_align] => field_bs_heading_alignment
        # [exbd_heading_style] => field_bs_heading_style
        # [exbd_style] => field_bs_background_style
        # [exbd_font_scale_title] => field_bs_title_font_scale
        # [exbd_font_scale_content] => field_bs_content_font_scale
        # [exbd_menu_style] =>

        style_value_map = {}

        style_value_map['icon_position'] = {}
        style_value_map['icon_position']['default'] = 'bs_icon_position_default'
        style_value_map['icon_position']['inline'] = 'bs_icon_position_default'
        style_value_map['icon_position']['offset'] = 'bs_icon_position_offset'
        style_value_map['icon_position']['top'] = 'bs_icon_position_top'

        style_value_map['icon_color'] = {}
        style_value_map['icon_color']['default'] = 'bs_icon_color_default'
        style_value_map['icon_color']['gray'] = 'bs_icon_color_gray'
        style_value_map['icon_color']['gold'] = 'bs_icon_color_gold'
        style_value_map['icon_color']['blue'] = 'bs_icon_color_blue'
        style_value_map['icon_color']['green'] = 'bs_icon_color_green'
        style_value_map['icon_color']['orange'] = 'bs_icon_color_orange'
        style_value_map['icon_color']['purple'] = 'bs_icon_color_purple'
        style_value_map['icon_color']['red'] = 'bs_icon_color_red'
        style_value_map['icon_color']['yellow'] = 'bs_icon_color_yellow'

        style_value_map['icon_size'] = {}
        style_value_map['icon_size']['default'] = 'bs_icon_size_default'
        style_value_map['icon_size']['increase'] = 'bs_icon_size_increase'

        style_value_map['heading'] = {}
        style_value_map['heading']['default'] = 'bs_heading_default'
        style_value_map['heading']['h2'] = 'bs_heading_default'
        style_value_map['heading']['h3'] = 'bs_heading_h3'
        style_value_map['heading']['h4'] = 'bs_heading_h4'
        style_value_map['heading']['h5'] = 'bs_heading_h5'
        style_value_map['heading']['h6'] = 'bs_heading_h6'
        style_value_map['heading']['strong'] = 'bs_heading_strong'

        style_value_map['heading_alignment'] = {}
        style_value_map['heading_alignment']['default'] = 'bs_heading_align_default'
        style_value_map['heading_alignment']['left'] = 'bs_heading_align_default'
        style_value_map['heading_alignment']['centered'] = 'bs_heading_align_centered'

        style_value_map['heading_style'] = {}
        style_value_map['heading_style']['default'] = 'bs_heading_style_default'
        style_value_map['heading_style']['hero'] = 'bs_heading_style_default_hero'
        style_value_map['heading_style']['hero-bold'] = 'bs_heading_style_default_hero_bold'
        style_value_map['heading_style']['supersize'] = 'bs_heading_style_default_supersize'
        style_value_map['heading_style']['supersize-bold'] = 'bs_heading_style_default_supersize_bold'

        style_value_map['background_style'] = {}
        style_value_map['background_style']['none'] = 'bs_background_style_none'
        style_value_map['background_style'][None] = 'bs_background_style_none'
        style_value_map['background_style']['default'] = 'bs_background_style_none'
        style_value_map['background_style']['white'] = 'bs_background_style_white'
        style_value_map['background_style']['light_gray'] = 'bs_background_style_gray'
        style_value_map['background_style']['dark_gray'] = 'bs_background_style_dark_gray'
        style_value_map['background_style']['tan'] = 'bs_background_style_tan'
        style_value_map['background_style']['light_blue'] = 'bs_background_style_light_blue'
        style_value_map['background_style']['lightblue'] = 'bs_background_style_light_blue'
        style_value_map['background_style']['blue-medium'] = 'bs_background_style_medium_blue'
        style_value_map['background_style']['blue-dark'] = 'bs_background_style_dark_blue'
        style_value_map['background_style']['green-light'] = 'bs_background_style_light_green'
        style_value_map['background_style']['brick'] = 'bs_background_style_brick'
        style_value_map['background_style']['outline'] = 'bs_background_style_outline'
        style_value_map['background_style']['underline'] = 'bs_background_style_underline'

        style_value_map['title_font_scale'] = {}
        style_value_map['title_font_scale']['default'] = 'bs_title_font_scale_default'
        style_value_map['title_font_scale']['increase'] = 'bs_title_font_scale_increase'
        style_value_map['title_font_scale']['decrease'] = 'bs_title_font_scale_decrease'

        style_value_map['content_font_scale'] = {}
        style_value_map['content_font_scale']['default'] = 'bs_content_font_scale_default'
        style_value_map['content_font_scale']['increase'] = 'bs_content_font_scale_increase'
        style_value_map['content_font_scale']['decrease'] = 'bs_content_font_scale_decrease'


        bean['style'] = {}
        bean['style']['icon'] = ''
        bean['style']['icon_position'] = 'default'
        bean['style']['icon_color'] = 'default'
        bean['style']['icon_size'] = 'default'
        bean['style']['heading'] = 'default'
        bean['style']['heading_alignment'] = 'default'
        bean['style']['heading_style'] = 'default'
        bean['style']['background_style'] = 'none'
        bean['style']['title_font_scale'] = 'default'
        bean['style']['content_font_scale'] = 'default'

        style_result = conn.execute(sqlalchemy.text(f"SELECT block_settings, block_theme FROM bean a, express_block_designer b WHERE a.delta = b.block_delta AND a.bid = '{bean['bid']}';"))

        for style in style_result:

            styles = phpserialize.loads(style.block_settings, decode_strings=True)

            bean['style']['icon'] = styles['exbd_icon']

            if 'exbd_icon_position' in styles:
                bean['style']['icon_position'] = styles['exbd_icon_position']
            bean['style']['icon_color'] = styles['exbd_icon_color']
            bean['style']['icon_size'] = styles['exbd_icon_size']
            bean['style']['heading'] = styles['exbd_heading']
            bean['style']['heading_alignment'] = styles['exbd_heading_align']
            if 'exbd_heading_style' in styles:
                bean['style']['heading_style'] = styles['exbd_heading_style']
            bean['style']['background_style'] = styles['exbd_style']
            bean['style']['title_font_scale'] = styles['exbd_font_scale_title']
            bean['style']['content_font_scale'] = styles['exbd_font_scale_content']

            if style.block_theme is not None:
                theme_result = conn.execute(sqlalchemy.text(f"SELECT block_settings FROM express_block_designer_themes WHERE id = '{style.block_theme}';"))


                for theme in theme_result:
                    theme_styles = phpserialize.loads(theme.block_settings, decode_strings=True)

                    bean['style']['icon_position'] = theme_styles['exbd_icon_position']
                    bean['style']['icon_color'] = theme_styles['exbd_icon_color']
                    bean['style']['icon_size'] = theme_styles['exbd_icon_size']
                    bean['style']['heading'] = theme_styles['exbd_heading']
                    bean['style']['heading_alignment'] = theme_styles['exbd_heading_align']
                    if 'exbd_heading_style' in theme_styles:
                        bean['style']['heading_style'] = theme_styles['exbd_heading_style']
                    bean['style']['background_style'] = theme_styles['exbd_style']
                    bean['style']['title_font_scale'] = theme_styles['exbd_font_scale_title']
                    bean['style']['content_font_scale'] = theme_styles['exbd_font_scale_content']

        bean['style']['icon_position'] = style_value_map['icon_position'][bean['style']['icon_position']]
        bean['style']['icon_color'] = style_value_map['icon_color'][bean['style']['icon_color']]
        bean['style']['icon_size'] = style_value_map['icon_size'][bean['style']['icon_size']]
        bean['style']['heading'] = style_value_map['heading'][bean['style']['heading']]
        bean['style']['heading_alignment'] = style_value_map['heading_alignment'][bean['style']['heading_alignment']]
        bean['style']['heading_style'] = style_value_map['heading_style'][bean['style']['heading_style']]


        bean['style']['background_style'] = style_value_map['background_style'][bean['style']['background_style']]
        bean['style']['title_font_scale'] = style_value_map['title_font_scale'][bean['style']['title_font_scale']]
        bean['style']['content_font_scale'] = style_value_map['content_font_scale'][bean['style']['content_font_scale']]


        if bean['style']['icon'] == 'none' or bean['style']['icon'] == '':
            bean['style']['icon'] = ''
        else:
            fa_style = ''
            fa_name = ''

            if bean['style']['icon'][3:] in fa_shims:
                fa_style = fa_shims[bean['style']['icon'][3:]]['style']
            elif bean['style']['icon'][3:] in fa_map:
                fa_style = fa_map[bean['style']['icon'][3:]]['styles'][0]
            else:
                fa_style = 'solid'

            if bean['style']['icon'][3:] in fa_map:
                fa_name = bean['style']['icon'][3:]
            elif bean['style']['icon'][3:] in fa_shims:
                fa_name = fa_shims[bean['style']['icon'][3:]]['name']
            else:
                fa_name = bean['style']['icon'][3:]

            bean['style']['icon'] = f'<i class="fa-{fa_style} fa-{fa_name}">&nbsp;</i>'

        if bean['type'] not in bean_types_map:
            bean_types_map[bean['type']] = []
        bean_types_map[bean['type']].append(bean)

        # print(bean_types)

        #beans.append(bean)

    #output['beans'] = beans
    output['beans'] = bean_types_map


    def get_bean_type(bid):
        for type in bean_types_map:
            for bean in bean_types_map[type]:
                if bean['bid'] == bid:
                    return type

    def get_bean(bid):
        for type in bean_types_map:
            for bean in bean_types_map[type]:
                if bean['bid'] == bid:
                    return bean




    nodes = []

    node_types = {}

    node_result = conn.execute(sqlalchemy.text("select nid, vid, type, title, uid, status, created, changed, comment, promote, sticky from node;"))
    for x in node_result:
        node = {}
        node['nid'] = x.nid
        node['vid'] = x.vid
        node['type'] = x.type
        node['title'] = x.title
        node['uid'] = x.uid
        node['status'] = x.status
        node['created'] = x.created
        node['changed'] = x.changed
        node['comment'] = x.comment
        node['promote'] = x.promote
        node['sticky'] = x.sticky

        if 'node/' + str(x.nid) in urlaliasmap:
            node['path'] = '/' + urlaliasmap['node/' + str(x.nid)]


        node['fields'] = extract_fields(x.type, x.nid, x.vid)
        node['fields2'] = extract_fields2(x.type, x.nid, x.vid)
        #
        # rules = [
        #     {
        #         'elements': ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'tr', 'td', 'th'],
        #         'patterns': [
        #             {'name': 'text-align', 'value': 'center', 'class': 'text-align-center'},
        #             {'name': 'text-align', 'value': 'right', 'class': 'text-align-right'}
        #         ]
        #     },
        #     {
        #         'elements': 'img',
        #         'patterns': [
        #             {'name': 'float', 'value': 'right', 'class': 'right', 'alt-attr': 'data-align'},
        #             {'name': 'float', 'value': 'center', 'class': 'center', 'alt-attr': 'data-align'},
        #             {'name': 'float', 'value': 'left', 'class': 'left', 'alt-attr': 'data-align'}
        #         ]
        #     }
        # ]
        #
        #
        #
        # if 'fields' in node:
        #     if 'body' in node['fields']:
        #         if 'data' in node['fields']['body']:
        #             for data in node['fields']['body']['data']:
        #                 if 'body_value' in data:
        #
        #                     html = data['body_value']
        #                     # print("Initial HTML:")
        #                     # print(html)
        #                     # print("Results:")
        #
        #                     soup = BeautifulSoup(html, features="lxml")
        #
        #                     for rule in rules:
        #                         results = soup.find_all(rule['elements'], style=True)
        #                         for result in results:
        #                             styles = cssutils.parseStyle(result['style'])
        #                             for style in styles:
        #                                 for pattern in rule['patterns']:
        #                                     if style.name == pattern['name'] and style.value == pattern['value']:
        #                                         attr = 'class'
        #                                         if 'alt-attr' in pattern:
        #                                             attr = pattern['alt-attr']
        #
        #                                         if result.get(attr) is None:
        #                                             result[attr] = pattern['class']
        #                                         else:
        #                                             result[attr].append(pattern['class'])
        #                             del result['style']
        #
        #                     data['body_value'] = str(soup)

        # if 'fields' in node:
        #     if 'field_person_title' in node['fields']:
        #         if 'data' in node['fields']['field_person_title']:
        #             for data in node['fields']['field_person_title']['data']:
        #                 if 'field_person_title_value' in data:
        #                     html = data['field_person_title_value']
        #                     soup = BeautifulSoup(html, features="lxml")
        #                     data['field_person_title_value'] = str(soup.get_text())


        #field_person_title_value

        if node['type'] == 'file':
            for f in output['files']['images']:
                for item in node['fields']['field_file_attachment']['data']:
                    if item['field_file_attachment_fid'] == f['fid']:
                        # print(f['fid'])
                        # print(node['path'])
                        f['canonical_path'] = node['path']

        if node['type'] == 'section_page':
            node['page_sections'] = []
            # print('Section page node found')
            for d in node['fields']['field_section_page_sections']['data']:
                # print(d['field_section_page_sections_target_id'])
                bs = {}
                bs['beans'] = []
                bs['bid'] = d['field_section_page_sections_target_id']
                for b in output['beans']['block_section']:
                    if b['bid'] == bs['bid']:
                        #print(b['fields']['field_blocks_section_blocks']['data'])
                        # field_block_section_bg_effect
                        # field_block_section_bg_image
                        if len(b['fields']['field_block_section_bg_effect']['data']) > 0:
                            bs['bg_effect'] = b['fields']['field_block_section_bg_effect']['data'][0]['field_block_section_bg_effect_value']
                        if len(b['fields']['field_block_section_bg_image']['data']) > 0:
                            bs['bg_image'] = b['fields']['field_block_section_bg_image']['data'][0]['field_block_section_bg_image_fid']
                        if len(b['fields']['field_block_section_padding']['data']) > 0:
                            padding = b['fields']['field_block_section_padding']['data'][0]['field_block_section_padding_value'].split()
                            if len(padding) == 1:
                                bs['padding_top'] = padding[0]
                                bs['padding_right'] = padding[0]
                                bs['padding_bottom'] = padding[0]
                                bs['padding_left'] = padding[0]
                            elif len(padding) == 2:
                                bs['padding_top'] = padding[0]
                                bs['padding_right'] = padding[1]
                                bs['padding_bottom'] = padding[0]
                                bs['padding_left'] = padding[1]
                            elif len(padding) == 3:
                                bs['padding_top'] = padding[0]
                                bs['padding_right'] = padding[1]
                                bs['padding_bottom'] = padding[2]
                                bs['padding_left'] = padding[1]
                            elif len(padding) == 4:
                                bs['padding_top'] = padding[0]
                                bs['padding_right'] = padding[1]
                                bs['padding_bottom'] = padding[2]
                                bs['padding_left'] = padding[3]

                        if len(b['fields']['field_hero_unit_bg_color']['data']) > 0:
                            section['bg_color'] = b['fields']['field_hero_unit_bg_color']['data'][0]['field_hero_unit_bg_color_value']

                        if len(b['fields']['field_hero_unit_overlay']['data']) > 0:
                            section['overlay'] = b['fields']['field_hero_unit_overlay']['data'][0]['field_hero_unit_overlay_value']

                        if len(b['fields']['field_hero_unit_text_color']['data']) > 0:
                            section['text_color'] = b['fields']['field_hero_unit_text_color']['data'][0]['field_hero_unit_text_color_value']


                        for c in b['fields']['field_blocks_section_blocks']['data']:
                            #print(c)
                            column = []
                            column.append(f"{c['field_blocks_section_blocks_target_id']} {get_bean_type(c['field_blocks_section_blocks_target_id'])} {get_bean(c['field_blocks_section_blocks_target_id'])['display_title']} 1")
                            bs['beans'].append(column)

                            #bs['beans'].append(f"{c['field_blocks_section_blocks_target_id']} {get_bean_type(c['field_blocks_section_blocks_target_id'])} {bean['display_title']} 1")
                node['page_sections'].append(bs)


                # print(d)
            # for b in output['beans']:




        layout_result = conn.execute(sqlalchemy.text(f"select layout_id, title, node_type from express_layout WHERE layout_id = '{x.nid}';"))

        for y in layout_result:
            layout = {}
            layout['layout_id'] = y.layout_id
            layout['title'] = y.title
            layout['node_type'] = y.node_type

            layout_field_names = []




            layout_field_names.append('field_intro')  # WIDE
            layout_field_names.append('field_slider')  # not WIDE

            layout_field_names.append('TITLE')

            layout_field_names.append('field_post_title_wide') # WIDE
            layout_field_names.append('field_post_title')
            layout_field_names.append('field_header')
            layout_field_names.append('BODY')
            layout_field_names.append('PHOTOGALLERY')
            layout_field_names.append('field_inner_content_left')
            layout_field_names.append('field_inner_content_right')
            layout_field_names.append('field_footer')
            layout_field_names.append('field_content_bottom')
            layout_field_names.append('field_wide_2') # WIDE


            layout_field_names.append('field_sidebar_first')
            layout_field_names.append('field_sidebar_second')


            fields = []

            for lfname in layout_field_names:

                if lfname == 'BODY' or lfname == 'TITLE' or lfname == 'PHOTOGALLERY':
                    continue

                field = {}
                field['name'] = lfname
                field_result = conn.execute(sqlalchemy.text(f"select {lfname}_target_id from field_data_{lfname} WHERE entity_id = '{x.nid}';"))
                bean_list = []
                for r in field_result:
                    bean_list.append(r[0])
                if len(bean_list) > 0:
                    field['beans'] = bean_list
                    fields.append(field)

            layout['fields'] = fields


            page_sections = {}
            for f in fields:
                field_name = f["name"]
                page_sections[field_name] = []
                for s in f['beans']:
                    section = {}

                    section['bid'] = s
                    section['beans'] = []

                    block_section = False

                    if 'block_section' in output['beans']:
                        for b in output['beans']['block_section']:
                            if b['bid'] == section['bid']:
                                # print(b['fields']['field_blocks_section_blocks']['data'])
                                block_section = True

                                if len(b['fields']['field_block_section_bg_effect']['data']) > 0:
                                    section['bg_effect'] = b['fields']['field_block_section_bg_effect']['data'][0]['field_block_section_bg_effect_value']
                                if len(b['fields']['field_block_section_bg_image']['data']) > 0:
                                    section['bg_image'] = b['fields']['field_block_section_bg_image']['data'][0]['field_block_section_bg_image_fid']
                                if len(b['fields']['field_block_section_padding']['data']) > 0:
                                    padding = b['fields']['field_block_section_padding']['data'][0]['field_block_section_padding_value'].split()
                                    if len(padding) == 1:
                                        section['padding_top'] = padding[0]
                                        section['padding_right'] = padding[0]
                                        section['padding_bottom'] = padding[0]
                                        section['padding_left'] = padding[0]
                                    elif len(padding) == 2:
                                        section['padding_top'] = padding[0]
                                        section['padding_right'] = padding[1]
                                        section['padding_bottom'] = padding[0]
                                        section['padding_left'] = padding[1]
                                    elif len(padding) == 3:
                                        section['padding_top'] = padding[0]
                                        section['padding_right'] = padding[1]
                                        section['padding_bottom'] = padding[2]
                                        section['padding_left'] = padding[1]
                                    elif len(padding) == 4:
                                        section['padding_top'] = padding[0]
                                        section['padding_right'] = padding[1]
                                        section['padding_bottom'] = padding[2]
                                        section['padding_left'] = padding[3]

                                if len(b['fields']['field_block_section_content_bg']['data']) > 0:
                                    section['frame_bg'] = b['fields']['field_block_section_content_bg']['data'][0]['field_block_section_content_bg_value']

                                if len(b['fields']['field_hero_unit_bg_color']['data']) > 0:
                                    section['bg_color'] = b['fields']['field_hero_unit_bg_color']['data'][0]['field_hero_unit_bg_color_value']

                                if len(b['fields']['field_hero_unit_overlay']['data']) > 0:
                                    section['overlay'] = b['fields']['field_hero_unit_overlay']['data'][0]['field_hero_unit_overlay_value']

                                if len(b['fields']['field_hero_unit_text_color']['data']) > 0:
                                    section['text_color'] = b['fields']['field_hero_unit_text_color']['data'][0]['field_hero_unit_text_color_value']



                                # block_row = False

                                for c in b['fields']['field_blocks_section_blocks']['data']:
                                    bid = c['field_blocks_section_blocks_target_id']
                                    if get_bean_type(bid) == 'block_row':

                                        columns = []

                                        block_row = True
                                        b = get_bean(bid)

                                        br = {}
                                        br['type'] = 'BLOCKROW'
                                        br['columns'] = []

                                        if 'field_block_row_collection' in b['fields']:
                                            for d in b['fields']['field_block_row_collection']['data']:
                                                column = []
                                                if 'collection' in d:

                                                    for ib in d['collection']:
                                                        inner_bean = ib['field_block_row_block']['field_block_row_block_target_id']
                                                        column.append(f"{inner_bean} {get_bean_type(inner_bean)} {get_bean(inner_bean)['display_title']} 3 ")

                                                # section['beans'].append(column)
                                                br['columns'].append(column)
                                        br['distribution'] = b['fields']['field_block_row_distribution']['data'][0]['field_block_row_distribution_value']
                                        section['beans'].append(br)

                                    else:
                                        #columns.append(f"{c['field_blocks_section_blocks_target_id']} {get_bean_type(c['field_blocks_section_blocks_target_id'])} {get_bean(c['field_blocks_section_blocks_target_id'])['display_title']} 2")
                                        sr = {}
                                        sr['type'] = 'SINGLE'
                                        sr['columns'] = []
                                        sr['columns'].append([f"{c['field_blocks_section_blocks_target_id']} {get_bean_type(c['field_blocks_section_blocks_target_id'])} {get_bean(c['field_blocks_section_blocks_target_id'])['display_title']} 2"])
                                        section['beans'].append(sr)


                                # if block_row == False:
                                #     section['beans'].append(columns)

                    if block_section == False:
                        
                        if get_bean_type(section['bid']) == 'block_row':
                            b = get_bean(section['bid'])
                            #pprint.pprint(b)
                            if 'field_block_row_collection' in b['fields']:
                                for d in b['fields']['field_block_row_collection']['data']:
                                    column = []
                                    if 'collection' in d:
                                        for ib in d['collection']:
                                            inner_bean = ib['field_block_row_block']['field_block_row_block_target_id']
                                            column.append(f"{inner_bean} {get_bean_type(inner_bean)} {get_bean(inner_bean)['display_title']} 3")
                                    section['beans'].append(column)
                            section['distribution'] = b['fields']['field_block_row_distribution']['data'][0]['field_block_row_distribution_value']

                                    #print(d['collection']['field_block_row_block']['field_block_row_block_target_id'])
                        else:
                            #section['beans']['columns'] = []
                            column = []

                            if get_bean(section['bid']) is not None:
                                column.append(f"{section['bid']} {get_bean_type(section['bid'])} {get_bean(section['bid'])['display_title']} 4")
                            else:
                                pass
                            # Check
                            #    column.append(f"{section['bid']} {get_bean_type(section['bid'])} false 5")



                            section['beans'].append(column)

                            #section['beans'].append(f"{section['bid']} {get_bean_type(section['bid'])} {bean['display_title']}")


                    page_sections[field_name].append(section)

            #Ugly block_row fix

            layout['page_sections_test'] = {}

            for ordered_name in layout_field_names:
                if ordered_name in page_sections:
                    new_section_list = []
                    for section in page_sections[ordered_name]:
                        reprocessing_required = False
                        for bean in section['beans']:
                            if 'type' in bean:
                                reprocessing_required = True

                        if reprocessing_required:
                            # print('Reprocessing')
                            new_sections = []
                            current_section = None
                            for bean in section['beans']:
                                if bean['type'] == 'SINGLE':
                                    if current_section == None:
                                        current_section = copy.deepcopy(section)
                                        current_section['beans'] = bean['columns']
                                    else:
                                        current_section['beans'][0].extend(bean['columns'][0])

                                    # new_section = copy.deepcopy(section)
                                    # new_section['beans'] = bean['columns']
                                    # new_sections.append(new_section)
                                elif bean['type'] == 'BLOCKROW':
                                    if current_section is not None:
                                        new_sections.append(current_section)
                                        current_section = None
                                    new_section = copy.deepcopy(section)
                                    new_section['beans'] = bean['columns']
                                    new_section['distribution'] = bean['distribution']
                                    new_sections.append(new_section)
                            if current_section is not None:
                                new_sections.append(current_section)
                                current_section = None


                            new_section_list.extend(new_sections)


                        else:
                            new_section_list.append(section)

                    for idx, x in enumerate(new_section_list):
                        # print(f" enum: {idx} {x}")
                        if x == 0:
                            continue
                        else:
                            if 'bg_image' in new_section_list[idx] and 'bg_image' in new_section_list[idx - 1]:
                                # print(f"{new_section_list[idx]['bg_image']} {new_section_list[idx - 1]['bg_image']}")
                                if new_section_list[idx]['bg_image'] == new_section_list[idx - 1]['bg_image']:
                                    new_section_list[idx - 1]['bg_effect'] = 'scroll'
                                    new_section_list[idx]['bg_effect'] = 'scroll'
                    # page_sections[ordered_name] = new_section_list
                    # print(new_section_list)
                    layout['page_sections_test'][ordered_name] = new_section_list
                    page_sections[ordered_name] = new_section_list



            # print("PAGE SECTIONS")
            # pprint.pp(page_sections)
            # print("PAGE SECTIONS TEST")
            # pprint.pp(layout['page_sections_test'])




            combined_page_sections = []
            for ordered_name in layout_field_names:
                if ordered_name in page_sections:
                    if ordered_name == 'field_intro' or ordered_name == 'field_post_title_wide' or ordered_name == 'field_wide_2':
                        for section in page_sections[ordered_name]:
                            section['container_width'] = 'edge-to-edge'

                    if ordered_name != 'field_sidebar_first' and ordered_name != 'field_sidebar_second':
                        combined_page_sections.extend(page_sections[ordered_name])
                if ordered_name == 'BODY':
                    body_element = {}
                    body_element['bid'] = 0
                    body_element['beans'] = []
                    column = []
                    column.append('0 body false')


                    if 'field_sidebar_first' in page_sections:
                        field_sidebar_first_column = []
                        for b in page_sections['field_sidebar_first']:
                            if len(b['beans']) > 0:
                                if b['beans'][0]:
                                    field_sidebar_first_column.append(b['beans'][0][0])


                        body_element['beans'].append(field_sidebar_first_column)

                    body_element['beans'].append(column)


                        
                    menu_column = []
                    menu_column.append('0 menu_main false')
                    menu_column.append('0 menu_secondary false')
                    menu_column.append('0 menu_footer false')


                    if 'field_sidebar_second' in page_sections:
                        # field_sidebar_second_column = []
                        for b in page_sections['field_sidebar_second']:
                            if len(b['beans']) > 0:
                                if b['beans'][0]:
                                    menu_column.append(b['beans'][0][0])
                        # body_element['beans'].append(field_sidebar_second_column)

                    body_element['beans'].append(menu_column)

                    # print('BODY:')
                    # print(body_element)

                    if(len(body_element['beans']) == 3):
                        body_element['distribution'] = 'center'

                    if(len(body_element['beans']) == 2):
                        body_element['distribution'] = 'left'


                    combined_page_sections.append(body_element)

                if ordered_name == 'TITLE':
                    title_element = {}
                    title_element['bid'] = 0
                    title_element['beans'] = []
                    column = []
                    column.append('0 title false')
                    title_element['beans'].append(column)

                    #title_element['beans'].append('0 title false')
                    combined_page_sections.append(title_element)
                if ordered_name == 'PHOTOGALLERY' and node['type'] == 'photo_gallery':
                    pg_element = {}
                    pg_element['bid'] = node['nid']
                    pg_element['beans'] = []
                    column = []
                    column.append(f'{node["nid"]} photogallery false')
                    pg_element['beans'].append(column)

                    #title_element['beans'].append('0 title false')
                    combined_page_sections.append(pg_element)


            for s in combined_page_sections:
                # print(f"Node: {node['nid']}, Columns: {len(section['beans'])}")
                if len(s['beans']) > 4:
                    # pprint.pp(f"Node: {node['nid']}, {s['beans']}")

                    original_beans = copy.deepcopy(s['beans'])
                    new_beans = []
                    new_column = []
                    for idx, x in enumerate(original_beans):
                        if idx % 3 == 0:
                            if len(new_column) > 0:
                                new_beans.append(new_column)
                            new_column = []
                        new_column.append(x[0])


                    if len(new_column) > 0:
                        new_beans.append(new_column)

                    s['beans'] = new_beans



            layout['page_sections'] = combined_page_sections



            node['layout'] = layout

        if node['type'] not in node_types:
            node_types[node['type']] = []
        node_types[node['type']].append(node)

        #nodes.append(node)
    nodes.append(node_types)
    output['nodes'] = nodes


    # Menus
    menumap = {}
    menumap['main-menu'] = 'main'
    menumap['menu-footer-menu'] = 'footer'
    menumap['menu-secondary-menu'] = 'secondary'

    menusignore = []
    menusignore.append('management')
    menusignore.append('navigation')
    menusignore.append('user-menu')


    menus = []
    menu_result = conn.execute(sqlalchemy.text("select menu_name, title, description from menu_custom;"))
    for x in menu_result:
        menu = {}

        if x.menu_name in menusignore:
            continue


        menu['name'] = x.menu_name
        menu['title'] = x.title
        menu['desciption'] = x.description
        menu['links'] = []

        menulink_result = conn.execute(sqlalchemy.text(f"select menu_name, mlid, plid, link_path, router_path, link_title, options, hidden, external, has_children, expanded, weight, depth, customized, p1, p2, p3, p4, p5, p6, p7, p8, p9, updated from menu_links WHERE menu_name = '{x.menu_name}';"))
        for y in menulink_result:
            menulink = {}

            if y.menu_name in menumap:
                menulink['menu_name'] = menumap[y.menu_name]
            else:
                menulink['menu_name'] = y.menu_name

            menulink['mlid'] = y.mlid
            menulink['plid'] = y.plid

            status = 0

            # if y.link_path != '<front>':
            #     node_result = conn.execute(sqlalchemy.text(f"select nid, status from node where nid = '{y.link_path[5:]}';"))
            #     for z in node_result:
            #         #print(f"nid:{z.nid} status:{z.status}")
            #         status = z.status
            # if status == 0:
            #     continue

            if y.link_path[0:4] == 'node/':
                node_result = conn.execute(sqlalchemy.text(f"select nid, status from node where nid = '{y.link_path[5:]}';"))
                for z in node_result:
                    #print(f"nid:{z.nid} status:{z.status}")
                    status = z.status
            elif y.link_path == '<firstchild>':
                status = 1
            elif y.link_path == '<front>':
                continue
            else:
                status = 1


            if y.link_path == '<firstchild>':
                menulink['link_path'] = '<none>'
            elif y.link_path in urlaliasmap:
                menulink['link_path'] = urlaliasmap[y.link_path]
            else:
                menulink['link_path'] = y.link_path


            menulink['router_path'] = y.router_path
            menulink['link_title'] = y.link_title
            menulink['options'] = y.options
            if y.hidden:
                menulink['enabled'] = 0
            else:
                menulink['enabled'] = 1
            menulink['external'] = y.external
            menulink['has_children'] = y.has_children
            menulink['expanded'] = y.expanded
            menulink['weight'] = y.weight
            menulink['depth'] = y.depth
            menulink['customized'] = y.customized
            menulink['p1'] = y.p1
            menulink['p2'] = y.p2
            menulink['p3'] = y.p3
            menulink['p4'] = y.p4
            menulink['p5'] = y.p5
            menulink['p6'] = y.p6
            menulink['p7'] = y.p7
            menulink['p8'] = y.p8
            menulink['p9'] = y.p9
            menulink['updated'] = y.updated

            if y.link_path == '<firstchild>':
                menulink['link_path'] = '<none>'
                menulink['options'] = 'a:1:{s:15:"menu_firstchild";a:1:{s:7:"enabled";i:1;}}'
            elif y.link_path in urlaliasmap:
                menulink['link_path'] = urlaliasmap[y.link_path]
            else:
                menulink['link_path'] = y.link_path




            menu['links'].append(menulink)


        menus.append(menu)
    output['menus'] = menus

    # Redirects

    internalredirects = []
    externalredirects = []
    redirects_result = conn.execute(sqlalchemy.text("select rid, source, redirect, status from redirect;"))
    for x in redirects_result:
        if x.status == 0:
            continue
        redirect = {}

        # redirectfilter = re.compile('node/\d*')


        redirect['rid'] = x.rid
        redirect['source'] = x.source
        redirect['redirect'] = x.redirect

        if redirect['source'][0:5] == 'node/':
            if redirect['source'] in urlaliasmap:
                redirect['source'] = urlaliasmap[redirect['source']]

        if redirect['redirect'][0:5] == 'node/':
            if redirect['redirect'] in urlaliasmap:
                redirect['redirect'] = urlaliasmap[redirect['redirect']]


        if x.redirect[0:4] != 'http':
            redirect['redirect'] = 'internal:/' + redirect['redirect']
            internalredirects.append(redirect)
        else:
            externalredirects.append(redirect)

    output['internalredirects'] = internalredirects
    output['externalredirects'] = externalredirects

    # Vocabularies

    vocabularies = {}

    vocabularies_mapping = [
        {'src': 'byline', 'dst': 'byline'},
        {'src': 'department', 'dst': 'department'},
        {'src': 'newsletter', 'dst': 'newsletter'},
        {'src': 'person_type', 'dst': 'ucb_person_job_type'},
        {'src': 'tags', 'dst': 'tags'},
        {'src': 'people_filter_1', 'dst': 'filter_1'},
        {'src': 'people_filter_2', 'dst': 'filter_2'},
        {'src': 'people_filter_3', 'dst': 'filter_3'},
        {'src': 'category', 'dst': 'category'},
        {'src': 'collection_categories', 'dst': ''},
        {'src': 'collection_type', 'dst': ''},
    ]

    for vocab in vocabularies_mapping:
        vocabulary_result = conn.execute(sqlalchemy.text(f"select vid from taxonomy_vocabulary where machine_name='{vocab['src']}';"))
        terms = []
        for vid in vocabulary_result:
            term_result = conn.execute(sqlalchemy.text(f"select tid, name, description, format, weight from taxonomy_term_data WHERE vid = '{vid.vid}';"))
            for t in term_result:

# footer
# path
# design
# name_image
# social_links

                parent = 0
                parent_result = conn.execute(sqlalchemy.text(f"select parent from taxonomy_term_hierarchy WHERE tid = '{t.tid}';"));
                for p in parent_result:
                    parent = p.parent

                term = {'tid': t.tid, 'parent': parent, 'name': t.name, 'description': t.description, 'format': t.format, 'weight': t.weight}

                if vocab['src'] == 'newsletter':
                    fields = {}
                    field_result = conn.execute(sqlalchemy.text(f"select field_newsletter_footer_value, field_newsletter_footer_format from field_data_field_newsletter_footer WHERE entity_id = '{t.tid}';"))
                    for f in field_result:
                        fields['field_newsletter_footer'] = {}
                        fields['field_newsletter_footer']['value'] = f.field_newsletter_footer_value
                        fields['field_newsletter_footer']['format'] = f.field_newsletter_footer_format

                    field_result = conn.execute(sqlalchemy.text(f"select field_newsletter_path_value from field_data_field_newsletter_path WHERE entity_id = '{t.tid}';"))
                    for f in field_result:
                        fields['field_newsletter_path'] = {}
                        fields['field_newsletter_path']['value'] = f.field_newsletter_path_value

                    field_result = conn.execute(sqlalchemy.text(f"select field_newsletter_design_value from field_data_field_newsletter_design WHERE entity_id = '{t.tid}';"))
                    for f in field_result:
                        fields['field_newsletter_design'] = {}
                        fields['field_newsletter_design']['value'] = f.field_newsletter_design_value

                    field_result = conn.execute(sqlalchemy.text(f"select field_newsletter_name_image_fid from field_data_field_newsletter_name_image WHERE entity_id = '{t.tid}';"))
                    for f in field_result:
                        fields['field_newsletter_name_image'] = {}
                        fields['field_newsletter_name_image']['fid'] = f.field_newsletter_name_image_fid

                    field_result = conn.execute(sqlalchemy.text(f"select field_newsletter_social_links_target_id from field_data_field_newsletter_social_links WHERE entity_id = '{t.tid}';"))
                    for f in field_result:
                        fields['field_newsletter_social_links'] = {}
                        fields['field_newsletter_social_links']['target_id'] = f.field_newsletter_social_links_target_id
                    term['fields'] = fields
                    

                terms.append(term)
        vocabularies[vocab['src']] = terms

    #
    # vocabularies_result = conn.execute(sqlalchemy.text(f"select vid, name, machine_name, description, hierarchy, module, weight from taxonomy_vocabulary;"))
    # for x in vocabularies_result:
    #     vocabulary = {}
    #
    #     vocabulary['vid'] = x.vid
    #     vocabulary['name'] = x.name
    #     vocabulary['machine_name'] = x.machine_name
    #     vocabulary['description'] = x.description
    #     vocabulary['hierarchy'] = x.hierarchy
    #     vocabulary['module'] = x.module
    #     vocabulary['weight'] = x.weight
    #
    #     terms = []
    #
    #     term_result = conn.execute(sqlalchemy.text(f"select tid, vid, name, description, format, weight from taxonomy_term_data WHERE vid = '{x.vid}';"))
    #     for y in term_result:
    #         term = {}
    #
    #         term['tid'] = y.tid
    #         term['vid'] = y.vid
    #         term['name'] = y.name
    #         term['description'] = y.description
    #         term['format'] = y.format
    #         term['weight'] = y.weight
    #
    #         terms.append(term)
    #
    #     vocabulary['terms'] = terms
    #
    #     vocabularies.append(vocabulary)

    output['vocabularies'] = vocabularies

    contexts = []
    context_result = conn.execute(sqlalchemy.text(f"select name, description, tag, conditions, reactions, condition_mode from context;"))
    for c in context_result:
        context = {}
        context['name'] = c.name
        context['description'] = c.description
        context['tag'] = c.tag
        context['conditions'] = c.conditions
        context['reactions'] = c.reactions
        context['condition_mode'] = c.condition_mode
        contexts.append(context)

    output['context'] = contexts

    def valid_xml_char_ordinal(c):
        codepoint = ord(c)
        # conditions ordered by presumed frequency
        return (
                0x20 <= codepoint <= 0xD7FF or
                codepoint in (0x9, 0xA, 0xD) or
                0xE000 <= codepoint <= 0xFFFD or
                0x10000 <= codepoint <= 0x10FFFF
        )

    def process_striptags(value):
        html = value
        soup = BeautifulSoup(html, features="lxml")
        return str(soup.get_text())

    def process_links(value):
        # if value == '':
        #     c1['field_callout_title'].pop('field_callout_title_url')
        if value[0:5] == 'node/':
            return 'internal:/' + value
        elif value[0:1] == '/':
            return 'internal:' + value
        elif value[0:7] == 'mailto:':
            return value
        elif value[0:4] == 'tel:':
            return value
        elif len(value) == 0:
            return value
        elif ':' not in value and '.' not in value:
            return 'internal:/' + value
        else:
            return value

    def process_styles(value):

        rules = [
            {
                'elements': ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'tr', 'td', 'th'],
                'patterns': [
                    {'name': 'text-align', 'value': 'center', 'class': 'text-align-center'},
                    {'name': 'text-align', 'value': 'right', 'class': 'text-align-right'}
                ]
            },
            {
                'elements': 'img',
                'patterns': [
                    {'name': 'float', 'value': 'right', 'class': 'right', 'alt-attr': 'data-align'},
                    {'name': 'float', 'value': 'center', 'class': 'center', 'alt-attr': 'data-align'},
                    {'name': 'float', 'value': 'left', 'class': 'left', 'alt-attr': 'data-align'}
                ]
            }
        ]

        html = value
        # print("Initial HTML:")
        # print(html)


        soup = BeautifulSoup(html, features="html.parser")

        for rule in rules:
            results = soup.find_all(rule['elements'], style=True)
            for result in results:
                styles = cssutils.parseStyle(result['style'])
                for style in styles:
                    for pattern in rule['patterns']:
                        if style.name == pattern['name'] and style.value == pattern['value']:
                            attr = 'class'
                            if 'alt-attr' in pattern:
                                attr = pattern['alt-attr']

                            if result.get(attr) is None:
                                result[attr] = pattern['class']
                            else:
                                result[attr].append(pattern['class'])
                del result['style']

        # print("Results:")
        # print(str(soup))

        return str(soup)

    styles_processing_tags = [
        'body_value',
        'field_block_text_value',
        'field_callout_text_value',
        'field_collection_body_value',
        'field_collection_preview_value',
        'field_cont_seq_body_value',
        'field_cont_seq_description_value',
        'field_expandable_text_value',
        'field_hero_unit_text_value',
        'field_newsletter_block_body_value',
        'field_newsletter_footer_value',
        'field_nl_section_content_body_value',
        'field_person_address_value',
        'field_person_office_hours_value',
        'field_qa_answer_value',
        'field_slider_teaser_value',
        'field_social_links_body_value',
        'field_video_reveal_text_value'
    ]

    links_processing_tags = [
        'field_article_byline_url_url',
        'field_article_external_url_url',
        'field_article_grid_more_link_url',
        'field_article_link_url',
        'field_callout_title_url',
        'field_category_term_page_link_url',
        'field_cont_seq_title_url',
        'field_fb_url_url',
        'field_hero_unit_link_url',
        'field_localist_link_url',
        'field_newsletter_ad_link_url',
        'field_newsletter_more_link_url',
        'field_nl_section_content_title_url',
        'field_person_website_url',
        'field_slider_link_url',
        'field_social_link_url_url',
        'field_social_links_homepage_url_url',
        'field_tag_term_page_link_url'
    ]

    striptags_processing_tags = [
        'field_person_title_value'
    ]

    image_fields = [
        'field_article_thumbnail',
        'field_block_photo',
        'field_block_section_bg_image',
        'field_block_section_bg_image_m',
        'field_block_section_bg_image_t',
        'field_callout_image',
        'field_collection_category_bg',
        'field_collection_image',
        'field_collection_thumbnail',
        'field_cont_seq_photos',
        'field_feature_title_image',
        'field_hero_unit_image',
        'field_image',
        'field_issue_image',
        'field_issue_image_insert',
        'field_newsletter_ad_image',
        'field_newsletter_intro_image',
        'field_newsletter_name_image',
        'field_nl_section_content_image'
        'field_person_photo',
        'field_photo',
        'field_slider_image',
        'field_video_reveal_image'
    ]

    image_info_uri = {}
    image_info_fid = {}



    def recurse_xml(root, output):
        if isinstance(output, dict):
            for key in output:

                if key in image_fields:
                    # pprint.pp(key)
                    # pprint.pp(output[key])

                    if key + '_alt' in output[key]:
                        # print(f"ALT FOUND: {output[key][key + '_fid']} {output[key][key + '_alt']}")
                        fid = output[key][key + '_fid']
                        if fid not in image_info_fid:
                            image_info_fid[fid] = []
                        image_info_fid[fid].append(output[key][key + '_alt'])


                    if 'data' in output[key]:
                        for d in output[key]['data']:
                            # print(f"ALT FOUND: {d[key + '_fid']} {d[key + '_alt']}")
                            fid = d[key + '_fid']
                            if fid not in image_info_fid:
                                image_info_fid[fid] = []
                            image_info_fid[fid].append(d[key + '_alt'])

                element = etree.SubElement(root, key)
                recurse_xml(element, output[key])
        if isinstance(output, list):
            for item in output:
                element = etree.SubElement(root, 'item')
                recurse_xml(element, item)
        if isinstance(output, int):
            root.text = str(output)
        if isinstance(output, str):
            cleaned_string = ''.join(c for c in output if valid_xml_char_ordinal(c))
            root.text = cleaned_string



            if root.tag in styles_processing_tags:

                soup = BeautifulSoup(root.text, features="html.parser")
                results = soup.find_all('img', style=True)
                for result in results:
                    # print('img found')
                    # print(result.get('alt'))
                    # print(result.get('src'))

                    src = result.get('src')
                    alt = result.get('alt')

                    if not src.startswith('sites/default/files/'):
                        continue

                    src = src.split('?')[0]
                    src = src[20:]
                    srclist = src.split('/')
                    if srclist[0] == 'styles':
                        srclist.pop(0)
                        srclist.pop(0)
                        srclist.pop(0)

                    src = "public://" + "/".join(srclist)


                    if src not in image_info_uri:
                        image_info_uri[src] = []
                    image_info_uri[src].append(alt)


                root.text = process_styles(root.text)



            if root.tag in links_processing_tags:
                if len(root.text) == 0:
                    root.tag = 'nulltag'
                    return

                root.text = process_links(root.text)

            if root.tag in striptags_processing_tags:
                root.text = process_striptags(root.text)

            # pprint.pp(root.tag)







    #print(output)

    dummyroot = etree.Element('root')
    recurse_xml(dummyroot, output)

    # pprint.pp(image_info_uri)
    # pprint.pp(image_info_fid)

    for f in output['files']['images']:
        longest_alt = ""
        if f['uri'] in image_info_uri:
            # print('URI found')
            for i in image_info_uri[f['uri']]:
                if len(i) > len(longest_alt):
                    longest_alt = i
        if f['fid'] in image_info_fid:
            # print('FID found')
            for i in image_info_fid[f['fid']]:
                if len(i) > len(longest_alt):
                    longest_alt = i
        # pprint.pp(longest_alt)
        f['alt'] = longest_alt

    root = etree.Element('root')

    recurse_xml(root, output)



    print(etree.tostring(root, pretty_print=True).decode())



    # xml = dicttoxml.dicttoxml(output, attr_type=False, encoding="UTF-8")
    #
    # print(xml)
    #
    # parser = etree.XMLParser(ns_clean=True, recover=True)
    # tree = etree.parse(BytesIO(xml), parser)
    # root = tree.getroot()

    #
    # print(etree.tostring(root, pretty_print=True).decode())


