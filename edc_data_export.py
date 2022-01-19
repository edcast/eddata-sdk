# Version 2.0
# Last update date - 09/22/2021
# Built for qa, preview and prod environment only
# Below script is modifed to handle GCP on 19/01/2022

import os
import time as t
import re
import sys
import argparse


GCP_ENV = os.environ.get('GCP_ENV', 'No')

if GCP_ENV == 'yes':
    
    from google.cloud import bigquery
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--cred_file", "-c", help = "Absolute path of the service account json")
    parser.add_argument("--query", "-q", help = "Query to run against bigquery")
    parser.add_argument("--out", "-o", help = "Path with file name - '/home/user/user_card_perf.csv'", default= "./output.csv")
    args = parser.parse_args()

    CRED_FILE = args.cred_file
    QUERY = args.query
    OUTPUT = args.out

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CRED_FILE

    client = bigquery.Client()

    result = client.query(QUERY).to_dataframe()  # Make an API request.

    print("Storing data in CSV : " + OUTPUT)
    result.to_csv(OUTPUT, index=False) 

else:
    import boto3
    import numpy
    VERSION = 2.0
    BUILT_ON = '2021-09-22 06:00:00 PST'

    def get_version():
        return "version={} built-on {}".format(VERSION, BUILT_ON)


    def validate_region(args={}):
        if args["REGION"] not in AWS_REGIONS:
            print("\n The given region is not supported, please enter a valid region. For help run the script with --help\n")
            exit()
        else:
            global region
            region = args["REGION"]
            return


    def validate_query(args={}):
        if 'where' not in args["QUERY"].lower():
            print("\n Please use filters in the query, without using filters in query might fetch whole chunk of data\n")
            exit()
        flag = 0
        for table in TABLES:
            if table in args["QUERY"].lower():
                flag = 1
                break
        if flag == 0:
            print("\nNo supported tables in the query. For more information run script with --help argument\n")
            exit()
        else:
            global query
            query = args["QUERY"]
            return


    def validate_access_key(args={}):
        valid_access_key = re.search(
            "(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])", args["AWS_ACCESS_KEY_ID"])
        if valid_access_key == None:
            print("\nNot a valid access key. Please check or contact EdCast support team.\n")
            exit()
        else:
            global AWS_ACCESS_KEY_ID
            AWS_ACCESS_KEY_ID = args["AWS_ACCESS_KEY_ID"]
            return


    def validate_secret_access_key(args={}):
        valid_secret_key = re.search(
            "(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])", args["AWS_SECRET_ACCESS_KEY"])
        if valid_secret_key == None:
            print("\n.Not a valid secret key. Please check or contact EdCast support team.\n")
            exit()
        else:
            global AWS_SECRET_ACCESS_KEY
            AWS_SECRET_ACCESS_KEY = args["AWS_SECRET_ACCESS_KEY"]
            return


    def validate_filename(args={}):
        if not args["FILENAME"].endswith('.csv'):
            print("\n Not a valid csv filename \n")
            exit()
        else:
            global filename
            filename = args["FILENAME"]
            return


    def validate_s3bucket(args={}):
        if args["S3BUCKET"] == "":
            print("\n S3 bucket cannot be null \n")
            exit()
        else:
            global s3bucket
            s3bucket = args["S3BUCKET"]
            return


    def validate_org_id(args={}):
        if args["ORG_ID"] == "":
            print("\n ORG_ID cannot be null \n")
            exit()
        else:
            global org_id
            org_id = args["ORG_ID"]
            return


    def validate_environment(args={}):
        if args["ENV"] not in ['prod', 'preview', 'qa']:
            print(
                "\n Environment not supported. Please check or contact EdCast support team.\n")
            exit()
        else:
            global env
            env = args["ENV"]
            return

    def validate_input_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--region", help="The region name that was provided by EdCast support team")
        parser.add_argument(
            "--query", help="The query which you want to bulk download")
        parser.add_argument("--aws_access_key_id",
                            help="The aws access key that was provided by EdCast support team")
        parser.add_argument("--aws_secret_access_key",
                            help="The aws secret key that was provided by EdCast support team")
        parser.add_argument(
            "--filename", help="The filename and path where the file will be saved")
        parser.add_argument(
            "--s3bucket", help="The s3 bucket that was provided by EdCast support team")
        parser.add_argument(
            "--org_id", help="The organization id that was provided by EdCast support team")
        parser.add_argument(
            "--env", help="The environment that was provided by EdCast support team")
        args = parser.parse_args()
        if(args.region == None or args.query == None or args.aws_access_key_id == None or args.aws_secret_access_key == None or args.filename == None or args.s3bucket == None or args.org_id == None or args.env == None):
            print("\nNot all required arguments are given.\n")
            return 0
        else:
            validate_region({
                "REGION": args.region
            })
            validate_query({
                "QUERY": args.query
            })
            validate_access_key({
                "AWS_ACCESS_KEY_ID": args.aws_access_key_id
            })
            validate_secret_access_key({
                "AWS_SECRET_ACCESS_KEY": args.aws_secret_access_key
            })
            validate_filename({
                "FILENAME": args.filename
            })
            validate_s3bucket({
                "S3BUCKET": args.s3bucket
            })
            validate_org_id({
                "ORG_ID": args.org_id
            })
            validate_environment({
                "ENV": args.env
            })
            return 1


    def get_help():
        print("\n Prerequisite for running the script")
        print("\n   Install the following")
        print("         - python (recommended python3)")
        print("         - run \"pip3 install -r requirements.txt\"")
        print("\n How to run this script and supporting arguments")
        print(" ================================================")
        print("\n Run the script by running the command -> \"python edc_bulk_downlaod.py\"")
        print("\n The script will prompt with a set of input arguments on interactive mode or you can pass the arguments,")
        print("\n - Enter your region: 'REGION_NAME' eg us-east-2 or eu-central-1 ")
        print("\n - Enter the query: 'QUERY' - the SQL compatible query to download the data.\n")
        print("     1. The query cannot be without any filters ")
        print("     2. The query should only query from the tables listed below")
        for table in TABLES:
            print("         - {0}".format(table))
        print("\n     3. Example queries are")
        print("         - \"select * from user_card_performance_reporting_i_v where day=’2020-04-01’\"")
        print("         - \"select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’\"")
        print("         - \"select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and user_email=’admin@acme.com’\"")
        print("         - \"select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and user_first_name like ’admin%\"")
        print("         - \"select * from user_card_performance_reporting_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and card_tile like ‘admin%’\"")
        print("         - \"select * from user_assignments_performance_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ and assignment_state=’completed’\"")
        print("         - \"select * from group_assignments_performance_i_v where day between ‘2020-04-01’ and ‘2020-04-04’ \"")
        print("\n - Enter your aws_access_key_id: 'AWS_ACCESS_KEY_ID' the key ID that was provided by EdCast support team.")
        print("\n - Enter your aws_secret_access_key: 'AWS_SECRET_ACCESS_KEY' the secret key that was provided by EdCast support team.")
        print("\n - Enter the file location along with the filename to be saved: 'FILENAME' the path and the filename where you want to save the file. The only supported file type is csv.")
        print("\n - Enter the s3 bucket name that was provided by EdCast support team: 'S3_BUCKET' the name of the S3 bucket that was provided by EdCast support team")
        print("\n - Enter the org_id that was provided by EdCast support team: org_id the ID of the organization that was provided by EdCast support team")
        print("\n - Enter the env that was provided by EdCast support team: environment name that was provided by EdCast support team")


    def start_query_execution():
        client = boto3.client(
            'athena',
            region_name=region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        try:
            execution = client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={
                    'Database': database
                },
                WorkGroup=workgroup
            )
        except Exception as e:
            print(e)
            print("\nUnexpected error while exporting the data. Please check query,org_id or S3_BUCKET values or contact EdCast support team. \n")
            exit()

        query_execution_id = execution['QueryExecutionId']
        query_state = 'RUNNING'
        execution_count = 1
        retry_count = 900
        while (execution_count <= retry_count and query_state in ['QUEUED', 'RUNNING']):
            # Get Query Execution
            response = client.get_query_execution(
                QueryExecutionId=query_execution_id)

            if 'QueryExecution' in response and 'Status' in response['QueryExecution'] and 'State' in response['QueryExecution']['Status']:
                query_state = response['QueryExecution']['Status']['State']
                if query_state == 'SUCCEEDED':
                    print("STATUS: " + query_state)
                    print(
                        "\nData export is complete and it's stored in {0}.\n".format(filename))
                    return query_execution_id
                    break
                elif query_state == 'FAILED':
                    reason = response['QueryExecution']['Status']['StateChangeReason']
                    raise Exception("STATUS: " + query_state +
                                    ", Due to:" + reason)
                else:
                    print("STATUS: " + query_state)
                    t.sleep(1)
            execution_count += 1
        else:
            client.stop_query_execution(QueryExecutionId=query_execution_id)
            raise Exception(
                '\n Query execution is taking too long and timed out after 15 minutes. Please use filters/limits in the query to limit no of records and try again or contact EdCast support team. \n')


    def download_file():
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            object_name = PREFIX + execution_id + ".csv"
            with open(filename, 'wb') as f:
                s3.download_fileobj(BUCKET_NAME, object_name, f)
        except Exception as e:
            print(e)
            print("\nUnexpected error while downloading the data. Please check S3_BUCKET values or contact EdCast support team. \n")
            exit()


    TABLES = ['assignments_fact_m_v', 'badges_dim_m_v', 'card_pack_relations_dim_m_v', 'card_performance_hourly_rollups_i_v', 'card_reportings_dim_m_v', 'cards_dim_m_v', 'channel_performance_hourly_rollups_i_v', 'channel_performance_reporting_i_v', 'channels_cards_dim_m_v', 'channels_dim_m_v', 'comments_fact_m_v', 'custom_fields_dim_m_v', 'group_assignments_performance_i_v', 'group_performance_hourly_rollups_i_v', 'group_performance_reporting_i_v', 'groups_dim_m_v', 'invalid_user_card_performance_reporting_i_v', 'journey_pack_relations_dim_m_v', 'mkp_course_event_review_dim_m_v', 'mkp_course_events_dim_m_v', 'mkp_courses_dim_m_v', 'mkp_daily_attendance_dim_m_v', 'mkp_learner_events_dim_m_v', 'organizations_dim_m_v', 'profiles_dim_m_v', 'quizzes_fact_m_v', 'roles_dim_m_v', 'searches_fact_i_v', 'skills_users_dim_m_v', 'structured_items_fact_m_v', 'structures_dim_m_v', 'team_assignments_fact_m_v', 'teams_dim_m_v', 'teams_users_fact_m_v', 'user_assignments_performance_i_v', 'user_card_performance_reporting_i_v', 'user_content_completions_dim_m_v', 'user_custom_fields_dim_m_v', 'user_metrics_aggregations_fact_m_v', 'user_onboardings_dim_m_v', 'user_performance_hourly_rollups_i_v', 'user_profiles_fact_m_v', 'users_dim_m_v']

    if ('--{}'.format('help') in sys.argv):
        get_help()
        exit()
    elif ('--{}'.format('version') in sys.argv):
        print("\n{0}\n".format(get_version()))
        exit()


    region = query = AWS_ACCESS_KEY_ID = AWS_SECRET_ACCESS_KEY = filename = database = s3bucket = env = ""

    AWS_REGIONS = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'eu-central-1', 'ap-south-1', 'ap-southeast-2']

    validate = validate_input_args()

    if(validate == 0):

        region = input("Enter your region: ")
        validate_region({
            "REGION": region
        })

        query = input("Enter the query: ")
        validate_query({
            "QUERY": query
        })

        AWS_ACCESS_KEY_ID = input(
            "Enter aws_access_key_id that was provided by EdCast support team: ")
        validate_access_key({
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID
        })

        AWS_SECRET_ACCESS_KEY = input(
            "Enter aws_secret_access_key that was provided by EdCast support team: ")
        validate_secret_access_key({
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY
        })

        filename = input(
            "Enter the file location along with the filename to be saved: ")
        validate_filename({
            "FILENAME": filename
        })

        s3bucket = input(
            "Enter the s3 bucket name that was provided by EdCast support team: ")
        validate_s3bucket({
            "S3BUCKET": s3bucket
        })

        org_id = input(
            "Enter the org_id that was provided by EdCast support team: ")
        validate_org_id({
            "ORG_ID": org_id
        })

        env = input("Enter the env that was provided by EdCast support team: ")
        validate_environment({
            "ENV": env
        })

    if env == 'qa':
        database = "v1_edc_qa_analytics_customer_database_{0}".format(str(org_id))
    else:
        database = "v1_edc_"+env+"_analytics_customer_database_{}".format(str(org_id))

    workgroup = "{}".format(org_id)

    PREFIX = "athena_query_results/org_id={}/".format(org_id)
    BUCKET_NAME = s3bucket
    S3_OUTPUT_LOCATION = "s3://" + BUCKET_NAME + "/" + PREFIX
    if database:
        execution_id = start_query_execution()
    else:
        print("\n.Not a valid database.\n")
        exit()

    if execution_id:
        download_file()
    else:
        print("\n.Unexpected error while exporting the data. Please try again! \n")
        exit()