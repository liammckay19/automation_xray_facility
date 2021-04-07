def main():
# https://solutions.sciquest.com/apps/Router/DocumentSearch?ParamAction=ExecuteSavedQuery&QueryId=1585270&FavoriteId=5100296&DocSrchExpRequestExp_ExportTemplate=1&tmstmp=1602872177949
# use this saved search to download and scrape all the POs to see their status.
# The PO number can be matched with the item and the Payment status can be joined to the right



# Get a list of PO#, settlement status

# settlement status location on html
# body > div.PageContent > table.TabSetContainer > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2)

# JS path
# document.querySelector("body > div.PageContent > table.TabSetContainer > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2)")

# style
# color: #000000;
# font-style: normal;
# font-weight: normal;
# font-family: 'Segoe UI', 'Open Sans', Verdana, Geneva, Arial, Helvetica, sans-serif;
# font-size: 1em;
# vertical-align: top;


# match PO#, settlement status to allReq.tsv Requisition	Requisition Number	Company	Number	Item Description	Catalog Number	Size / Packaging	Unit Price	Quantity	Ext. Price	Date Complete	Purchase Order
# PO#  is column 11 if first column is named 1
# PO#  is column 10 if first column is named 0

# something like pandas.join(on="Purchase Order", requsitiontable, postatustable)

if __name__ == '__main__':
    main()