import datetime
from qiling import *
from qiling.const import *
from qiling.os.const import *
from matplotlib import cm
import matplotlib.pyplot as plt

import numpy as np
from malloc_call import malloc_call

import time



allocation_calls = []
my_time = -1


# Blocul de memorie catre care pointeaza functia malloc
def get_dimension(ql):
    # dimensiunea care trebuie alocata
    dim = ql.os.resolve_fcall_params({'dimension': int})
    allocation_calls.append(malloc_call(dim['dimension'], time.time() - my_time))
    return dim['dimension']


# Functia returneaza addresa unde s-a facut alocarea
def get_addr(ql):
    addr = ql.reg.read("RAX")
    allocation_calls[-1].addr = addr
    if (addr != 0):
        return addr

# Functia returneaza adresa care urmeaza a fi eliberata, iar aceasta coincide cu adresa la care s-a facut alocarea
def free(ql):
    prev_addr = get_addr(ql)
    n = len(allocation_calls)
    i = 0
    while i < n:
        if (allocation_calls[i].addr == prev_addr):
            allocation_calls[i].end_allocation_time = time.time() - my_time
        i +=1 
    return prev_addr


time_axis = 1200
memory_axis = 800

def plotting(vector: malloc_call):
    start_time = vector[0].allocation_time
    end_time = vector[0].end_allocation_time
    start_mem = vector[0].addr
    end_mem = vector[0].addr + vector[0].dimension
    allocated_mem = 0

    i = 0
    n = len(vector)
    
    while i < n:
        start_time = min(start_time, vector[i].allocation_time)
        end_time = max(end_time, vector[i].end_allocation_time)
        start_mem = min(start_mem, vector[i].addr)
        end_mem = max(end_mem, vector[i].addr + vector[i].dimension)
        allocated_mem = max(allocated_mem, vector[i].dimension)
        i += 1
    
    diff_time = (end_time - start_time) / time_axis
    diff_mem = (end_mem - start_mem) / memory_axis

    # Se pun punctele pe axa
    vector_plot = np.zeros((memory_axis, time_axis))     

    poz_mem = [0]
    mapped_mem = [start_mem]
    poz_time = [0]
    mapped_time = [start_time]

    for i in range(len(vector)):   # plotam fiecare obiect de tip malloc_call
        aux = (vector[i].addr - start_mem) / diff_mem                                                                 
        begin_mem  = int(np.floor(aux)) 
        poz_mem.append(begin_mem)
        mapped_mem.append(vector[i].addr)
        aux1 = (vector[i].addr + vector[i].dimension - start_mem) / diff_mem
        last_mem  = int(np.floor(aux1)) 
        poz_mem.append(last_mem)
        mapped_mem.append((vector[i].addr + vector[i].dimension))

        aux2 = (vector[i].allocation_time - start_time) / diff_time
        begin_time = int(np.floor(aux2))
        poz_time.append(begin_time)
        mapped_time.append(vector[i].allocation_time)
        aux3 = (vector[i].end_allocation_time - start_time) / diff_time
        last_time = int(np.floor(aux3))
        poz_time.append(last_time)
        mapped_time.append(vector[i].end_allocation_time)

        
        time_allocation = vector[i].end_allocation_time - vector[i].allocation_time
        print("Timpul cat a fost alocat obiectul", i)
        print("\t", time_allocation)
        print("\n")
        memory_for_each_elem = (vector[i].addr + vector[i].dimension) - vector[i].addr
        print("Numarul de biti ocupati in memorie pentru obiectul", i)
        print("\t", memory_for_each_elem)
        print("\n")

        vector_plot[begin_mem : last_mem, begin_time : last_time] = (vector[i].dimension / allocated_mem)

    my_colors = cm.get_cmap('magma')
    my_colors.colors[0] = [1.0, 0.1, 0.1]

    plt.figure(figsize=(13, 8))
    plt.imshow(vector_plot, cmap=my_colors)
    plt.xticks(poz_time, mapped_time)
    plt.yticks(poz_mem, mapped_mem)
    plt.xlabel("Time")
    plt.ylabel("Memory")
    plt.show()



def start_qilling(path, rootfs):
    ql = Qiling(path, rootfs, verbose=QL_VERBOSE.OFF)

    ql.set_api('malloc', get_dimension, QL_INTERCEPT.ENTER)
    ql.set_api('malloc', get_addr, QL_INTERCEPT.EXIT)
    ql.set_api('free', free)

    ql.run()

    plotting(allocation_calls)
    

if __name__ == "__main__":
    print("Rularea a inceput, te rog asteapta!!!\n")
    start_qilling(["a.out"], "rootfs/x8664_linux")