# SHIELD K to 12 Playbook

## How to Run

### For Local Development
- run`sh exec.sh`

### Remote Auto Redeploy
- ssh into the remote machine
- clone this repository `git clone https://github.com/longshuicy/ShieldPK12.git`
- run cronjob `*/5 * * * * (cd /home/ubuntu/ShieldPK12 && sh redeploy.sh > redeploy.log)`. Note you can change the 
  Git branch by modifying the `BRANCH` variable in `redeploy.sh` script

## Decision Tree Structure
### Cleaning Decision
![image](test/cleaning_decision_graph.png)

### Distancing Decision
![image](test/distancing_decision_graph.png)

### IT Decision
- TBD

### Mask Decision
![image](test/mask_decision_graph.png)

### Testing Decision
![image](test/testing_decision_graph.png)

### Ventilation Decision
![image](test/ventilation_decision_graph.png)