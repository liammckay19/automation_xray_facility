#!/bin/bash
source /Users/liam_msg/Documents/automation_local/automation_env/bin/activate
python3 /Users/liam_msg/Documents/automation/updateReq_selenium.py
python3 /Users/liam_msg/Documents/automation/bearbuy_scrape.py
open /Users/liam_msg/Documents/automation/allRequisitions.tsv
python3 /Users/liam_msg/Documents/automation/get_delivery_information.py -reqtsv /Users/liam_msg/Documents/automation/allRequisitions.tsv
python3 /Users/liam_msg/Documents/automation/logistics_info_scrape.py
open /Users/liam_msg/Documents/automation/logistics_info_scrape_output.tsv