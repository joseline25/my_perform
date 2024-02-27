# Purpose: This endpoint retrieves all actions recorded within a specified time frame

## Endpoint URL: GET /api/actions/get_actions_in_timeframe/{start_date}/{end_date}/

Method: GET

## URL Parameters

{start_date} (required): The start date of the time frame for retrieving actions in the format YYYY-MM-DD.
{end_date} (required): The end date of the time frame for retrieving actions in the format YYYY-MM-DD.

## Response

### Status Codes

200 OK: Successful request. Actions within the specified time frame are returned.
400 Bad Request: Invalid date format provided in the request URL.
Response Body: JSON representation of actions within the specified time frame.

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
    "name": "Research on new technology",
    "what_you_did_today": "Explored options for integrating AI into the project.",
    "objective": 5,
    "duration": 90,
    "achievements": "Learning",
    "collaborators": [4, 5]
  }
]

``

### Error Responses

400 Bad Request: Invalid date format provided in the request URL.
Response Body

`` {
  "error": "Invalid date format. Use YYYY-MM-DD."
}

``
