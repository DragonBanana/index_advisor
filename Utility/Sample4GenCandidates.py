import pickle
import psqlparse
from Preprocess import Dataset as ds
from Utility import Encoding as en
from Utility import ParserForIndex as pi

enc = en.encoding_schema()
# path to your tpch_directory/dbgen
work_dir = "tpc-h"
w_size = 50
wd_generator = ds.TPCH(work_dir, w_size)
workload = wd_generator.gen_workloads()
print(f'wd_generator {wd_generator}, workdir {work_dir}, workload {workload}')
parser = pi.Parser(enc['attr'])

with open('workload' + str(w_size) + '.pickle', 'wb') as df:
    pickle.dump(workload, df, protocol=0)


def gen_i(__x):
    added_i = set()
    for i in range(len(workload)):
        if i > __x:
            continue
        print(f'\n\n\n\n\nparse dict {workload[i]}\n\n\n\n')

        b = psqlparse.parse_dict(workload[i])
        print(f'parsing {b} with {workload[i]}')
        parser.parse_stmt(b[0])
        parser.gain_candidates()
        if i == 8:
            added_i.add('lineitem#l_shipmode')
            added_i.add('lineitem#l_orderkey,l_shipmode')
            added_i.add('lineitem#l_shipmode,l_orderkey')

    f_i = parser.index_candidates | added_i
    f_i = list(f_i)
    f_i.sort()
    with open('candidate' + str(__x + 1) + '_c.pickle', 'wb') as df:
        pickle.dump(list(f_i), df, protocol=0)

    temp = [x for x in f_i if len(x.split(",")) == 1]
    with open('candidate' + str(__x + 1) + '_s.pickle', 'wb') as df:
        pickle.dump(list(temp), df, protocol=0)

    temp = [x for x in f_i if x.split("#")[0] == "orders" or x.split("#")[0] == 'lineitem']
    with open('candidate2_' + str(__x + 1) + '_c.pickle', 'wb') as df:
        pickle.dump(list(temp), df, protocol=0)

    temp = [x for x in f_i if x.split("#")[0] == 'lineitem']
    with open('candidate1_' + str(__x + 1) + '_c.pickle', 'wb') as df:
        pickle.dump(list(temp), df, protocol=0)


# for i in range(0, w_size):
gen_i(14)
