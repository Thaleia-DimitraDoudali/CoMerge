Author: *Pankaj Mistry -- pankajmistryin [at] gmail.com*

Emulation of Non Volatile Memory of variable bandwidth and latency, via thermal throttling. <br/>
Custom assigned values (trained dataset) to the corresponding PCI-based registers, for a dual socket Intel Xeon Platform.
```
python throttlectrl.py --help
Options:
  -h, --help          show this help message and exit
  -c CFG_FILE         Input/Output configuration file
  -i TRAINED_FILE     Input/Output configuration file
  -t DO_TRAIN         finds duty cycle for various scaling factors 1= needed,
                      0 = not needed [default: 0]
  -f THROTTLE_FACTOR  throttles the memory by this factor [default: -1]
  -n NODE_ID          throttles the memory on node nid [default: -1]
  -v VERBOSE          1 = show the current configuration on this platform
                      [default: 0]
  --verify=VERIFY     1 = verify and update the current platform parameters
                      [default: 0]
  -o TFNAME           1 = verify and update the current platform parameters
                      [default: ]
  --show=SHOW         1 = display current cached configuration [default: 0]
  --currbw=CBW        1 = show current bandwidth and scale factors applied to
                      each node [default: 0]
  --lspci=LSPCI       1 = show PCI ID's of throttling devices [default: 0]
```

