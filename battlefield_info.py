possible = []
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
l_to_n = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
n_to_l = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}

for i in letters:
    for j in range(8):
        possible.append(f'{i}{j}')


