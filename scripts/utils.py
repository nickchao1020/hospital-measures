import pandas as pd
import json


def get_counts(es, index='hospital-index'):
    # results are paginated, so we need a while loop
    # after the initial search until we collect all the results.
    counts = []
    query = json.dumps({
        "aggs": {
            "buckets": {
                "composite": {
                    "sources": [
                        {
                            "state": {
                                "terms": {
                                    "field": "state"
                                }
                            }
                        },
                        {
                            "measure_id": {
                                "terms": {
                                    "field": "measure_id"
                                }
                            }
                        }
                    ]
                }
            }
        }
    })
    res = es.search(index=index, body=query)
    counts += res['aggregations']['buckets']['buckets']
    while 'after_key' in res['aggregations']['buckets']:
        after_key = res['aggregations']['buckets']['after_key']
        query = json.dumps({
            "aggs": {
                "buckets": {
                    "composite": {
                        "sources": [
                            {
                                "state": {
                                    "terms": {
                                        "field": "state"
                                    }
                                }
                            },
                            {
                                "measure_id": {
                                    "terms": {
                                        "field": "measure_id"
                                    }
                                }
                            }
                        ],
                        "after": after_key
                    }
                }
            }
        })
        res = es.search(index=index, body=query)
        counts += res['aggregations']['buckets']['buckets']
    return counts
