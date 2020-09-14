import glob
import pandas as pd
from time import time


# start = time()
# df = pd.read_csv('asd.csv')
# print(time()-start)

# start = time()
# df = pd.read_csv('asd_comp.csv', compression = 'gzip')
# print(time()-start)

start = time()
df = pd.read_feather('asd.ftr')
print(time()-start)

start = time()
df = pd.read_hdf('asd.h5', key='table')
print(time()-start)

start = time()
df = pd.read_parquet('asd.parquet')
print(time()-start)