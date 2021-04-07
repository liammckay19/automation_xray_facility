import string

from tqdm import tqdm

from datetime import datetime
import email_purchase_order_finder
from bs4 import BeautifulSoup
import copy
import os
import sys
import json as js
import csv
import glob
import argparse

# Author Liam McKay
automation_dir = "."
parser = argparse.ArgumentParser()
parser.add_argument("-reqtsv", "--requisition_directory", help="optional path to location of HTML files",
                    required=False)
parser.add_argument("-file", "--file_extension", help="optional file extension for HTM files", required=False)
parser.add_argument("-email", "--email_find", help="optional search gmail for purchase orders", required=False,
                    action='store_true')
parser.add_argument("-r", "--hard_run", help="overwrite allRequisitions.tsv", required=False, action='store_true')
args = parser.parse_args()


def match_class(target):
    def do_match(tag):
        try:
            classes = dict(tag.attrs)["class"]
        except KeyError:
            classes = ""
        return all(c in classes for c in target)

    return do_match


# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-the-tree
def has_class(tag):
    return tag.has_attr('class')


def po_information_tags(tag):
    return tag.has_attr('class') and tag.has_attr('href') and tag.has_attr('tabindex') and "ElementValue" in tag[
        'class']


def main(args):
    run_script = "y"
    if os.path.exists("allRequisitions.tsv") and args.hard_run == False:
        run_script = input("Requisition table detected. Perform BearBuy webscraping? y/n")
    if run_script == 'n':
        return
    if args.requisition_directory:
        if args.file_extension:
            html_files = glob.glob(os.path.join(args.requisition_directory, "*." + args.file_extension))
        else:
            html_files = glob.glob(os.path.join(args.requisition_directory, "*.html"))
        print(len(html_files), "htmls found")
    else:
        html_files = glob.glob(os.path.join('bearbuy_requisitions', "*.html"))
    output_tsv = ""
    for file_name in tqdm(html_files):
        rows_processed = 0

        with open(file_name, "r") as html_doc:
            soup = BeautifulSoup("".join(html_doc.readlines()), 'html.parser')

            # the magic location of the info (hopefully BearBuy doesn't update their HTML soon)
            company_boxes = soup.find(['div', 'table', 'tbody', 'tr', 'td', 'div', 'div',
                                       'div', 'table', 'tbody', 'tr', 'td'], recursive=True, attrs="ForegroundPanel")

            try:
                date_completed = soup.find(['td', 'div', 'table', 'tbody', 'td', 'div'], recursive=True,
                                           attrs=["TabbedBackgroundPanel", "tabpanel"])
                date_completed_further = [a.find('div') for a in date_completed.contents[3].table.tbody.children][4]
                date = [a.find('div') for a in date_completed_further.table.tbody.children][2]
                date_str = date.div.string.rstrip().replace("\n", '').replace('(', '').replace(')', '')
            except (AttributeError, IndexError) as e:
                print("Couldn't find date for " + file_name)
                date_str = ''
            text_in_general_box = [a.string for a in soup.find_all(po_information_tags)]
            purchase_orders = []
            for t in text_in_general_box:
                if t:
                    if len(t) > 0:
                        if "B0" in t:
                            purchase_orders.append(t)
            try:
                findmysiblings = copy.copy(company_boxes.div.div.find('a', 'SupplierName'))
            except AttributeError as e:
                print(e)
                continue

            po_idx = 0
            json = {}
            for child in company_boxes.div.div.children:
                splitRows = False
                company = child.find("a")
                if child.find("a") != -1:
                    if "Subtotal" in company.string:
                        continue
                    if "Hide line details" not in company.string:
                        try:
                            json[company.string] = {purchase_orders[po_idx]: {}}
                        except IndexError:
                            json[company.string] = {str(po_idx) + " Pending": {}}
                        row = []
                        for i, td in enumerate(child.find_all("td", "LineSixPack")):  # item bought information
                            for a in td.stripped_strings:
                                if "more info..." not in a and 'Select (' not in a:
                                    row.append(a.replace("\xa0", '').replace('USD', '').replace('\n', '/'))
                            if i > 10:
                                splitRows = True
                        if splitRows:
                            list_rows = []
                            indices = [0]
                            for i, item in enumerate(row):
                                if "addLineData" in item:
                                    indices.append(i + 1)
                            for i in range(len(indices) - 1):
                                list_rows.append(row[indices[i]:indices[i + 1] - 1])
                            if list_rows:
                                try:
                                    json[company.string][purchase_orders[po_idx]] = {row[0]: row[1:] for row in
                                                                                     list_rows}
                                except IndexError:
                                    json[company.string][str(po_idx) + " Pending"] = {row[0]: row[1:] for row in
                                                                                      list_rows}
                        else:
                            if row:
                                try:
                                    json[company.string][purchase_orders[po_idx]] = {row[0]: row[1:-1]}
                                except IndexError:
                                    json[company.string][str(po_idx) + " Pending"] = {row[0]: row[1:-1]}
                        # if json:
                        #     email_list = email_purchase_order_finder.search_email(
                        #         purchase_orders[po_idx].replace(string.whitespace, ""))
                        #     json[company.string][purchase_orders[po_idx]][row[0]].append(
                        #         " ".join(email_list.__str__().split()))
                        #     print(email_list.__str__())
                        po_idx += 1
                rows_processed += 1

        # add data to output_tsv string
        # Requisition Requisition Number  Company Number  Item Description    Catalog Number  Size / Packaging    Unit Price  Quantity    Ext. Price  Date Complete   Purchase Order
        # 
        for company, things_bought in json.items():
            for po, row in things_bought.items():
                for number, item in row.items():
                    output_tsv += file_name + "\t" + file_name.split(os.sep)[-1].replace("Summary - Requisition ",
                                                                                         "").replace(".html",
                                                                                                     "") + "\t" + company + "\t" + number + "\t"
                # "Requisition
                    # Requisition Number
                    # Company
                    # Number
                    # Item Description
                    # Catalog Number
                    # Size / Packaging
                    # Unit Price
                    # Quantity
                    # Ext. Price
                    # Date Complete
                    # Purchase Order
                    # \t\t\t\t\t\t\n")

                    output_tsv += item[0] + "\t"
                    if "/EA" not in item[1]:
                        output_tsv += item[1] + "\t"
                    else:
                        output_tsv += "\t"
                    output_tsv += item[-4] + "\t"
                    output_tsv += item[-3] + "\t"
                    output_tsv += item[-2] + "\t"
                    output_tsv += item[-1] + "\t"
                    output_tsv += date_str + "\t"
                    output_tsv += po
                    if args.email_find == True:
                        email_list = email_purchase_order_finder.search_email(
                            item[1].replace(string.whitespace, ""))  # catalog number
                        if email_list == []:
                            email_list += email_purchase_order_finder.search_email(
                                po.replace(string.whitespace, ""))  # purchase order number
                        emails_related = " ".join(email_list.__str__().split())
                        output_tsv += "\t" + emails_related  # new as of 9/24/2020
                    output_tsv += "\n"

        json['Date'] = date_str

        with open(os.path.join(automation_dir, file_name.replace("html", 'json')), 'w') as json_file_out:
            js.dump(json, json_file_out)
        if json:
            pass
            # print("wrote to " + "data" + file_name.replace("html", 'json') + "\t Lines Found = " + str(rows_processed))
        else:
            print("json is empty for " + "data" + file_name.replace("html", 'json'))

    today = datetime.today()
    # output_tsv to allRequisitions.tsv
    with open(os.path.join(automation_dir, "allRequisitions.tsv"), 'w') as tsvout:
        tsvout.write("Scrape performed on: " + str(today) + "\n")
        tsvout.write(
            "Requisition\tRequisition Number\tCompany\tNumber\tItem Description\tCatalog Number\tSize / Packaging\tUnit Price\tQuantity\tExt. Price\tDate Complete\tPurchase Order\t\t\t\t\t\t\t\n")
        tsvout.write(output_tsv)
    print("wrote to allRequisitions.tsv")


if __name__ == '__main__':
    main(args)
