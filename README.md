# SparkifyUserRetention
Design the data schema for Sparkify business and build predictive model for analyzing user retention



Goal: 
Sparkify is a straming music service. This project will be helping Sparkify to create a data pipline to generate the reporting dashboard and user retention prediction. The source data, which is the user activity log is stored in S3. The data pipeline will be designed for easier maintenance and it will be based on big data environment. 

Scope:
1. Design a dimension model based on its business   
2. Stage data in Redshift and process them to a data lake by Spark.
3. Configured data pipeline with Airflow
4. Build a model to predict the user retention using EMR
5. Create a Tableau Dashboard to analyze the user activity based on data from Redshift and prediction model from step 4



Folder:

1_DataWarehouse:
    script:
    
        create_cluster.py: create a new iam role and create a redshift cluster
        
        create_tables.py: tigger the command to create tables and drop tables
        
        dwh.cfg: configuration file. Includes the keys and secrets of aws account, server name, arn and so on. the important information are removed
        
        etl.py: tigger the command to extract data from S3 bucket, transfrom to the appropriate format and load it to tables in Redshift

2_AirflowConfiguration:
    dags: dag flow
    plugins: helper & operations

3_UserRententionPrediction：
    Sparkify User Retention jupyter notebook: building model using Spark


4_Dashboard:

    tableau workbook
    
    you can also click the link to view the dashboard: https://public.tableau.com/profile/wenxian.fei#!/vizhome/Sparkify_User_Retention/UserAnalysisReport
