import sys
from os import listdir
import numpy as np

# merging all component .csv files to train, test .csv files
def mergingAll(names, tr_path, cv_path, save_path, shuffle=True):
    paths = [(tr_path, '_tr.csv'), (cv_path, '_cv.csv')]
    for path, ending in paths:
        X = None
        for i, name in enumerate(names):
            # print progress
            sys.stdout.write('\r')
            formatted_names = '{:.2%}'.format(i/len(names))
            sys.stdout.write(formatted_names)
            sys.stdout.flush()

            curr = np.loadtxt(path + name + ending, delimiter=',')
            if X is None:
                X = curr.copy()
                continue
            X = np.vstack([X, curr])
        sys.stdout.write('\r100.00%\n')

        # shuffle
        if shuffle:
            np.random.shuffle(X)
        np.savetxt(save_path + 'all' + ending, X, delimiter=',', fmt='%i')