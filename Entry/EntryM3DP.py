import numpy as np
import pickle

import Model.Model3DQNFixCount as model
import Model.Model3DQNFixStorage as model2
import Utility.PostgreSQL as pg


def One_Run_DQN(is_fixcount, conf, __x, is_dnn, is_ps, is_double, a, workload_file, candidate_file):
    conf['NAME'] = 'MA_9' + str(__x)
    print('=====load workload=====')
    wf = open(workload_file, 'rb')
    workload = pickle.load(wf)
    print('=====load candidate =====')
    cf = open(candidate_file, 'rb')
    index_candidates = pickle.load(cf)
    if is_fixcount:
        agent = model.DQN(workload[:], index_candidates, 'hypo', conf, is_dnn, is_ps, is_double, a)
        _indexes = agent.train(False, __x)
        indexes = []
        for _i, _idx in enumerate(_indexes):
            if _idx == 1.0:
                indexes.append(index_candidates[_i])
        return indexes
    else:
        agent = model2.DQN(workload, index_candidates, 'hypo', conf)
        _indexes, storages = agent.train(False, __x)
        indexes = []
        for _i, _idx in enumerate(_indexes):
            if _idx == 1.0:
                indexes.append(index_candidates[_i])
        return indexes


def get_perf(f_indexes, _frequencies, workload_file):
    # _frequencies = [1659, 1301, 1190, 1741, 1688, 1242, 1999, 1808, 1433, 1083, 1796, 1266, 1046, 1353]
    frequencies = np.array(_frequencies) / np.array(_frequencies).sum()
    wf = open(workload_file, 'rb')
    workload = pickle.load(wf)
    pg_client = pg.PGHypo()
    pg_client.delete_indexes()
    cost1 = (np.array(pg_client.get_queries_cost(workload)) * frequencies).sum()
    print(cost1)
    for f_index in f_indexes:
        pg_client.execute_create_hypo(f_index)
    cost2 = (np.array(pg_client.get_queries_cost(workload)) * frequencies).sum()
    print(cost2)
    pg_client.delete_indexes()
    print((cost1 - cost2) / cost1)
    return (cost1 - cost2) / cost1


conf21 = {'LR': 0.002, 'EPISILO': 0.97, 'Q_ITERATION': 200, 'U_ITERATION': 5, 'BATCH_SIZE': 64, 'GAMMA': 0.95,
          'EPISODES': 800, 'LEARNING_START': 1000, 'MEMORY_CAPACITY': 20000}

conf = {'LR': 0.1, 'EPISILO': 0.9, 'Q_ITERATION': 9, 'U_ITERATION': 3, 'BATCH_SIZE': 8, 'GAMMA': 0.9,
        'EPISODES': 800, 'LEARNING_START': 400, 'MEMORY_CAPACITY': 2000}


# is_fixcount == True, constraint is the index number
# is_fixcount == False, constraint is the index storage unit
def entry(is_fixcount, constraint, workload_file, candidate_file):
    if is_fixcount:
        return One_Run_DQN(is_fixcount, conf21, constraint, False, True, True, 0, workload_file, candidate_file)
    else:
        return One_Run_DQN(is_fixcount, conf, constraint, False, False, False, 0, workload_file, candidate_file)


fix_count_freq = [1659, 1301, 1190, 1741, 1688, 1242, 1999, 1808, 1433, 1083, 1796, 1266, 1046, 1353]
fix_storage_freq = [1659, 1301, 1190, 1741, 1688, 1242, 1999, 1808, 1433, 1083, 1796, 1266, 1046, 1353]

def log(x):
    with open("test.txt", "a") as myfile:
        myfile.write(x)

for n in range(2, 12):
    print("----------------------------")
    print("Workload 14 - Candidate 14 C")
    print("----------------------------")
    indexes = entry(True, n, 'Entry/workload_14.pickle', 'Entry/candidate_14_c.pickle')
    print(indexes)
    reward = get_perf(indexes, fix_count_freq, 'Entry/workload_14.pickle')
    log(reward)

for n in range(2, 12):
    print("----------------------------")
    print("Workload 14 - Candidate 14 S")
    print("----------------------------")
    indexes = entry(True, n, 'Entry/workload_14.pickle', 'Entry/candidate_14_s.pickle')
    print(indexes)
    reward = get_perf(indexes, fix_count_freq, 'Entry/workload_14.pickle')
    log(reward)

for n in range(3, 9):
    print("----------------------------")
    print("Workload 14 - Candidate2 14 C")
    print("----------------------------")
    indexes = entry(True, n, 'Entry/workload_14.pickle', 'Entry/candidate2_14_c.pickle')
    print(indexes)
    reward = get_perf(indexes, fix_count_freq, 'Entry/workload_14.pickle')
    log(reward)

for n in range(3, 9):
    print("----------------------------")
    print("Storage - Workload 14 - Candidate2 14 C")
    print("----------------------------")
    indexes = entry(False, n, 'Entry/workload_14.pickle', 'Entry/candidate2_14_c.pickle')
    print(indexes)
    reward = get_perf(indexes, fix_storage_freq, 'Entry/workload_14.pickle')
    log(reward)

for n in range(2, 12):
    print("----------------------------")
    print("Workload 50 - Candidate2 14 C")
    print("----------------------------")
    indexes = entry(True, n, 'Entry/workload1_50.pickle', 'Entry/candidate1_14_c.pickle')
    print(indexes)
    reward = get_perf(indexes, fix_count_freq, 'Entry/workload1_50.pickle')
    log(reward) 
