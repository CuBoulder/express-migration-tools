#!/bin/bash
set -e

terminus env:wake $1.live
terminus site:upstream:clear-cache $1
terminus upstream:updates:apply $1.dev --accept-upstream
terminus env:deploy $1.test --yes
terminus env:deploy $1.live --yes --updatedb --cc
terminus remote:drush $1.live -- cr
terminus remote:drush $1.live -- en media_alias_display media_entity_file_replace media_file_delete menu_block ckeditor5_paste_filter scheduler layout_builder_iframe_modal linkit administerusersbyrole google_tag menu_firstchild responsive_preview anchor_link smtp recaptcha_v3 rebuild_cache_access ckeditor5_bootstrap_accordion ucb_drush_commands menu_item_extras ucb_styled_block --yes
terminus remote:drush $1.live -- features:import cu_boulder_content_types --yes
terminus remote:drush $1.live -- config:import --partial --source=/code/web/profiles/custom/boulder_profile/config/install --yes
terminus remote:drush $1.live -- updb --yes;
terminus remote:drush $1.live -- cr;
terminus remote:drush $1.live -- config:set boulder_base.settings web_express_version "20241030" --yes
