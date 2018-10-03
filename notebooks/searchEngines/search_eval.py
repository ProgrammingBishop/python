import math
import sys
import time

import metapy
import pytoml

class InL2Ranker(metapy.index.RankingFunction):
    def __init__(self, some_param = 1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        inner = 1 + ( sd.avg_dl / sd.doc_size )
        tfn   = sd.doc_term_count * math.log( inner, 2 )
        inner = ( sd.num_docs + 1 ) / ( sd.corpus_term_count + 0.5 )
        score = sd.query_term_weight * ( tfn / ( tfn + self.param ) ) * math.log( inner, 2 )
        
        # return (self.param + sd.doc_term_count) / (self.param * sd.doc_unique_terms + sd.doc_size)
        return score


def load_ranker(cfg_file):
    return metapy.index.OkapiBM25(k1 = 1.2, b = 0.75, k3 = 500)
    #return InL2Ranker(some_param = 0.5) 


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
            print("Query {} average precision: {}".format(query_num + 1, avg_p))
    print("Mean average precision: {}".format(ev.map()))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
