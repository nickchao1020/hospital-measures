# Overview

This repository contains a pipeline to create an elasticsearch index from the Hospital Measurement data, make queries on the index, and upload the docker image to AWS ECR.

For evaluating code:

The code I wrote to setup the necessary .json file that populates my elasticsearch index is located in /scripts/etl.py.
The script /scripts/create.sh will create the index, then upload its mapping and documents.

/scripts/create_plot.py is where I query elasticsearch and build the plots. The logic to build the query is in /scripts/utils.py


# Usage

### Starting ElasticSearch
(This assumes docker is installed and running on your machine)

First, pull an elasticsearch docker image from the Elastic Docker Registry registry;

`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.8.1`


Now that we have an elasticsearch docker image, we can run it with:

`docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.8.1`

### Creating documents for hospital measurement ES index

After elasticsearch is running, an index for the hospital measurement dataset is created by running:

`python3 etl.py path/to/Healthcare Associated Infections - Hospital.csv`

This script will create the documents.json file that can be used to populate the index with the data.

### Create the hospital measure index

With the data prepared, navigate to the es-index/ directory and run the following command to build the index:

`./create.sh`

If permissions are denied, give permissions using `sudo chmod 755 create.sh`.

### Generating plot

Now that the index is created and populated, the state-measurement bar plot can created by running
the create_plot.py script. This script takes an input argument for the filepath where you want
to save the plot:

`python3 scripts/create_plot.py path/to/save/plot.png`

### Pushing image to AWS ECR

We can now push the elasticsearch image we are using to ECR, which allows us to access it through services like ECS.

First, get the image id by running `docker images` and finding the elasticsearch image.

Next, tag the image using it's image id to our ECR repository using this command:

`docker tag <image-id> <aws_id>.dkr.ecr.<aws-region>.amazonaws.com/hospital-data`

Finally, push the image to ECR using:

`docker push <aws_id>.dkr.ecr.<aws-region>.amazonaws.com/hospital-data`


(This assumed we've already setup an ECR repository called `hospital-data` and the AWS CLI is authenticated to the registry we are pushing to)

e.g.

Authenticating AWS CLI:

`aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com`

Returns login commands.

And setup repository called hospital-data:
`aws ecr create-repository \
    --repository-name hospital-data \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1`

