# Purpose

This endpoint retrieves all the changes made to a specific objective based on its ID.

## Endpoint URL

GET /objectives/{objective_id}/changes/

Example: <http://localhost:8000/api/objectives/1/changes/>

**Method:** GET

**Path Parameters:**

- `objective_id` (integer, required): Unique identifier for the objective.

## Response

### Status Codes

- 200 OK: Objective changes retrieved successfully.
- 404 Not Found: Objective with the specified ID does not exist.

### Response Body (Success)

```json
[
  {
    "objective_id": 1,
    "user": "john@example.com",
    "timestamp": "2024-02-28T15:30:00Z",
    "changes": "Updated objective name to 'New Objective'"
  },
  {
    "objective_id": 1,
    "user": "jane@example.com",
    "timestamp": "2024-02-28T16:45:00Z",
    "changes": "Updated deadline to '2024-12-31'"
  },
  ...
]
