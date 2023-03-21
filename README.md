# Visualization-of-Dynamic-Memory-Allocations
A simple project using Python and Qiling Framework for graphical representation of malloc() and free() functions. There is support for Linux.


***Get the following resources before getting the project:***

    1. Qilling: git clone https://github.com/qilingframework/qiling.git
    2. rootfs: git clone https://github.com/qilingframework/rootfs.git, go to rootfs directory, only the x8664_linux directory is kept.
    
**Get the following resources for running:**

    1. git clone https://github.com/marinvanessa/Visualization-of-Dynamic-Memory-Allocations.git
    2. cd to the /followmallocfreecalls directory
    3. code . (open in VSCode)
    4. chmod +x resources.sh
    5. sudo ./resources.sh


**Execution:**

    Use the following commands in linux terminal:
        1. gcc follow_allocation.c
        2. python3 main.py
    Another way is using the following commands:
        1. chmod +x start.sh
        2. ./start.sh


**Result:**

![result](Visualization-of-Dynamic-Memory-Allocations/VisualizationOfDynamicMemoryAllocations/result/ "Result")

