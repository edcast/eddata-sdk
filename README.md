# EdData-sdk

# [AWS](https://github.com/avinash-u/eddata-sdk/tree/gcp-eddata-sdk#installation)
# [GCP](https://github.com/avinash-u/eddata-sdk/tree/gcp-eddata-sdk#gcpenvironment)

## AWS Environment 
SDK to query EdCast's data lake. This is a wrapper script which uses AWS Athena python SDK to query and download the data.


## Installation
This python based utility can be installed and run from a Unix or Windows environment. Below are the steps to install and run the utility.

1. Install python3
2. Install the python pre-req libraries using below command

````
        pip3 install -r requirements.txt
````
## Command to run
````
python3 edc_data_export.py --region us-east-1 --query "select * from user_card_performance_reporting_i_v where day=’2020-04-01’" --aws_access_key_id <<sample_access_key>> --aws_secret_access_key <<sample_secret_key>> --filename download_data.csv --s3bucket  edcast-provided-bucket-name --org_id 100000 --env prod
````
Above command runs and stores the extracted data in CSV format in the download_data.csv.



## Downloading each EdData dataset
This is the section where downloading of data in the past hour for every single eddata dataset is described below.

## Sample Queries for AWS
Some sample queries that can be used in the utility.

````
select * from user_card_performance_reporting_i_v where day=’2020-04-01’
select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’
select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and user_email=’admin@acme.com’
select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and user_first_name like ’admin%
select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and card_tile like ‘admin%’
select * from user_assignments_performance_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and assignment_state=’completed’
````
There is no output to the utility call, a file will be downloaded locally with the given name.


## GCP ENVIRONMENT

SDK to query EdCast's data lake. This is a wrapper script which uses BigQuery python SDK to query and download the data.

# Installation
This python based utility can be installed and run from a Unix or Windows environment. Below are the steps to install and run the utility.

1. Install python3
2. Install the python pre-req libraries using below command

````
        pip3 install -r gcp_requirements.txt
````
# Command to run 
````
GCP_ENV=yes python3 edc_data_export.py \
    -c $SERVICE_ACCOUNT_JSON \
    -q "select * from $CUSTOMER_DATASET.$TABLE_NAME" \
````
Above command runs and stores the extracted data in CSV format in the output.csv

# Downloading each Eddata dataset
This is the section where downloading of data in the past hour for every single eddata dataset is described below.

# Sample Queries for GCP
Some sample queries that can be used or refrenced.

````
SELECT * FROM edc_qa_analytics_customer_100006.o_user_card_performance
SELECT * FROM edc_qa_analytics_customer_100006.o_user_assignments_performance
````
The output file will be downloaded locally with the given name.