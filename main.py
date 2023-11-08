import functions_framework
import requests
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv

load_dotenv()
# Define the GraphQL endpoint URL.
GRAPHQL_URL = "https://leetcode.com/graphql"
MONGO_URI = os.getenv("MONGO_URI")

# Define your GraphQL query.
query = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      difficulty
      frontendQuestionId: questionFrontendId
      title
      topicTags {
        name
        id
        slug
      }
      solution {
        body
      }
      hasSolution
      hasVideoSolution
      content
      categoryTitle
    }
  }
}
"""

# Function to send the GraphQL query with a filter.
def get_questions_with_filter(category_slug, limit, filter):
    # Define the variables for the GraphQL query.
    variables = {
        "categorySlug": category_slug,
        "limit": limit,
        "filters": filter
    }

    # Create a new client and connect to the server
    # .env looks something like this with the {} filled up
    # MONGO_URI=f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{dbName}?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI)

    # Select a specific database and collection
    db = client['questions']  # Replace 'your_database_name' with your actual database name
    collection = db['serverless']  # Replace 'your_collection_name' with your actual collection name

    # Remove previous questions 
    collection.delete_many({})

    # Create an empty list to store the questions
    questions_to_insert = []

    # Send the GraphQL request.
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables})

    # Check if the request was successful (status code 200).
    if response.status_code == 200:
        data = response.json()
        questions = data['data']['problemsetQuestionList']['questions']

        # Process and append the question data to the list, including solutions for questions that have them
        for question in questions:
            # Check if a solution exists before accessing its "body"
            if question['solution']:
                # Concatenate topic titles with commas
                topics = ", ".join(tag['name'] for tag in question['topicTags'])
                # our structure of quesition data 
                question_data = {
                    "title": question['title'],
                    "frontendQuestionId": question['frontendQuestionId'],
                    "difficulty": question['difficulty'],
                    "category": question['categoryTitle'],
                    "topics": topics,  # Store topics as a comma-separated string
                    "content": question['content'],
                    "solution": question['solution']['body'],  # Include the solution
                    "isDeleted": False
                }
                questions_to_insert.append(question_data)

        # Insert the questions into MongoDB (For debugging purposes)
        if questions_to_insert:
            result = collection.insert_many(questions_to_insert)
            print(f"Inserted {len(result.inserted_ids)} questions into MongoDB.")
        else:
            print("No questions to insert.")
    else:
        print("Failed to retrieve data from the GraphQL API.")
    
    # Close the MongoDB client connection when done
    client.close()
    return questions_to_insert

# cloud function
@functions_framework.http
def put_questions(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    # Define filter parameters as a Python dictionary.
    custom_filter = {}

    category_slug = ""  # Replace with the desired category slug.
    if request_args and 'limit' in request_args:
      limit = request_args['limit']
    else:
      limit = 2852  # Number of questions to retrieve.

    questions = get_questions_with_filter(category_slug, limit, custom_filter)
    return "DB populated with {} questions".format(len(questions))

if __name__ == "__main__":
    # Define filter parameters as a Python dictionary.
    custom_filter = {}

    category_slug = ""  # Replace with the desired category slug.
    limit = 2852 if len(sys.argv) == 1 else int(sys.argv[1]) # Number of questions to retrieve.

    get_questions_with_filter(category_slug, limit, custom_filter)
