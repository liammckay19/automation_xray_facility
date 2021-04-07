from googleDriveUtils import authorizeGoogleDriveUsage
import pygsheets as pyg
import pandas as pd
from glob import glob
from datetime import datetime
gc = authorizeGoogleDriveUsage('/Users/liam_msg/Documents/automation/project-id-9593510060528633608-c268bb362046.json')


def main():
    bearbuy_ss = gc.open_by_key('1XZRQlNG4QuFHyc3Q2AGtMSWBTNgxwDjSPVOo_KuJHA4')
    dump = bearbuy_ss.worksheet('title','dump_allRequisitions-tsv_data_webscrape')
    all_req_df = pd.read_csv(glob('allRequisitions.tsv')[0], skiprows=1, sep='\t').fillna('')
    dump.update_value('A1', str(datetime.today()))
    dump.update_values('A2', ["Requisition	Requisition Number	Company	Number	Item Description	Catalog Number	Size / Packaging	Unit Price	Quantity	Ext. Price	Date Complete	Purchase Order".split('\t')])
    dump.update_values('A3',all_req_df.values.tolist())
main()