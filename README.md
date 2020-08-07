# Usage

First, pull an elasticsearch docker image from the Elastic Docker Registry registry\
`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.8.1`
\

Now that we have an elasticsearch docker image, we can run it with:\

`docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.8.1`
