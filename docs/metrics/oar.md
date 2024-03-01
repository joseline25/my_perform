# Purpose

This endpoint calculates the user performance based on the assigned objectives within a specified timeframe.

## Endpoint URL

GET /objectives/user_performance/{user_id}/{start_date}/{end_date}/

Example: <http://localhost:8000/api/objectives/user_performance/1/2024-01-01/2024-01-31/>

**Method:** GET

**Parameters:**

- `user_id` (integer, required): Unique identifier for the user.
- `start_date` (string, required): Start date of the timeframe (format: "YYYY-MM-DD").
- `end_date` (string, required): End date of the timeframe (format: "YYYY-MM-DD").

## Response

### Status Codes

- 200 OK: User performance data retrieved successfully.
- 404 Not Found: User with the specified ID does not exist.

### Response Body (Success)

```json
{
  "user": {
    "id": 1,
    "username": "john",
    ...
  },
  "completed_objectives": [
    {
      "objective_id": 1,
      "objective_name": "Project Launch",
      ...
    },
    ...
  ],
  "assigned_objectives": [
    {
      "objective_id": 2,
      "objective_name": "Product Development",
      ...
    },
    ...
  ],
  "completed_objectives_count": 3,
  "assigned_objectives_count": 5,
  "oar": 60.0
}

### Response Body (Error)

```json
{}

```
