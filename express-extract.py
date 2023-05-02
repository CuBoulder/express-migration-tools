import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv
import dicttoxml
import time
import re

from lxml import etree
from io import StringIO, BytesIO

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


engine = sqlalchemy.create_engine("mariadb+pymysql://root:pass@localhost/strategicrelations?charset=utf8mb4", echo=False)

with engine.connect() as conn:

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
    filemap['images'] = ['image/jpeg', 'image/png']
    filemap['documents'] = ['application/pdf']
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

        file['filepath'] = '/home/tirazel/Projects/migration-tools/ucb-strategicrelations/files/' + x.uri[9:]

        if x.filemime in filemap['images']:
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
        skiplist.append('alco6164')
        skiplist.append('mibo7729')
        skiplist.append('jesp3304')
        skiplist.append('fraziere')
        skiplist.append('jesp3304')
        skiplist.append('wetu1300')
        skiplist.append('linebarg')
        skiplist.append('brokaw')
        skiplist.append('crafts')
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


        for y in roles_result:

            roles.extend(rolemap[y[0]])

        user['roles'] = roles
        users.append(user)
    output['users'] = users

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

        node['path'] = '/' + urlaliasmap['node/' + str(x.nid)]


        node['fields'] = extract_fields(x.type, x.nid, x.vid)


        layout_result = conn.execute(sqlalchemy.text(f"select layout_id, title, node_type from express_layout WHERE layout_id = '{x.nid}';"))

        for y in layout_result:
            layout = {}
            layout['layout_id'] = y.layout_id
            layout['title']  = y.title
            layout['node_type'] = y.node_type

            layout_field_names = []

            layout_field_names.append('field_footer')
            layout_field_names.append('field_header')
            layout_field_names.append('field_inner_content_left')
            layout_field_names.append('field_inner_content_right')
            layout_field_names.append('field_intro')
            layout_field_names.append('field_sidebar_first')
            layout_field_names.append('field_sidebar_second')
            layout_field_names.append('field_slider')
            layout_field_names.append('field_wide_2')
            layout_field_names.append('field_content_bottom')
            layout_field_names.append('field_post_title')
            layout_field_names.append('field_post_title_wide')

            fields = []

            for lfname in layout_field_names:
                field = {}
                field['name'] = lfname
                field_result = conn.execute(sqlalchemy.text(f"select {lfname}_target_id from field_data_{lfname} WHERE entity_id = '{x.nid}';"))
                for r in field_result:
                    field['target_id'] = r[0]

                    beans = []

                    bean_result = conn.execute(sqlalchemy.text(f"select bid, vid, delta, label, title, type, view_mode, data, uid from bean WHERE bid = '{r[0]}';"))
                    for b in bean_result:

                        bean = {}
                        bean['bid'] = b.bid
                        bean['vid'] = b.vid
                        bean['delta'] = b.delta
                        bean['label'] = b.label
                        bean['title'] = b.title
                        bean['type'] = b.type
                        bean['view_mode'] = b.view_mode
                        bean['data'] = b.data
                        bean['uid'] = b.uid

                        bean_fields = []

                        bean['fields'] = extract_fields(b.type, b.bid, b.vid)

                        beans.append(bean)

                    field['layout_beans'] = beans
                if 'beans' in field:
                    fields.append(field)

            layout['fields'] = fields

            node['layout'] = layout

        if node['type'] not in node_types:
            node_types[node['type']] = []
        node_types[node['type']].append(node)

        #nodes.append(node)
    nodes.append(node_types)
    output['nodes'] = nodes

    # Beans

    bean_types = {}
    #
    # bean_articles_fields = []
    # bean_articles_fields.append('field_article_display')
    # bean_articles_fields.append('field_article_exclude_category')
    # bean_articles_fields.append('field_article_exclude_tag')
    # bean_articles_fields.append('field_article_items_display')
    # bean_articles_fields.append('field_article_link')
    # bean_articles_fields.append('field_article_list_category')
    # bean_articles_fields.append('field_article_pager')
    # bean_articles_fields.append('field_article_term')
    # bean_types['articles'] = bean_articles_fields
    #
    # bean_article_grid_fields = []
    # bean_article_grid_fields.append('field_article_exclude_category')
    # bean_article_grid_fields.append('field_article_exclude_tag')
    # bean_article_grid_fields.append('field_article_grid_category')
    # bean_article_grid_fields.append('field_article_grid_filter')
    # bean_article_grid_fields.append('field_article_grid_items')
    # bean_article_grid_fields.append('field_article_grid_more_link')
    # bean_article_grid_fields.append('field_article_grid_summary')
    # bean_types['article_grid'] = bean_article_grid_fields
    #
    # bean_block_fields = []
    # bean_block_fields.append('field_block_photo')
    # bean_block_fields.append('field_block_text')
    # bean_types['block'] = bean_block_fields
    #
    # bean_block_row_fields = []
    # bean_block_row_fields.append('field_block_row_block')
    # bean_block_row_fields.append('field_block_row_collection')
    # bean_block_row_fields.append('field_block_row_distribution')
    # bean_block_row_fields.append('field_block_row_match_height')
    # bean_types['block_row'] = bean_block_row_fields



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
    #field_hero_unit_bg_color?
    #field_hero_unit_overlay?
    #field_hero_unit_text_color?
    bean_types['block_section'] = bean_block_section_fields

    # bean_block_wrapper_fields = []
    # bean_block_fields.append('field_block_wrapper_reference')
    # bean_types['block_wrapper'] = bean_block_wrapper_fields
    #
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
    #
    # bean_content_sequence_fields = []
    # bean_content_sequence_fields.append('field_cont_seq_body')
    # bean_content_sequence_fields.append('field_cont_seq_content')
    # bean_content_sequence_fields.append('field_cont_seq_date')
    # bean_content_sequence_fields.append('field_cont_seq_description')
    # bean_content_sequence_fields.append('field_cont_seq_display')
    # bean_content_sequence_fields.append('field_cont_seq_display_date')
    # bean_content_sequence_fields.append('field_cont_seq_display_end_date')
    # bean_content_sequence_fields.append('field_cont_seq_end_date')
    # bean_content_sequence_fields.append('field_cont_seq_group')
    # bean_content_sequence_fields.append('field_cont_seq_photos')
    # bean_content_sequence_fields.append('field_cont_seq_scale')
    # bean_content_sequence_fields.append('field_cont_seq_title')
    # bean_content_sequence_fields.append('field_cont_seq_video')
    # bean_content_sequence_fields.append('field_cont_sequence_title')
    # bean_types['content_sequence'] = bean_content_sequence_fields


    # bean_feature_callout_fields = []
    # bean_feature_callout_fields.append({'name': 'field_callout_columns', 'type': 'bean', 'bundle': 'feature_callout'})
    # bean_feature_callout_fields.append({'name': 'field_callouts', 'type': 'bean', 'bundle': 'feature_callout'})
    # bean_feature_callout_fields.append({'name': 'field_callout_image_size', 'type': 'bean', 'bundle': 'feature_callout'})
    # bean_feature_callout_fields.append({'name': 'field_callout_style', 'type': 'bean', 'bundle': 'feature_callout'})
    # bean_feature_callout_fields.append({'name': 'field_callout_text', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    # bean_feature_callout_fields.append({'name': 'field_callout_image', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    # bean_feature_callout_fields.append({'name': 'field_callout_title', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    # bean_types['feature_callout'] = bean_feature_callout_fields

    bean_feature_callout_fields = []
    bean_feature_callout_fields.append({'name': 'field_callout_columns', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_image_size', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_style', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callouts', 'type': 'bean', 'bundle': 'feature_callout'})
    bean_feature_callout_fields.append({'name': 'field_callout_image', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_feature_callout_fields.append({'name': 'field_callout_text', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_feature_callout_fields.append({'name': 'field_callout_title', 'type': 'field_collection_item', 'bundle': 'field_callouts'})
    bean_types['feature_callout'] = bean_feature_callout_fields



    # bean_hero_unit_fields = []
    # bean_hero_unit_fields.append('field_hero_unit_bg_color')
    # bean_hero_unit_fields.append('field_hero_unit_headline')
    # bean_hero_unit_fields.append('field_hero_unit_image')
    # bean_hero_unit_fields.append('field_hero_unit_link')
    # bean_hero_unit_fields.append('field_hero_unit_link_color')
    # bean_hero_unit_fields.append('field_hero_unit_overlay')
    # bean_hero_unit_fields.append('field_hero_unit_size')
    # bean_hero_unit_fields.append('field_hero_unit_size_priority')
    # bean_hero_unit_fields.append('field_hero_unit_text')
    # bean_hero_unit_fields.append('field_hero_unit_text_align')
    # bean_hero_unit_fields.append('field_hero_unit_text_color')
    # bean_types['hero_unit'] = bean_hero_unit_fields
    #
    # bean_localist_events_fields = []
    # bean_localist_events_fields.append('field_localist_all_instances')
    # bean_localist_events_fields.append('field_localist_content_match')
    # bean_localist_events_fields.append('field_localist_days_ahead')
    # bean_localist_events_fields.append('field_localist_filters')
    # bean_localist_events_fields.append('field_localist_filters_excluded')
    # bean_localist_events_fields.append('field_localist_groups')
    # bean_localist_events_fields.append('field_localist_hide_descriptions')
    # bean_localist_events_fields.append('field_localist_hide_images')
    # bean_localist_events_fields.append('field_localist_hide_past_events')
    # bean_localist_events_fields.append('field_localist_hide_times')
    # bean_localist_events_fields.append('field_localist_link')
    # bean_localist_events_fields.append('field_localist_minical_layout')
    # bean_localist_events_fields.append('field_localist_new_window')
    # bean_localist_events_fields.append('field_localist_places')
    # bean_localist_events_fields.append('field_localist_render_html')
    # bean_localist_events_fields.append('field_localist_results')
    # bean_localist_events_fields.append('field_localist_show_featured')
    # bean_localist_events_fields.append('field_localist_show_sponsored')
    # bean_localist_events_fields.append('field_localist_skip_recurring')
    # bean_localist_events_fields.append('field_localist_start_date')
    # bean_localist_events_fields.append('field_localist_style')
    # bean_localist_events_fields.append('field_localist_tags')
    # bean_localist_events_fields.append('field_localist_truncate_desc')
    # bean_localist_events_fields.append('field_localist_widget_type')
    # bean_types['localist_events'] = bean_localist_events_fields
    #
    # bean_people_list_block_fields = []
    # bean_people_list_block_fields.append('field_people_block_thumbnail')
    # bean_people_list_block_fields.append('field_people_childterms')
    # bean_people_list_block_fields.append('field_people_dept_filter_show')
    # bean_people_list_block_fields.append('field_people_filter1_show')
    # bean_people_list_block_fields.append('field_people_filter2_show')
    # bean_people_list_block_fields.append('field_people_filter3_show')
    # bean_people_list_block_fields.append('field_people_filter_1')
    # bean_people_list_block_fields.append('field_people_filter_2')
    # bean_people_list_block_fields.append('field_people_filter_3')
    # bean_people_list_block_fields.append('field_people_group_by')
    # bean_people_list_block_fields.append('field_people_list_department')
    # bean_people_list_block_fields.append('field_people_list_display')
    # bean_people_list_block_fields.append('field_people_list_person_type')
    # bean_people_list_block_fields.append('field_people_order_by')
    # bean_people_list_block_fields.append('field_people_pos_filter_show')
    # bean_people_list_block_fields.append('field_person_address')
    # bean_people_list_block_fields.append('field_person_department')
    # bean_people_list_block_fields.append('field_person_email')
    # bean_people_list_block_fields.append('field_person_filter_1')
    # bean_people_list_block_fields.append('field_person_filter_2')
    # bean_people_list_block_fields.append('field_person_filter_3')
    # bean_people_list_block_fields.append('field_person_first_name')
    # bean_people_list_block_fields.append('field_person_job_type')
    # bean_people_list_block_fields.append('field_person_last_name')
    # bean_people_list_block_fields.append('field_person_office_hours')
    # bean_people_list_block_fields.append('field_person_phone')
    # bean_people_list_block_fields.append('field_person_photo')
    # bean_people_list_block_fields.append('field_person_title')
    # bean_people_list_block_fields.append('field_person_website')
    # bean_types['people_list_block'] = bean_people_list_block_fields
    #
    #
    # bean_slider_fields = []
    # bean_slider_fields.append('field_slider_caption')
    # bean_slider_fields.append('field_slider_design_style')
    # bean_slider_fields.append('field_slider_image')
    # bean_slider_fields.append('field_slider_link')
    # bean_slider_fields.append('field_slider_size')
    # bean_slider_fields.append('field_slider_slide')
    # bean_slider_fields.append('field_slider_teaser')
    # bean_types['slider'] = bean_slider_fields
    #
    # bean_video_hero_unit_fields = []
    # bean_video_hero_unit_fields.append('field_hero_video_overlay')
    # bean_video_hero_unit_fields.append('field_hero_video_size')
    # bean_video_hero_unit_fields.append('field_video_hero_url')
    # bean_types['video_hero_unit'] = bean_video_hero_unit_fields

    beans = []
    bean_result = conn.execute(sqlalchemy.text("select bid, vid, delta, label, title, type, view_mode, data, uid, created, changed from bean;"))
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

                    data = []

                    fd_result = conn.execute(sqlalchemy.text(
                        f"select {', '.join(columns)} from field_data_{fname['name']} where bundle = '{bean['type']}' AND entity_id = '{bean['bid']}' AND revision_id = '{bean['vid']}';"))

                    for fd_item in fd_result.mappings():
                        field_item = {}
                        field_item['collection'] = []
                        for colname in columns:
                            field_item[colname] = fd_item[colname]

                        if 'entity_id' in field_item and 'delta' in field_item:
                            field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"


                        fci_item_fields = []

                        for fci_item in field_names:
                            fci_data = []
                            if fci_item['bundle'] == fname['name']:
                                print(f"FCI ITEM: {fci_item['name']}")

                                fci_columns = extract_subfields(fci_item['name'])
                                print(fci_columns)



                                fci_id_column = fname['name'] + '_value'
                                print(f"FCI ID COLUMN: {fci_id_column}")
                                fci_revision_column = fname['name'] + '_revision_id'
                                print(f"FCI REVISION COLUMN: {fci_revision_column}")

                                fci_query = f"select {', '.join(fci_columns)} from field_data_{fci_item['name']} where entity_type = '{fci_item['type']}' AND bundle = '{fci_item['bundle']}' AND entity_id = '{field_item[fci_id_column]}' AND revision_id = '{field_item[fci_revision_column]}';"

                                print(fci_query)

                                fci_result = conn.execute(sqlalchemy.text(fci_query))
                                for fcif in fci_result.mappings():
                                    fcif_item = {}
                                    for fcif_colname in fci_columns:
                                        fcif_item[fcif_colname] = fcif[fcif_colname]

                                    fci_data.append(fcif_item)
                                    #field_item['collection'].append(fcif_item)

                            if len(fci_data) != 0:
                                field_item['collection'].append(fci_data)

                        if len(field_item['collection']) == 0:
                            del field_item['collection']


                        data.append(field_item)

                    field['data'] = data
                    fields[field['field_name']] = field

            bean['fields'] = fields

        beans.append(bean)

    output['beans'] = beans



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

            if y.link_path != '<front>':
                node_result = conn.execute(sqlalchemy.text(f"select nid, status from node where nid = '{y.link_path[5:]}';"))
                for z in node_result:
                    #print(f"nid:{z.nid} status:{z.status}")
                    status = z.status
            if status == 0:
                continue

            if y.link_path in urlaliasmap:
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
            redirect['source'] = urlaliasmap[redirect['source']]

        if redirect['redirect'][0:5] == 'node/':
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
        {'src': 'job_type', 'dst': 'ucb_person_job_type'},
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
                terms.append({'tid': t.tid, 'name': t.name, 'description': t.description, 'format': t.format, 'weight': t.weight})
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

    def valid_xml_char_ordinal(c):
        codepoint = ord(c)
        # conditions ordered by presumed frequency
        return (
                0x20 <= codepoint <= 0xD7FF or
                codepoint in (0x9, 0xA, 0xD) or
                0xE000 <= codepoint <= 0xFFFD or
                0x10000 <= codepoint <= 0x10FFFF
        )

    def recurse_xml(root, output):
        if isinstance(output, dict):
            for key in output:
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






    #print(output)

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


