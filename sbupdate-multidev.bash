#!/bin/bash
set -e

terminus env:wake $1.prod-clone
terminus env:deploy $1.prod-clone --yes --updatedb --cc
terminus remote:drush $1.prod-clone -- cr
terminus remote:drush $1.prod-clone -- en media_alias_display media_entity_file_replace media_file_delete menu_block ckeditor5_paste_filter scheduler layout_builder_iframe_modal linkit administerusersbyrole google_tag menu_firstchild responsive_preview anchor_link smtp recaptcha_v3 rebuild_cache_access ckeditor5_bootstrap_accordion ucb_drush_commands menu_item_extras ucb_styled_block ucb_linkmod trash entity_usage paragraphs_library --yes
terminus remote:drush $1.prod-clone -- features:import cu_boulder_content_types --yes
terminus remote:drush $1.prod-clone -- config:import --partial --source=/code/web/profiles/custom/boulder_profile/config/install --yes
terminus remote:drush $1.prod-clone -- updb --yes;
terminus remote:drush $1.prod-clone -- cr;
terminus remote:drush $1.prod-clone -- config:set boulder_base.settings web_express_version "20250212" --yes
