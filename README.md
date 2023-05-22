

# To D List Application

A simple Flask  application for managing tasks.

## Installation

1. Clone the repository:
https://github.com/Mohan8474/Todo.git


2. Navigate to the project directory:

cd Todo


3. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate


4. Install the dependencies:

pip install -r requirements.txt

## Usage

1. Load the intial data

python3 bin/load_initial_data.py

2. Run the application

flask run 
or
run the run.py file

3. Access the API Endpoints

   - Open your web browser or use an API testing tool (e.g.Postman).

   - Use the following base URL to access the API endpoints:

     ```
     http://localhost:5000/tasks
     ```

   - Endpoint 1: `/tasks`
     - Method: GET (To retrieve all tasks)
     - Method: POST (To create a new task(single and multiple) )
     - Method: PUT (To Update a task(single and multiple))
     - Method: DELETE (To Delete all tasks)

   - Endpoint 2: `/tasks/{id}`
     - Method: GET (To retrieve a specific task)
     - Method: DELETE (To delete a specific task)
 



