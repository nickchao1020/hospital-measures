from elasticsearch import Elasticsearch
import pandas as pd
import sys

from utils import get_counts

print('Connecting to elasticsearch...')
es = Elasticsearch(hosts='localhost:9200')

print('pulling state-measure counts...')
counts = get_counts(es)

print('Building plot...')
counts_df = pd.DataFrame([{'state': item['key']['state'],
                           'measure_id': item['key']['measure_id'],
                           'counts': item['doc_count']}
                          for item in counts])
plot_df = counts_df.pivot(index='state', columns='measure_id', values='counts')

plot = plot_df.plot.bar(stacked=True, figsize=(20, 20))

print('Saving plot to {}'.format(sys.argv[1]))
plot.get_figure().savefig(sys.argv[1])