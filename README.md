[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)
# ServerlessTemplate

Not completed yet 

## Cloud Function
Uses graphql and python requests to get leetcode question and add in additional fields to match mongoose question model.


### Running the script locally
1) Create .env file in root
___
.env file variable

MONGO_URI=mongodb+srv://{username}:{password}@{clusterid}.3w1nmj1.mongodb.net/{dbname}?retryWrites=true&w=majority
___
2) Run in terminal `pip install pipenv`
3) `pipenv shell`
4) `pipenv install -r requirements.txt`
5) `python3 main.py <limit>`
___
![image](https://github.com/CS3219-AY2324S1/ay2324s1-assignment-6-g06/tree/branch-assignment-6/images/localhost)
___
6) `exit`

### Deployed function
For 10 questions

To change the number of questions, change the value after `limit=`

- https://asia-northeast2-cs3219-group6-400112.cloudfunctions.net/put-questions?limit=10

For all questions

- https://asia-northeast2-cs3219-group6-400112.cloudfunctions.net/put-questions

### Verification

[Website](https://fe-cd-test-a2rwifv3ta-dt.a.run.app/)

- user: serverless
- password: serverless

