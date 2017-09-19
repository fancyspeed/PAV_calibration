#coding: utf-8
#author: zuotao.liu@gmail.com 
#description: Pool-adjacent-violators (PAV) Algorithm
import math

max_bin_num = 1000
min_bin_imp = 50000
min_bin_clk = 50
min_bin_step = 0.00001


def get_train_pairs(p_truth, p_pred):
    pairs = []
    with open(p_truth) as fin:
        for line in open(p_pred):
            pred_ctr = float(line.split(' ')[0].strip())
            true_clk = float(fin.readline().split(' ')[0].strip())
            pairs.append( (pred_ctr, true_clk) )
    return pairs 


def get_parts(train_pairs):
    sort_list = sorted(train_pairs, key=lambda d:d[0])
    step = len(sort_list) / max_bin_num
    v_list = [] # start, end, ctr, imp, clk

    for i in range(max_bin_num):
        if i == max_bin_num-1: part = sort_list[step*i:]
        else:                  part = sort_list[step*i:step*(i+1)]
        start, end, imp, clk = part[0][0], part[-1][0], len(part), sum([v for k, v in part])

        if v_list and (start < v_list[-1][0] + min_bin_step or (v_list[-1][3] < min_bin_imp and v_list[-1][4] < min_bin_clk)):
            new_imp = v_list[-1][3] + imp 
            new_clk = v_list[-1][4] + clk
            new_ctr = new_clk / float(new_imp) 
            v_list[-1] = [v_list[-1][0], end, new_ctr, new_imp, new_clk]
        else:
            ctr = clk / float(imp)
            v_list.append([start, end, ctr, imp, clk])
    return v_list


def train(v_list, p_out):
    i = 0
    while i < len(v_list) - 1:
        j = len(v_list) - 1
        while j > i:
            avg_ctr = sum([v_list[k][2] for k in range(i,j+1)]) / (j+1-i)
            if avg_ctr <= v_list[i][2]:
                # 1. if avg(nexts) < i; do something
                min_ctr, min_j = avg_ctr, j
                j2 = i + 1
                while j2 <= j: 
                    avg_ctr = sum([v_list[k][2] for k in range(i,j2+1)]) / (j2+1-i)
                    if avg_ctr < min_ctr:
                        min_ctr, min_j = avg_ctr, j2
                    j2 += 1
                # 2. find min_ctr, and replace
                for k in range(i, min_j+1):
                    v_list[k][2] = min_ctr
                break 
            j -= 1
        # 3. if no avg(nexts) < i; do nothing
        i += 1
    with open(p_out, 'w') as fo:
        for start, end, ctr, imp in v_list:
            fo.write('%s\t%s\n' % (end, ctr))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print '<usage> truth pred out_dict'
        exit(1)

    train_pairs = get_train_pairs(sys.argv[1], sys.argv[2])
    parts = get_parts(train_pairs)
    train(parts, sys.argv[3])


