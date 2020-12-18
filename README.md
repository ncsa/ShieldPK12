# CUPHD-Health-Status-Tool
A tool for CUPHD to approve, isolate and quanrantine covid19 testers

### Structure
![img](CUPHD-Health-Status-Tool.png)

### Interface
![img](CUPHD-Health-Status-Tool_interface.png)

### Endpoint Description
| endpoint    | request          | response                                                                                  | description                                                           |
|-------------|------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| /login      | GET              | redirect to /callback by shibboleth                                                       |                                                                       |
| /logout     | GET              | redirect to {Shibboleth_endpoint}/idp/profile/Logout                                      |                                                                       |
| /callback   | GET              | redirect to / upon success login                                                          |                                                                       |
| /           | GET              | display interface                                                                         |                                                                       |
| /search     | POST {"uin":uin} | {"user":{"uin":uin, "given_name":given_name, "family_name":family_name, "status":status}} | get user information and status from PADA                             |
| /quarantine | POST {"uin":uin} | {"user":{"uin":uin, "given_name":given_name, "family_name":family_name, "status":status}} | update access status to False in PADA update quarantine status in QIR |
| /isolate    | POST {"uin":uin} | {"user":{"uin":uin, "given_name":given_name, "family_name":family_name, "status":status}} | update access status to False in PADA update isolate status in QIR    |
| /release    | POST {"uin":uin} | {"user":{"uin":uin, "given_name":given_name, "family_name":family_name, "status":status}} | update access status to True in PADA update release status in QIR     |
| /health     | GET              | {"message":"Healthy"} 