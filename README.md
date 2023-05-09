# CS557 Final Project
#### William Scarbro

### Contents
This is a fork of <a href="https://github.com/noxrepo/pox">noxrepo/pox</a>. I have added/edited the following files

| File                      | Description                                  |
|---------------------------|----------------------------------------------|
| ./FinalProject.pdf              | Final Report                                 |
| pox/misc/MyTopology.py    | Translates POX topology to list adjacency    |
|                           | Implements throughput model                  |
| pox/misc/Dijkstras.py     | Shortest Path First (Entirely AI generated)  |
| pox/misc/MyTopoExample.py | Example interface with POX                   |
| pox/openflow/topology.py  | Minor changes to make compatible with MyTopo |


### To run
1. Download mininet VM (follow <a href="https://github.com/mininet/openflow-tutorial/wiki/Set-up-Virtual-Machine">tutorial</a> on setting up), subsequent steps in VM
2. Clone this repo <br> ``` git clone git@github.com:WilliamScarbro/pox.git```
3. Start POX <br> ``` ./pox/pox.py log.level --DEBUG topology openflow.topology openflow.discovery misc.MyTopoExample ```
4. (From anothe shell) start Mininet <br> ```sudo mn --mac --topo linear,3 --switch ovsk --controller remote```
5. Start ping traffic for host discovery in Mininet shell <br> ``` pingall ```
6. Throughput will be in POX logs, example <br> ``` DEBUG:misc.MyTopoExample:Throughput: 0.16666666666666666 ``` <br> (throughput will change as new hosts are detected)
