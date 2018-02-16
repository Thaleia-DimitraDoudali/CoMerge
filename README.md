# CoMerge
Experimental setup for exploration of efficient data placement in shared heterogeneous memory systems.

## Hybrid Memory System Emulation
Scripts in `throttle/`

## Overall Application Sensitivity
`run_all_throttle.sh` in the individual application subfolders, to see the overall application performance across different combinations of bandwidth and latency NVM emulation.

## Data Structure Sensitivity
Needs custom modification of 1 line of code in each source code file. The line refers to the choice of memory node for the allocation of the data object, and is clearly marked.

## Collocation Analysis
For specific data tierings and NVM emulation, implemented as stated in the two previous steps, run in parallel the desired applications, multiple times. 

### Experimental raw data
In folder `data/`

### Reference

For further detail and experimental result analysis refer to:

*Thaleia Dimitra Doudali and Ada Gavrilovska. 2017. CoMerge: Toward Efficient Data Placement in Shared Heterogeneous Memory Systems. In Proceedings of MEMSYS 2017, Alexandria, VA, USA, October 2–5, 2017, 11 pages.*
