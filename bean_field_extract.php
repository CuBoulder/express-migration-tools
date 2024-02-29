<?php


function t()
{

}

$basepath = '/home/tirazel/Projects/pantheon-upstream-express-production/web/profiles/express/modules/';

function extract_bean_info(string $subpath, string $module_name, bool $is_bean = True)
{
    global $basepath;

    if($module_name == 'cu_video_hero_unit')
    {
        require $basepath . $subpath . '/' . $module_name . '_bundle/' . $module_name . '.bean.inc';
        require $basepath . $subpath . '/' . $module_name . '_bundle/' . $module_name . '.features.field_base.inc';
        require $basepath . $subpath . '/' . $module_name . '_bundle/' . $module_name . '.features.field_instance.inc';

    }
    else
    {
        require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.bean.inc';
        require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.features.field_base.inc';
        require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.features.field_instance.inc';
    }


    $beans = ($module_name . "_bean_admin_ui_types")();

    $instances = ($module_name . "_field_default_field_instances")();
    $bases = ($module_name . "_field_default_field_bases")();


    $beanlist = array();
    $beanlist['name'] = $module_name;
    $beanlist['beans'] = array();


    foreach ($beans as $beans_key => $beans_value)
    {

//        print("#Module: " . $beans_key . "\n\n");
        $beanname = $beans_key;

        $beaninfo = array();
        $beaninfo['name'] = $beans_key;
        $beaninfo['fields'] = array();


        foreach ($instances as $i_key => $i_value)
        {
            $field = array();


            if($beaninfo['name'] != $i_value['bundle'])
            {
                continue;
            }

            $field['name'] = $i_value['field_name'];
            $field['type'] = $i_value['entity_type'];
            $field['bundle'] = $i_value['bundle'];

            foreach ($instances as $f_key => $f_value)
            {
                if($field['name'] == $f_value['bundle'])
                {
                    $afield = array();

                    $afield['name'] = $f_value['field_name'];
                    $afield['type'] = $f_value['entity_type'];
                    $afield['bundle'] = $f_value['bundle'];

                    $beaninfo['fields'][] = $afield;

                }
            }


            $beaninfo['fields'][] = $field;

        }

        $beanlist['beans'][] = $beaninfo;

    }

    return $beanlist;
}


function extract_module_info(string $subpath, string $module_name, bool $is_bean = True)
{
    global $basepath;


    require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.features.inc';
    require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.features.field_base.inc';
    require $basepath . $subpath . '/' . $module_name . '/' . $module_name . '.features.field_instance.inc';



    $beans = ($module_name . "_bean_admin_ui_types")();

    $instances = ($module_name . "_field_default_field_instances")();
    $bases = ($module_name . "_field_default_field_bases")();


    $beanlist = array();
    $beanlist['name'] = $module_name;
    $beanlist['beans'] = array();


    foreach ($beans as $beans_key => $beans_value)
    {

//        print("#Module: " . $beans_key . "\n\n");
        $beanname = $beans_key;

        $beaninfo = array();
        $beaninfo['name'] = $beans_key;
        $beaninfo['fields'] = array();


        foreach ($instances as $i_key => $i_value)
        {
            $field = array();


            if($beaninfo['name'] != $i_value['bundle'])
            {
                continue;
            }

            $field['name'] = $i_value['field_name'];
            $field['type'] = $i_value['entity_type'];
            $field['bundle'] = $i_value['bundle'];

            foreach ($instances as $f_key => $f_value)
            {
                if($field['name'] == $f_value['bundle'])
                {
                    $afield = array();

                    $afield['name'] = $f_value['field_name'];
                    $afield['type'] = $f_value['entity_type'];
                    $afield['bundle'] = $f_value['bundle'];

                    $beaninfo['fields'][] = $afield;

                }
            }


            $beaninfo['fields'][] = $field;

        }

        $beanlist['beans'][] = $beaninfo;

    }

    return $beanlist;
}




function emit_python_bean_schema($beanlist)
{

    print("# Module: " . $beanlist['name'] . "\n\n");


    for($i = 0; $i != count($beanlist['beans']); $i++)
    {

        $bean = $beanlist['beans'][$i];
        $fields = $bean['fields'];

        print("#  Bean: " . $bean['name'] . "\n\n");

        print("bean_" . $bean['name'] . "_fields = []" . "\n");
        for($j = 0; $j != count($fields); $j++)
        {
            print("bean_" . $bean['name'] . "_fields" . ".append({'name': '" . $fields[$j]['name'] . "', 'type': '" .  $fields[$j]['type'] . "', 'bundle': '" . $fields[$j]['bundle'] . "'})" . "\n");
        }
        print("bean_types['" . $bean['name'] . "'] = bean_" . $bean['name'] . "_fields" . "\n\n");
    }

    print("\n");

}


$module_list = array();

$module_list[] = array('subpath' => 'features', 'name' => 'cu_block', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'custom', 'name' => 'cu_block_to_bean', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'custom', 'name' => 'cu_block_row', 'is_bean' => True);

$module_list[] = array('subpath' => 'features', 'name' => 'cu_feature_callout', 'is_bean' => True);
$module_list[] = array('subpath' => 'custom/cu_content_sequence_bundle', 'name' => 'cu_content_sequence', 'is_bean' =>  True);
$module_list[] = array('subpath' => 'features', 'name' => 'cu_article', 'is_bean' =>  True);
$module_list[] = array('subpath' => 'custom', 'name' => 'express_localist_bundle', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'custom', 'name' => 'cu_video_hero_unit', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'features', 'name' => 'people_content_type', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'custom', 'name' => 'cu_expandable', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'features', 'name' => 'cu_slider', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'custom', 'name' => 'cu_video_reveal', 'is_bean' =>  True);

$module_list[] = array('subpath' => 'features', 'name' => 'cu_block_section', 'is_bean' =>  True);

//$module_list[] = array('subpath' => 'features', 'name' => 'cu_faq', 'is_bean' => False);


////$subpath = 'features';
////$module_name = 'cu_feature_callout';
//
//$subpath = 'custom/cu_content_sequence_bundle';
//$module_name = 'cu_content_sequence';

for($i = 0; $i != count($module_list); $i++)
{
    $beanlist = extract_bean_info($module_list[$i]['subpath'], $module_list[$i]['name'], $module_list[$i]['is_bean']);
    emit_python_bean_schema($beanlist);

}













