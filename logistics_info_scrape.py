import copy
import os
from os import path
import sys
import json as js
import csv
from bs4 import BeautifulSoup
from glob import glob

from tqdm import tqdm

import email_purchase_order_finder

automation_dir = "/"


def top_table_tags(tag):
    return tag.has_attr('valign') and tag.name == 'tr' and "top" in tag['valign']


def processed_information_tags(tag):
    # <div style="width:23.99mm;min-width: 23.99mm;">
    if tag.string:
        return tag.has_attr("style")
    else:
        return False


def main():
    logistics_htmls = glob(path.join('logistics_shipping', '*'))
    PO_to_message = {}
    for html in tqdm(logistics_htmls):
        with open(html, "r") as html_doc:
            PO = html.split(os.sep)[-1].replace('.html', '')
            soup = BeautifulSoup("".join(html_doc.readlines()), 'html.parser')
            try:
                not_received = soup.find_all(top_table_tags)[2].find('div').string  # <tr valign="top">.div.string
                if not_received is "Parcel has not been received at Oyster Point for Package Delivery Program.":
                    PO_to_message[PO] = not_received
            except IndexError:
                pass
            strings_on_webpage = [a.string for a in
                                  soup.find_all(processed_information_tags)]  # <tr valign="top">.div.string
            if "Parcel has not been received at Oyster Point" in strings_on_webpage:
                PO_to_message[PO] = not_received
            else:
                num_processed = 0
                num_delivered = 0
                date = ''
                deliver_date = ''
                for i, s in enumerate(strings_on_webpage):
                    if 'Processed' in s:
                        if "Processed" in strings_on_webpage[i + 1]:
                            num_processed = int(strings_on_webpage[i + 2])
                        else:
                            try:
                                num_processed = int(strings_on_webpage[i + 1])
                            except ValueError:
                                print("num processed unavailable")

                    if 'Delivered:' in s:
                        if "Delivered:" in strings_on_webpage[i + 1]:
                            num_delivered = int(strings_on_webpage[i + 2])
                        else:
                            try:
                                num_delivered = int(strings_on_webpage[i + 1])
                            except ValueError:
                                print("num delivered unavailable")
                    if "Report Print Date/Time:" in s:
                        date = strings_on_webpage[i + 1].rstrip()
                    if s == "Delivered":
                        deliver_date = strings_on_webpage[i + 6]

                emailed_bool = False
                emailed = list(email_purchase_order_finder.search_email('(BODY "{0}")'.format(PO)))
                if "OK" in emailed:
                    emailed_bool = True

                PO_to_message[PO] = {"Delivered": num_delivered, "Processed": num_processed,
                                     "Deliver Date": deliver_date, "Date": date, "Emailed": emailed_bool}
    print(PO_to_message)

    with open(os.path.join(automation_dir, "logistics_info_scrape_output.tsv"), 'w') as tsv_o:
        tsv_o.write("Purchase Order\tDelivered\tProcessed\tDate Delivered\tDate\n")

        for po, info in PO_to_message.items():
            tsv_o.write(
                "{po}\t{delivered}\t{processed}\t{deliverdate}\t{date}\t{emailed}\n".format(po=po.rstrip(),
                                                                                            delivered=info['Delivered'],
                                                                                            processed=info['Processed'],
                                                                                            deliverdate=info[
                                                                                                "Deliver Date"],
                                                                                            date=info['Date'],
                                                                                            emailed=info['Emailed']))

if __name__ == '__main__':
    main()
