import sqlalchemy


engine = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/ucbtodaysrc?charset=utf8mb4", echo=False)

# engine2 = sqlalchemy.create_engine(f"mariadb+pymysql://root:pass@localhost/ucbtoday?charset=utf8mb4", echo=False)

engine2 = sqlalchemy.create_engine(f"mariadb+pymysql://pantheon:SVtRLDKPQBYvCajCXJrQmYQKRghefVi0@dbserver.live.dff0ebbe-8cf0-4b16-a2db-a802a1fe78ce.drush.in:12176/pantheon?charset=utf8mb4", echo=False)

aud_map = {}
aud_map[682] = 1304
aud_map[684] = 1305
aud_map[680] = 1306

unit_map = {}
unit_map[722] = 1308
unit_map[728] = 1309
unit_map[900] = 1310
unit_map[718] = 1311
unit_map[1253] = 1312
unit_map[1177] = 1313
unit_map[1173] = 1314
unit_map[1179] = 1315
unit_map[1175] = 1316
unit_map[1181] = 1317
unit_map[1265] = 1318
unit_map[1167] = 1319
unit_map[732] =  1320
unit_map[1262] = 1321
unit_map[724] = 1322
unit_map[730] = 1323
unit_map[1119] = 1324
unit_map[726] = 1325
unit_map[1115] = 1326
unit_map[686] = 1327
unit_map[902] = 1328
unit_map[734] = 1329
unit_map[898] = 1330
unit_map[1004] = 1331
unit_map[1264] = 1332


src_aud = {}
src_unit = {}

def next_delta(nid):
    with engine2.connect() as conn:
        delta_result = conn.execute(sqlalchemy.text(f"select max(delta)+1 as d from node__field_syndication_unit where entity_id = '{nid}';"))
        d = 0
        for result in delta_result:
            if result.d is not None:
                d = result.d
        print(d)
        return d


with engine.connect() as conn:
    # try:
        terms_result = conn.execute(sqlalchemy.text("select entity_id, field_adv_article_synd_unit_tid from field_data_field_adv_article_synd_unit;"))
        for result in terms_result:
            if result.field_adv_article_synd_unit_tid in unit_map:
                tid = unit_map[result.field_adv_article_synd_unit_tid]
                nid = result.entity_id
                # print(f"{nid} {tid}")
                if nid not in src_unit:
                    src_unit[nid] = []
                src_unit[nid].append(tid)
            else:
                print(f"Key not found: {result.field_adv_article_synd_unit_tid}")

        print(src_unit)

        with engine2.connect() as newconn:
            for nid in src_unit:
                if nid >= 53589:
                    continue

                node_result = newconn.execute(sqlalchemy.text(f"select vid from node where nid = '{nid}';"))
                for result in node_result:
                    vid = result.vid

                for tid in src_unit[nid]:

                    if tid != 1329 and tid != 1330 and tid != 1331 and tid != 1332:
                        continue

                    new_row = {}
                    new_row['bundle'] = 'ucb_article'
                    new_row['deleted'] = 0
                    new_row['entity_id'] = nid
                    new_row['revision_id'] = vid
                    new_row['langcode'] = 'en'
                    new_row['field_syndication_unit_target_id'] = tid
                    new_row['delta'] = 0

                    cmd = f"INSERT INTO node__field_syndication_unit (bundle, deleted, entity_id, revision_id, langcode, delta, field_syndication_unit_target_id) VALUES ('ucb_article', '0', '{nid}', '{vid}', 'und', '{next_delta(nid)}', '{tid}');"
                    print(cmd)

                    newconn.execute(sqlalchemy.text(cmd))
                    newconn.commit()







    # except Exception as e:
    #     print(f"Exception: {e}")