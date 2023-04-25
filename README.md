## Deploying the App

> Make sure your AWS account has the bucket earthdaily-deployments-pdx
```
aws cloudformation package \
--template-file infrastructure_template/template.yaml \
--output-template-file packaged.template \
--s3-bucket earthdaily-deployments-pdx
```

```bash
aws cloudformation deploy \
--template-file packaged.template \
--stack-name EarthdailyAtmStack \
--capabilities CAPABILITY_IAM
```

## Testing the App
Import the Api spec - `EarthdailyAtmStack-Prod-swagger-postman.json` into postman.
Alternatively make the curl requests to the public endpoint - https://utkynsmhz0.execute-api.us-west-2.amazonaws.com/Prod

## Overview of Application
AtmApplication is a simple service that stores the list of atms. Each atm can have 3 attributes - address, provider and rating. 
Additionally, each atm has a unique id and a "created_on" attribute. The service has the following apis - 
1. A POST api to create atms.
2. A GET api to query
3. A PUT api to update the attributes - address, provider and rating.

## High Level Architecture
ApiGateway -> Lambda -> DDB

Logs and metrics are outputted into Cloudwatch. Cloudformation is used to orchestrate the deployment.

Here is the justification for each component I used -
1. Cloudformation: So that we treat infrastructure as code.
2. ApiGateway: Easy to setup and will scale well to the project requirement of 2000 TPS (transaction per request). 
   Further, it provides a solution to throttle requests and add authZ/authN mechanisms. 
3. Lambda: Easy to setup and scales well to the project requirements of 2000 TPS. A new lambda instance will start-up in order of milliseconds.
4. DynamoDB: Easy to setup and scales well for the data quantity at hand.

How will the architecture evolve in the future?
1. More Models:
Currently, the app only has one model - Atm. As the number of models grow, the number of supporting objects such as Controllers, Repositories and Servioces will grow.  
Since we are initializing all the supporting objects ahead of handling the request, the lambda startup time will increase, which will increase the latency.
To maintain our latencies, we should migrate to ECS/Fargate or EC2, where the supporting objects can persist in-memory between requests. 

2. Higher Consistency
Depending on the nature of queries we may want to use SQL database. For example, if we need a GET to succeed 100% of the times on nely created item, we may want to move to a SQL that guarantees consistency. 

## Low Level Design
The executable code that runs in lambda has a 3-layerd structure as per the [CSR design pattern](https://tom-collings.medium.com/controller-service-repository-16e29a4684e5).
Actor -> Controller Layer -> Service Layer -> Repository layer -> DB

The invocation begins in the "atm_function.handler" method, which constructs the "Beans" and processes the request (i grew up in Java Land). 
The rest of the code is kept in a single file to keep deployment easy. 

Each class is tested using unittest.

How will the architecture evolve in the future?
As more models and supporting classes are added, the code will grow. To better manage it I would split the sile into smaller files amd deploy the code using docker.
Proposed directory structure -

```
EarthDailyHomeAssignment
+ function/
--+ models/
  --+ atm.py
  --+ <new_model>.py
--+ repository/            # Abstracts out the DB read/write apis
  --+ atm_repository.py
  --+ <other_repository>.py
--+ service/               # Business Logic
  --+ atm_service.py
  --+ <other_service>.py
--+ controller/            # Management of REST interface to the business logic
  --+ atm_controller.py
  --+ <other_controllers>.py
--+ handler.py             # Entry point
+ infrastructure_temple
...

```

