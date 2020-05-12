import numpy as np
import time

start_time = time.time()

a=np.array([1])
st_time = time.time() - start_time
a=np.append(a,[2])
a_time = time.time()- st_time

a[1]=3
b_time = time.time()- a_time

replace=1000*(b_time - a_time)
app=1000*(a_time - st_time)

print(a_time,b_time,st_time)