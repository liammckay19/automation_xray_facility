import pandas as pd
from glob import glob
import os

automation_dir = "/Users/liam_msg/Documents/automation"

delivery_df = pd.read_csv(glob(os.path.join(automation_dir, 'logistics_info_scrape_output.tsv'))[0], sep='\t',
                          dtype=str).reset_index().drop(columns="Purchase Order").rename(columns={"index":"Purchase Order"})
print(delivery_df)

requisition_df = pd.read_csv(glob(os.path.join(automation_dir, 'allRequisitions.tsv'))[0],
                             sep='\t', dtype=str)


print(requisition_df)
date_deliver_requisition = pd.merge(requisition_df, delivery_df, on='Purchase Order')

date_deliver_requisition.to_csv(path_or_buf=os.path.join(automation_dir, 'allRequisition_date.tsv'), sep='\t',
                                index=False, index_label=False)
