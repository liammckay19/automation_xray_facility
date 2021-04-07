import updateReq_selenium
import bearbuy_scrape
import get_delivery_information
import logistics_info_scrape
import merge_logistics_delivery_requisition
import argparse
import uploadToBearbuyReq

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-reqtsv", "--requisition_directory", help="optional path to location of HTML files",
                        required=False)
    parser.add_argument("-file", "--file_extension", help="optional file extension for HTM files", required=False)
    parser.add_argument("-email", "--email_find", help="optional search gmail for purchase orders", required=False, action='store_true')
    parser.add_argument("-r", "--hard_run", help="overwrite allRequisitions.tsv", required=False, action='store_true')
    args = parser.parse_args()
    updateReq_selenium.main(args)
    bearbuy_scrape.main(args)
    uploadToBearbuyReq.main()
    # get_delivery_information.main()
    # logistics_info_scrape.main()
    # merge_logistics_delivery_requisition.main()

main()