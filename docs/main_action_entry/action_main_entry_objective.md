# Purpose : This endpoint retrieves all actions associated with a specific objective

## Endpoint URL : GET /api/action_main_entry_objective/{objective_id}/

Method: GET

## URL Parameters

{objective_id} (required): The ID of the objective for which actions are to be retrieved.

## Response

### Status Codes

200 OK: Successful request. Actions associated with the specified objective are returned.
404 Not Found: The specified objective does not exist.
Response Body: JSON representation of actions associated with the specified objective.

### Sample Response

`` [
  {
    "id": 1,
    "date": "2024-02-12",
    "name": "Meeting with Team",
    "what_you_did_today": "Discussed project progress and upcoming tasks.",
    "objective": 3,
    "duration": 60,
    "achievements": "Work-Product",
    "collaborators": [1, 2, 3]
  },
  {
    "id": 2,
    "date": "2024-02-12",
    "name": "Research on New Technology",
    "what_you_did_today": "Explored options for integrating AI into the project.",
    "objective": 3,
    "duration": 90,
    "achievements": "Learning",
    "collaborators": [4, 5]
  }
]
 ``

## Error Responses

404 Not Found: The specified objective does not exist.
Response Body: None
