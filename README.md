# End-to-End Data Engineering
The Jabar Digital Service (JDS) oversees all data related to West Java Province. One of the datasets they manage is Coronavirus data, which is available to the public through an API. This project aims to :

1. Develop and design a complete data engineering solution using Google Cloud Platform (GCP) services
2. Create a data pipeline that transforms raw data into meaningful insights
3. Visualize the data to meaningful insight

These insights will help inform decision-making and accelerating situation recovery and handling during the pandemic.

# Data Architecture Diagram
![etl architecture diagram](https://github.com/znlbdn/Data-Engineering-Projects/blob/master/include/assets/data_arch_project.png)

Tech in used within this projects are:
1. Google Compute Engine
2. Snowflake
3. PostgreSQL
4. Astronomer (Airflow)
5. DBT
6. Metabase
7. Docker

# Data Flow Diagram
![etl flow diagram](https://github.com/znlbdn/Data-Engineering-Projects/blob/master/include/assets/data_flow_project.png)

# Tale of Project Content
1. Setup Google Compute Engine
2. Setup Snowflake Warehouse, Database, Role and Schema
3. Install and run Docker on VM GCE
4. Install Astro CLI on VM
5. Setup Remote SSH with VSCode
6. Initialize Airflow with Astronomer
7. Initilalize DBT
8. Building Dashboard with Metabase

# Setup Google Compute Engine
You can follow this link to setup your VM instances
https://cloud.google.com/compute/docs/instances/create-start-instance

# Setup Snowflake
Makesure that you have already snwoflake account. And let's configure the warehouse, database, schmea and user role.
```
USE ROLE ACCOUNTADMIN;

-- Create Project Warehouse
CREATE WAREHOUSE IF NOT EXISTS PROJECT_WH WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Create Project Database
CREATE DATABASE IF NOT EXISTS PROJECT_DB;

-- Create Project Role
CREATE ROLE IF NOT EXISTS PRO_ROLE;

-- Check the Grants for PROEJCT_WH Warehouse
SHOW GRANTS ON WAREHOUSE PROJECT_WH;

-- Granting Usage for PRO_ROLE to Warehouse
GRANT USAGE ON WAREHOUSE PROJECT_WH TO ROLE PRO_ROLE;

-- Granting role to user
GRANT ROLE PRO_ROLE TO USER <your username>;

-- Granting All on Database to Role
GRANT ALL ON DATABASE PROJECT_DB TO ROLE PRO_ROLE;

-- Use PRO_ROLE
USE ROLE PRO_ROLE;

-- Create Schema for Jabar Data Schmea
CREATE OR REPLACE SCHEMA PROJECT_DB.JABAR_DATA_SCHEMA;
```

# Setup Docker within GCE Instances
This guide will help you to install docker on GCE instances that you created before
```
sudo apt-get update
sudo apt install gnome-terminal  # For non-Gnome Desktop environments
sudo apt remove docker-desktop   # Remove previous Docker versions (if installed)

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh

sudo docker version # verify docker installation
```
Nice, you have install the docker!

# Installing Astro CLI
To use Astronomer, first you must install the Astro CLI
```
curl -sSL install.astronomer.io | sudo bash -s
```
# Setup SSH on with VSCode
To setup remote connection to our VM using SSH, you must install an VSCode extension (Remote Explorer).
After that you can connect to SSH, but make sure that the google cloud CLI have been installed on you local machine.
Open the terminal on VSCode and run the code below
```
gcloud compute config-ssh
```
And connect with your project account

# Initialize Airflow with Astronomer
To start the airflow project within astro, easily by running this command
```
astro dev init # if promted add sudo on the first command
```

adding some requirements that will use within this project
```
astronomer-cosmos
apache-airflow-providers-snowflake
requests
pandas
psycopg2-binary
snowflake-connector-python
snowflake-sqlalchemy
```
start your airflow using this command
```
astro dev strat
```
wait until terimal sugges you to open new window on port 8080
Nice, now you can create DAG, connection and monitor you job within airflow.

# Initialize DBT
Under the dags folder, create new folder named dbt.
Initialized the dbt project using this command below
```
python3 -m pip install dbt-core # to install dbt core
python3 -m pip install dbt-snowflake # to install the snowflake connection

dbt init # initialize the dbt project
```
set the name and connection for sowflake, you can follow this my previous repository for more detail.

after that you can cretae models and run the models

# Dashboarding with Metabase
Within you docker before, install the Metabase.
```
docker pull metabase/metabase:latest
docker run -d -p 3000:3000 --name metabase metabase/metabase
```
by using two command above, now you can open the metabase by using the <externalapi>:3000

Access my dashoard here : http://34.101.166.169:3000/public/dashboard/f929f00d-85a7-4dbe-833c-eabe2272b1b2

![dashbaord diagram](https://github.com/znlbdn/Data-Engineering-Projects/blob/master/include/assets/dahsboard.png)



