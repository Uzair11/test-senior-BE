## Running the project
Build the docker-compose file using 
``` make build ```
. Run the containers using
``` make up ```
In a separate terminal, run the command
``` make console```
Then run the commands in the following sequence
```
ls app
flask db init
flask db migrate -m ""
flask db upgrade
```

Open a different terminal and use the following command

``` make start ```

#### Challenges faced

There were a couple of  challenges that I faced during performing this task. The first challenge that I faced was to decide whether to store all the DB information inside mongodb   upon submit-creds API call so thst future retrieval of information regarding DB can be done in a fast and efficient manner. However, this posed a problem of metadata sync between local DB and provided. Keeping this issue in mind at this level, I developed  asynchronous APIs that would establish connection with the DB for retrieving upto date information. The APIs are developed on top of asynchronous programming and use highly efficient queries to avoid latencies whilst connecting to the DB. The ConnectionManager class is an asynchronous context manager class built on top template pattern for handling connections in a non-blocking manner. The code base currently supports connections with postgresql and mysql db. However, support for other types of DBs can easily be extended.
#### How would you implement authentication?
I have implemented authentication using jwt with a 300s timeout and object level permissions for a secure communication channel. However, more secure measures like storing encrypted data in the DB and MFA can be implemented as well
#### If you had to scale this system up to serve 1000s of requests per hour, how would you do it?
If the system had to serve 1000s of requests per hour, my first approach would be to generally implement a load balancer in order to distribute the load of requests across nodes and along with that I would be implementing caching strategies using redis. In order to further scale, I would break down the application in microservices architecture more generally in a service mesh pattern

#### If you had to be able to support Databases with 10,000 tables, how would your design change? What if you had to support databases with a million columns across 100,000 tables?
If I had to tackle this scenario, I would radically change the system design by first of all instead of loading metadata of the connected DB into the memory, I would implement a system to stream the results back to client. Additionally I would also consider a couple of other methods like batch processing and pagination with client providing the size of batch and suitable pagination params for efficient retreival.

### Data model
The DB consists of two tables
#### User Table
 ```
Column id int primary-key
Column username String
Column email String
Column password String
```

#### DbCredentials Table
```
Column id int primary-key
Column user_id int Foreign Key (User)
Column host String
Column port String
Column db_name String
Column username String



One to many relation between both the tables
```

### Documentation of APIs
You may access the documentation of APIs at
``` http://localhost:5000/apidocs/index.html ```