# Average Number of Actions per Objective (ANA/O)

## Endpoint URL

GET /objectives/user_average_actions_objective/{user_id}/{start_date}/{end_date}/

Example: <http://localhost:8000/api/objectives/user_average_actions_objective/1/2023-01-01/2023-12-31/>

**Method:** GET

**Parameters:**

- `user_id` (integer, required): Unique identifier for the user.
- `start_date` (string, required): Start date of the timeframe (format: "YYYY-MM-DD").
- `end_date` (string, required): End date of the timeframe (format: "YYYY-MM-DD").

## Response

### Status Codes

- 200 OK: Average actions per objective data retrieved successfully.
- 404 Not Found: User with the specified ID does not exist.

### Response Body (Success)

```json
{
  "user": {
    "id": 1,
    "username": "john",
    ...
  },
  "total_actions": 10,
  "total_objectives": 5,
  "average_actions_per_objective": 2.0
}

### Response Body (Error)

```json`
{}

```
