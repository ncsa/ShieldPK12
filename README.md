# SHIELD K to 12 Playbook

## How to Run

### For local development
- run`sh exec.sh`

### For deployment
#### Deploy with ssl
- `ssh` into your remote machine
- Make suer you already install `git`, `cron`, `docker`: 
  - Following the instruction of https://docs.docker.com/engine/install/ubuntu/ to install docker.
  - Install docker-compose following: https://docs.docker.com/compose/install/
- `git clone` this repository `git clone https://github.com/longshuicy/ShieldPK12.git`
- Initialize SSL certificate by run `sh init-letsencrypt.sh`, please change the domain name to ones that you 
  own. Right now this domain is pointing towards `shield-k12-playbook.ncsa.illinois.edu`. Check [init-letsencrypt.
  sh](init-letsencrypt.sh) for more details.
- To see if the whole stack comes together by running command `docker-compose up`
- To shut down the running app, run command `docker-compose down`  
- **Important note:** you can run cronjob to automatically redploy if there is any change on the code repository. 
  To do so, follows the below steps:
    - Change which git branch to monitor by modifying the `BRANCH` variable in [redeploy.sh](redeploy.sh) script. 
      - E.g. point to the current branch: `BRANCH=$(git branch --show-current)`
      - E.g. point to the master branch `BRANCH=master`
    - Place `*/5 * * * * (cd /home/ubuntu/ShieldPK12 && sh redeploy.sh > redeploy.log)` into a text file, e.g. 
      `job.txt`
    - Then run command `crontab job.txt`. You can check if cronjob in place by `crontab -l`
  
#### Deploy without SSL
In case you do not own a domain name yet, or just want to deploy a test/develop version of the app, you can deploy 
without SSL: Run command `docker-compose -f docker-compose_wo_ssl.yml up --build -d`. Then you can access the 
web app at `http://{hostIP}`. See the custom docker compose file [docker-compose_wo_ssl.yml](docker-compose_wo_ssl.yml)
for more details.

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