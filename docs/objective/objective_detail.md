# Purpose

This endpoint retrieves details of a specific objective based on its ID.

## Endpoint URL

GET /objectives/{objective_id}/

Example: <http://localhost:8000/api/objectives/1/>

**Method:** GET

**Path Parameters:**

- `objective_id` (integer, required): Unique identifier for the objective.

## Response

### Status Codes

- 200 OK: Objective details retrieved successfully.
- 404 Not Found: Objective with the specified ID does not exist.

### Response Body (Success)

```json
{
  "objective_id": 1,
  "objective_name": "Project Launch",
  "assign_to": [1, 2],
  "visible_to": [3, 4],
  "associated_task": "Develop and launch a new product.",
  "deadline": "2024-12-31T23:59:59Z",
  "action_phrase": "Develop",
  "number": 1,
  "units": "Product",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "priority": "High",
  "complexity": "Hard",
  "objective_type": "Financial",
  "skills": [5, 6],
  "tools": [7, 8],
  "dog": "Successfully launch the product.",
  "is_draft": false,
  "repeat": false,
  "status": "In Progress",
  "completion_date": null,
  "estimated_hours": 0
}

### Response Body (Error)

```json
{
  "detail": "Not found."
}

```
