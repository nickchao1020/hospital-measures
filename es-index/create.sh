#!/bin/bash
curl -X DELETE "localhost:9200/hospital-index"
curl -X PUT "localhost:9200/hospital-index"
curl -X PUT "localhost:9200/hospital-index/_mapping" -H 'Content-Type: application/json' -d @mapping.json
curl -X POST "localhost:9200/hospital-index/_bulk" -H 'Content-Type: application/x-ndjson' --data-binary @documents.json
