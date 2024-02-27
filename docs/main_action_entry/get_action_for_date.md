
# Purpose: This endpoint retrieves all actions recorded for a specific date

# URL: GET /api/actions/{date}/

Example: <http://localhost:8000/api/action/2023-01-01/>

Method: GET
URL Parameters:
{date} (required): The date for which actions are to be retrieved in the format YYYY-MM-DD.

# Response

## Status Codes

200 OK: Successful request. Actions for the specified date are returned.
400 Bad Request: Invalid date format provided in the request URL.
Response Body: JSON representation of actions for the specified date.

Each action object contains the fields of the ActionMainEntry model

## Sample Response

[
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
"objective": 5,
"duration": 90,
"achievements": "Learning",
"collaborators": [4, 5]
}
]

## Error Responses

400 Bad Request: Invalid date format provided in the request URL.
Response Body:
{
  "error": "Invalid date format. Use YYYY-MM-DD."
}
