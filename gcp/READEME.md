Prerequisite : 
 - Python3 & pip3

Steps : 
 - pip3 install -r requirement.txt
 - python3 gcp_edc_data_export.py \
    -c $SERVICE_ACCOUNT_JSON \
    -q "select * from $CUSTOMER_DATASET.$TABLE_NAME" \

Parameter 
-c / --cred-file : Absolute path ofService Account JSON [Mandatory]
-q / --query     : Query to run on Datalake             [Mandatory]
-o / --out       : Output CSV File with Path            [Optional]