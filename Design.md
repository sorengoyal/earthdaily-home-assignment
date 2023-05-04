## Requirements
1. Develop a simple RESTful API (using a language of choice) that interacts with a backend DB.
	- Decisions:
		- Language: Python
	 	- Backend DB: DyanmodDb
2. API shall have one endpoint supporting a POST, PUT and GET method.
 	- Decisions:
 		- Endpoint Name: https://utkynsmhz0.execute-api.us-west-2.amazonaws.com/Prod
 		- APIs:
 			- GET  /atm/<id>/
 			- POST /atm/ {<body>}
 			- PUT /atm/<id>/ {<body>}
 3. The object being created shall contain a mixture of primitive attributes(date/time, string, 
int, float, Boolean, etc) to support REST API's query capability	
	- Decisions: 
		- API for query: GET /atm/?<field>=<value>
		- DB Schema for ATM:
			[id: uuid, address: string, provider: string, rating: float, created_on: datetime, geometery(optional)]
4. Assume that the RESTful API is expected to handle an average load of 1000 QPS POST+PUT and 2000 QPS GETs.
	- Decisions:
		- Used Lambda to scale up elastically, 
		- Read/Write quota of the DB will have to be increased, 
5. This traffic may spike up to 2000 POST or PUT request and 4000 GET request per second.
	- Decisions:
		- Apigateway+Lambda+DynamoDB can handle 2000 TPS.
        - The current configuration is as follows - 
          - API Gateway is configured to allow 1000 rate + 2000 burst
          - Lambda's max concurrent executions has been set to 400 ( can be increased to 2000 by paying money)
          - DynamoDB's read/write capacity is at 5. (can be increased to 2000 by paying more money).
6. The RESTful API should also respect the order of creation as in the PUT request should properly be handled after the corresponding POST request.
	- Decisions: We perform PUT only when the object is available, if not, we returna error.
7. [BONUS] use an object with spatial data type like bounding box, binary geometry, geojson or similar. Please demonstrate how to read and write 
chosen spatial data type from the API.
	- Skipped as part of this project
8. [BONUS] Our entire system runs fully in AWS and your AWS experience is very relevant to the position. Please develop and deploy the above RESTful API within AWS using the AWS services of your choice.
	- Decision: Using the stack - Cloudformation, ApiGateway, Lambda, DynamoDB

## Submission Requirements
1. Please have all your code, tests, scripts, docs (anything you feel is required to support follow on questions during the next interview) available 
in a git-based repository and make this available for EarthDaily Analytics to review prior to the next interview
	- Link to Git repo: https://github.com/sorengoyal/earthdaily-home-assignment
2. Please have this exercise in a working state such that it can be demo-ed during the interview itself
	- Link to AWS Endpoint: https://utkynsmhz0.execute-api.us-west-2.amazonaws.com/Prod
3. Timebox effort to 4 hrs + 2hrs
	- Actual spent: 16 hrs
	  - 9 hrs on AWS setup
      - 5 hrs the code
      - 2 hr on doc 


## Assumptions
#### Regarding API
1. Rating has no limit and is provided by application administrator.
2. APIs are called by a client that is aware of ATM IDs.
   1. Therefore, it is ok for the atm id to not be human-readable.
3. The volume of PUT requests is not very high, so we do need to handle the case of ordering the PUT requests. 


#### Regarding Performance
1. Latency SLA for each request is  < 1s.
   1. Assumption helped me avoid the problem of lambda cold start.

#### Regarding Deployment
1. Code is small, so deploying with a single file is ok.
   1. Larger code bases can be packed into a docker image or zip file and then deployed to lambda.


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

2. Support for Geospatial Datatypes
Postgres and DocumentDB provide features to index geospatial datatypes.
[How are coordinates indexed](https://towardsdatascience.com/geospatial-index-101-df2c011da04b)

## Low Level Design
The executable code that runs in lambda has a 3-layerd structure as per the [CSR design pattern](https://tom-collings.medium.com/controller-service-repository-16e29a4684e5).
Actor -> Controller Layer -> Service Layer -> Repository layer -> DB

The invocation begins in the "atm_function.handler" method, which constructs the "Beans" and processes the request (i grew up in Java Land). 
The rest of the code is kept in a single file to keep deployment easy. 


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

### Future Work
#### APIs
1. Add a LIST api to list the atm's based on a criteria
   1. Will need to add GSI on attributes like provider and address.
2. Add model validations to the api to ensure - 
   1. Rating is a float
   2. length of address is within the DB limits
   3. Provider is a pre-existing name
3. Make the POST/PUT requests idempotent.

#### Client Experience
1. Have a Swagger UI endpoint to help clients read the api docs.
2. Use a human-readable URI instead of the endpoint generatd by APi gateway.
   1. Use Route53 for storing the DNS records.
   2. Use certificate manager to create a certificate for the URI.

#### Concurrency Handling
1. Change the writes to use locking
  - Possible ideas - [Link](https://dynobase.dev/dynamodb-locking/)

#### Performance Testing
1. Run load tests

#### Logging
1. Have standardized logs
2. Emit metrics per api







