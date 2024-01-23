## Running the project
Build the docker-compose file using 
make build
Run the containers using
make up
In a separate terminal, run the command
make console
Then run the commands in the following sequence
ls app
flask db init
flask db migrate -m ""
flask db upgrade

Open a different terminal and use the following command

make start

### Challenges faced

There were a couple of  challenges that I faced during performing this task. The first challenge that I faced was to decide whether to store all the DB information inside mongodb   upon submit-creds API call so thst future retrieval of information regarding DB can be done in a fast and efficient manner. However, this posed a problem of metadata sync between local DB and provided. Keeping this issue in mind at this level, I developed  asynchronous APIs that would establish connection with the DB for retrieving upto date information. The APIs are developed on top of asynchronous programming and use highly efficient queries to avoid latencies whilst connecting to the DB. The ConnectionManager class is an asynchronous context manager class built on top template pattern for handling connections in a non-blocking manner. The code base currently supports connections with postgresql and mysql db. However, support for other types of DBs can easily be extended.
### How would you implement authentication?
I have implemented authentication using jwt with a 300s timeout and object level permissions for a secure communication channel. However, more secure measures like storing encrypted data in the DB and MFA can be implemented as well

### Data model
The DB consists of two tables
#### User Table
Column id primary-key
Column username String
Column email String
Column password String

#### DbCredentials Table


One to many relation between both the tables