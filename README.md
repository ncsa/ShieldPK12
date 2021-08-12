# SHIELD K-12 Playbook

## How to Run

### For local development
- run`sh exec.sh`

### For deployment
#### Deploy with domain name and SSL
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
In case you do not own a domain name yet, or just want to deploy the test/develop version of the app, you can deploy 
without SSL: Run command `docker-compose -f docker-compose_wo_ssl.yml up --build -d`. Then you can access the 
web app at `http://{hostIP}`. See the custom docker compose file [docker-compose_wo_ssl.yml](docker-compose_wo_ssl.yml)
for more details.

## How to add new module

### Write a new module
#### Format explanation
Modules are written in JSON (JavaScript Object Notation) format, which is a lightweight data-interchange format. It is 
easy for humans to read and write. It is easy for machines to parse and generate. [Read more...](https://www.json.org/json-en.html)

We define a few fields that this playbook app recognizes and automatically populates. If you need to add content 
beyond the pre-defined fields, you would also need to modify the existing app code, or add additional code to parse 
and consume those.

Here is an example of the module template. You can find the same content here [decision_template.json](doc/decision_template.json). 
You can also see how other modules were written under the [decisiontrees](decisiontrees) folder.
```angular2html
{
  "moduleName": "",
  "moduleDescription": "",
  "prettyModuleName": "",
  "moduleContent": [
    {
      "rules": {
        "operator": "AND",
        "criteria": [
          {
            "AID": ""
          }
        ]
      },
      "QID": "",
      "question": "",
      "description": "",
      "answers": [
        {
          "AID": "",
          "prettyAID": "",
          "answer": "",
          "description": "",
          "nextQID": ""
        },
        ...,
        ...
      ]
    },
    ...
  ],
  "checklist": [
    {
      "activityID": "",
      "activity": "",
      "links": [],
      "rules": {
        "operator": "OR|AND|NOT|ALL",
        "criteria": [
          {
            "AID": ""
          },
          ...
        ]
      }
    },
    ...
  ]
}
```

- **moduleName** will reflect on the URL of that module. No space is allowed on this field. For example, 
  `"moduleName": "special-education"` will link the cleaning module to  `https://{your domain name}
  /special-education/questions`
- **prettyModuleName** is the pretty name for a module where space and other special characters are allowed. For 
  example, `"prettyModuleName":"special education"`
  ![img.png](doc/moduleName.png)
- **moduleDescription**: a short paragraph of module description will be reflected on the module cards located 
  at the landing page. ![moduleDescription.png](doc/moduleDescription.png)
--------------------------------  
- **moduleContent** contains a list of Q&A items. Each item is one screen:  
```angular2html
{
      "QID": "",
      "question": "",
      "description": "",
      "answers": [
        ...
        ...
        ...
      ]
    },
```
- **QID** is the unique question ID that the app uses internally to track the dependencies and progress of Q&As
- **question** will be displayed on the left of the screen
- **description**: short description of the question will be displayed below the question. HTML tag is allowed, e.g.
  `<a>` tag for links
- **answers**: contains a list of options as answers of the question:
```angular2html
    "answers": [
        {
          "AID": "",
          "prettyAID": "",
          "answer": "",
          "description": "",
          "nextQID": ""
        },
        ...
    ]
```
- **AID** is the unique answer ID that the app uses internally to track the dependencies and progress of Q&As
- **prettyAID** is the prettified answer ID (usually we use "a, b, c, ...", but you could use "1, 2, 3, ...", or "i,
  ii, iii,..")
- **answer** is the content of answer that will be displayed on the right of the screen as selectable options
- **description*** is the description of the answer 
- **nextQID** is the ID of the next question that you want to point user toward upon selection. **It is very 
  important that you put down the a valid existing QID, otherwise it may cause malfunction of the app. If you 
  reach the end of your module (last question), then simply put `null` as the nextQID.**
![img.png](doc/moduleContent.png)  


The skip/display for some questions may depend on previous answers.

For example: Only when use answer "surface cleaning supplies" for the question "What supplies will you have for 
cleaning", they will be prompted to answer "What surface cleaning supplies will you have". You can use the **rules** field to set up those conditions:
```angular2html

      "rules": {
        "operator": "AND",
        "criteria": [
          {
            "AID": ""
          }
        ]
      },
```
- **operator**: You can put down `OR`, `AND`, or `NOT`. This is the logic operator to determine if *any*, *all*, or 
  *none* of the criteria need to be matched in order to display this Q&A.
- **criteria**: a list of answer IDs to match
- **AID**: valid, existing answer ID

To help you understand, here is an example in [cleaning module](decisiontrees/cleaning_decision.json):
```angular2html
{
      "QID": "2",
      "question": "What supplies will you have for cleaning",
      "multiple": true,
      "description": "Cleaning resources should...",
      "resources": [],
      "answers": [
        {
          "AID": "2a",
          "prettyAID": "a",
          "answer": "Surface cleaning supplies",
          "description": "",
          "resources": [],
          "nextQID": "2a-i"
        },
        {
          "AID": "2b",
          "prettyAID": "b",
          "answer": "Air Filters",
          "description": "See the <a href='/ventilation/questions'>ventilation...",
          "resources": [],
          "nextQID": "3"
        }
      ]
    },
```

If a user chooses `AID = 2a` as the answer, the following Q&A screen will be displayed:
```angular2html
{
      "QID": "2a-i",
      "question": "What surface cleaning supplies will you have",
      "multiple": true,
      "rules": {
        "operator": "AND",
        "criteria": [
          {
            "AID": "2a"
          }
        ]
      },
      "description": "",
      "resources": [],
      "answers": [
        ...
        ...
      ]
    },
```
Otherwise, this question "2a-i" will be skipped.

--------------------------------  
- **checklist** contains a list of action items that will be displayed once the user finish each module
```angular2html
"checklist": [
    {
      "activityID": "",
      "activity": "",
      "links": [],
      "rules": {
        "operator": "OR|AND|NOT|ALL",
        "criteria": [
          {
            "AID": ""
          },
          ...
        ]
      }
    },
    ...
  ]
```
- **activityID**: unique ID of action item the app uses internally
- **activity**: name of the checklist action item. e.g. "Signs next to all cleaning supplies to remind cleaners about 
  hand washing and not touching their face"
- **links**: URLs pointing towards supporting documents
- **rules** constains a list of rules that determine under what condition a checklist action item will be needed.
```angular2html
    "rules": {
        "operator": "OR|AND|NOT|ALL",
        "criteria": [
          {
            "AID": ""
          },
          ...
        ]
      }
```
- **operator**: allowed boolean operator includes "OR", "AND", "NOT", and "ALL", which indicates "any", "all" or 
  "none" of the answer ID should appear in user's answers. Note that when you put down "ALL", you do not need to 
  list any specific "AID", as it means this checklist item will always be present
  e.g: the below snippet of text means, if a user choose ""1a-iv-2"" or "1b-i-2-b-ii" as answer, then this action 
  item "Process for validating vaccine..." will be presented in the checklist.
  ```
      "activityID": "7",
      "activity": "Process for validating vaccine status through the state system",
      "links": [
        "https://www.cdc.gov/vaccines/programs/iis/contacts-locate-records.html#state"
      ],
      "rules": {
        "operator": "OR",
        "criteria": [
          {
            "AID": "1a-iv-2"
          },
          {
            "AID": "1b-i-2-b-ii"
          }
        ]
      }
  ```
- **cretieria** constains a list of answer IDs
- **AID**: valid, existing answer ID. Please refer to the explanation in `"moduleContent" -> "answers" -> "AID"`
![img.png](doc/checklists.png)

### Integrate the new module into the app
- Once you have your new module file `{your new module}.json`, simply place it under the [/decisiontrees](/decisiontrees) folder.
- Restart the app following section **How to Run**