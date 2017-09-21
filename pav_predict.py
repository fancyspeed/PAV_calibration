import math

def load_pav_dict(p_in):
    pav_dict = [(0, 0)] 
    for line in open(p_in):
        end, ctr = line.strip().split('\t')
        pav_dict.append( (float(end), float(ctr)) )
    pav_dict.append( (1, pav_dict[-1][1]) )
    return pav_dict

def pav_adjust(y, pav_dict):
    y_new = -1 
    for i, pair in enumerate(pav_list):
        if i == len(pav_list)-2 or y <= pav_list[i+1][0]:
            ratio = (y - pair[0]) / (pav_list[i+1][0] - pair[0])
            y_new = pair[1] + ratio * (pav_list[i+1][1] - pair[1]) 
            break
    return y_new


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print '<usage> out in pav_dict'
        exit(1)
    
    pav_list = load_pav_dict(sys.argv[3])
    
    with open(sys.argv[1], 'w') as fo:
        for line in open(sys.argv[2]):
            y = float(line.split(' ')[0].strip())
            y_new = pav_adjust(y, pav_list)
            fo.write('%s\n' % y_new)

