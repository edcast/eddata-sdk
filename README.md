# eddata-sdk
SDK to query EdCast's data lake

# Installation
This python based utility can be installed and run from a Unix or Windows environment. Below are the steps to install and run the utility.


# Install python3
Download data export utility zip from here
Extract the content of the data export utility zip file to a local folder. This folder includes below 2 files
requirements.txt - This files contains the python libraries required by the utility
edc_bulk_download.py - This is the data export utility that connects to the data lake and downloads the file as CSV
Install the python pre-req libraries using below command
pip3 install -r requirements.txt

Command to run
python3 edc_data_export.py --region us-east-1 --query "select * from user_card_performance_reporting_i where day=’2020-04-01’" --aws_access_key_id <<sample_access_key>> --aws_secret_access_key <<sample_secret_key>> --filename download_data.csv --s3bucket  edcast-provided-bucket-name --org_id 100000 --env prod

Above command runs and stores the extracted data in CSV format in the download_data.csv.
Sample Queries
Some sample queries that can be used in the utility

select * from user_card_performance_reporting_i where day=’2020-04-01’
select * from user_card_performance_reporting_i where day between ‘2020-04-01’ and ‘2020-04-04’
select * from user_card_performance_reporting_i where day between ‘2020-04-01’ and ‘2020-04-04’ and user_email=’admin@acme.com’
select * from user_card_performance_reporting_i where day between ‘2020-04-01’ and ‘2020-04-04’ and user_first_name like ’admin%
select * from user_card_performance_reporting_i where day between ‘2020-04-01’ and ‘2020-04-04’ and card_tile like ‘admin%’
select * from user_assignments_performance_i where day between ‘2020-04-01’ and ‘2020-04-04’ and assignment_state=’completed’


There is no output to the utility call, a file will be downloaded locally with the given name.
