# automation_xray_facility
 General Automation for the UCSF Xray Lab Manager. 
## Bearbuy Automation
This automates with Selenium/Python the hassle of going through all the previous purchase orders that have been made on BearBuy and compiles a table of purchase orders.

### Features:

- Bearbuy requisition + purchase report + emails associated
- Scrapes information for every Requisition into a JSON format

 Example:

| Requisition                                               | Requisition Number | Company           | Number | Item Description                                                                                                                                            | Catalog Number | Size / Packaging | Unit Price | Quantity | Ext. Price | Date Complete      | Purchase Order |
|-----------------------------------------------------------|--------------------|-------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|------------------|------------|----------|------------|--------------------|----------------|
| bearbuy_requisitions/Summary - Requisition 128146338.html | 128146338          | FASTENAL COMPANY  | 1      | Air / Water Hose - 1/4"IDx29/64"OD Clear H285 250PSI Low Pressure Hose(50'PricedPerFt)                                                                      | 0447021        | EA               | 0.7606     | 35/EA    | 26.62      | 1/16/2020 5:25 PM  | B001821448     |
| bearbuy_requisitions/Summary - Requisition 125421656.html | 125421656          | FISHER SCIENTIFIC | 1      | Accessory for PIPETMAN Complete Pipetting System- Reagent Reservoirs Polystyrene White, Use With: Pipetteman complete pipetting system 50mL, F267670 10/PK  | F267670G       | PK               | 180.23     | 1/PK     | 180.23     | 11/4/2019 11:53 AM | B001774860     |
| bearbuy_requisitions/Summary - Requisition 125421656.html | 125421656          | FISHER SCIENTIFIC | 2      | Accessory for PIPETMAN Complete Pipetting System- Reagent Reservoirs Polystyrene White, Use With: Pipetteman complete pipetting system 25mL, F267660 100/PK | F267660G       | PK               | 133.00     | 1/PK     | 133.00     | 11/4/2019 11:53 AM | B001774860     |


### Quickstart:

- Install Firefox https://www.mozilla.org/en-US/firefox/new/

- Download geckodriver https://github.com/mozilla/geckodriver/releases
- Put geckodriver exec. in <code>/usr/local/bin/geckodriver</code>
- <code>git clone https://github.com/liammckay19/automation.git </code>
- <code>pip install requirements.txt</code>
- Create a file called <code>credentials_myaccess_email.json</code> with these contents in the file. UCSF email and password are required

```json
{
  "username": "first.lastname@ucsf.edu",
  "password": "moresecurethan_password1234"
}
```


- Create another file called <code>credentials_email.json</code> with these contents in the file. This is the email where you get purchase orders sent to.
```json
{
  "username": "first.lastname@gmail.com",
  "password": "moresecurethan_password1234"
}
```

- Important: To stop the program at anytime, hit ctrl-c
- <code>python run_update_bearbuy_inventory.py</code>
- <code>allRequisitions.tsv</code> is the resulting output. Copy and paste this into a Google Spreadsheet for viewing. 
