# Purpose : endpoint allows the creation of new objectives by submitting a POST request with the necessary data

## Endpoint URL : POST /api/create_objective/

Method: POST
Request Body:
Content-Type: application/json
Parameters:
    1. objective_name (string, required): Name or title of the objective.
    2. assign_to (array of integers, optional): User IDs to assign the objective.
    3. visible_to (array of integers, optional): User IDs who have access to view the objective.
    4. associated_task (string, required): Description of the task associated with the objective.
    5. deadline (string, optional): Deadline for completing the objective (YYYY-MM-DD HH:MM:SS).
    6. action_phrase (string, required): Action phrase describing what needs to be done to achieve the objective.
    7. number (integer, required): Number of outputs expected from the objective.
    8. units (string, required): Unit of measurement for the objective outputs.
    9. start_date (string, required): Start date of the objective (YYYY-MM-DD HH:MM:SS).
    10. end_date (string, required): End date of the objective (YYYY-MM-DD HH:MM:SS).
    11. priority (string, required): Priority level of the objective (Low, Intermediate, High).
    12. complexity (string, required): Estimated difficulty level of executing the objective (Easy, Hard).
    13. objective_type (string, required): Type of objective (Financial, Non-Financial).
    14. skills (array of integers, optional): IDs of required competencies for completing the objective.
    15. tools (array of integers, optional): IDs of recommended tools for achieving the objective.
    16. dog (string, required): Definition of Good criteria for evaluating the objective.
    17. is_draft (boolean, optional): Indicates whether the objective is in draft status.
    18. repeat (boolean, optional): Indicates whether the objective should be repeated

## Response

### Status Codes

201 Created: Objective created successfully.
400 Bad Request: Invalid request parameters.

### Response Body (Success)

``{
  "status": "success",
  "message": "Objective created successfully"
}
``

### Response Body (Error)

``{
  "objective_name": ["This field is required."],
  "associated_task": ["This field is required."]
  ...
}

``

## Usage

``
{
  "objective_name": "Project Launch",
  "assign_to": [1, 2],
  "visible_to": [3, 4],
  "associated_task": "Develop and launch a new product.",
  "deadline": "2024-12-31 23:59:59",
  "action_phrase": "Develop",
  "number": 1,
  "units": "Product",
  "start_date": "2024-01-01 00:00:00",
  "end_date": "2024-12-31 23:59:59",
  "priority": "High",
  "complexity": "Hard",
  "objective_type": "Financial",
  "skills": [5, 6],
  "tools": [7, 8],
  "dog": "Successfully launch the product.",
  "is_draft": false,
  "repeat": false
}

``
