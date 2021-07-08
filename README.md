# SHIELD K to 12 Playbook

## How to Run

### For Local Development
- run`sh exec.sh`

### Remote Auto Redeploy
- ssh into the remote machine
- install `git`, `cron`, `docker` if not already exist. 
  - Following the instruction of https://docs.docker.com/engine/install/ubuntu/ to install docker.
  - Install docker-compose following: https://docs.docker.com/compose/install/
- clone this repository `git clone https://github.com/longshuicy/ShieldPK12.git`
- initialize ssl by run `sh init-letsencrypt.sh`
- test if the whole stack comes together by `docker-compose up`; to shut down, run `docker-compose down`  
- **run cronjob to automatically redploy if there is any change on the code repository**
  - placing `*/5 * * * * (cd /home/ubuntu/ShieldPK12 && sh redeploy.sh > redeploy.log)` into a text file, e.g. `job.txt`
  - then run command `crontab job.txt`. You can check if cronjob in place by `crontab -l`
  - Note you can change the which git branch to monitor by modifying the `BRANCH` variable in `redeploy.sh` script. 

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