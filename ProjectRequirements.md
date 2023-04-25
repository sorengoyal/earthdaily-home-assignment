# Requirements
## Product Requirements
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
		- Apigateway+Lambda can handle 2000 TPS. APigateway can be configured to throttle requests beyond 2000 TPS
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
	- Link to Git repo: TBD
2. Please have this exercise in a working state such that it can be demo-ed during the interview itself
	- Link to AWS Endpoint:
3. Timebox effort to 4 hrs + 2hrs
	- Actual spent: 15 hrs
	  - 9 hrs on AWS setup
      - 5 hrs the code
      - 1 hr on doc 


# Clarifications
1. Should a a GET called right after POST return the correct object or  a HTTP 404?
2. What is the possible time lag between a POST and PUT request for the same resource?
2. Do the need the endpoint to be protected from a DDOS?
3. Do we need a authN mechanism to acces the gateway?







