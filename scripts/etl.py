import pandas as pd
import numpy as np
import json
import sys

SOURCE_DATA_FP = sys.argv[1]

print('Reading datafile...')
hospital_df = pd.read_csv(SOURCE_DATA_FP)

hospital_df.columns = ['facility_id', 'facility_name', 'address',
                       'city', 'state', 'zip', 'county', 'phone_number',
                       'measure_id', 'measure_name', 'compared_to_national',
                       'score', 'footnote', 'start_date', 'end_date']

hospital_df = hospital_df.fillna('null')
hospital_dict = hospital_df.to_dict('records')

ES_DATA_FP = '../es-index/documents.json'
with open(ES_DATA_FP, 'w') as f:
    for i, item in enumerate(hospital_dict):
        # remove missing scores
        if item['score'] in ['Not Available', '--']:
            item.pop('score')
        head = {"create": {"_index": "hospital-index"}}
        doc = '{}\n{}\n'.format(json.dumps(head), json.dumps(item))
        f.write(doc)
    f.write('\n')