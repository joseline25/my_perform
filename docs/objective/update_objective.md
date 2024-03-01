# Purpose

This endpoint updates the details of a specific objective based on its ID.

## Endpoint URL

PUT /objectives/update/{objective_id}/

Example: <http://localhost:8000/api/update_objective/1/>

**Method:** PUT

**Path Parameters:**

- `objective_id` (integer, required): Unique identifier for the objective.

## Request Body

The request body should contain the updated data for the objective. The fields are similar to the response body structure mentioned in the previous documentation.

## Response

### Status Codes

- 200 OK: Objective successfully updated.
- 404 Not Found: Objective with the specified ID does not exist.

### Response Body (Success)

```json
{
  "objective_id": 1,
  "objective_name": "Updated Objective",
  ...
  "completion_date": "2024-12-31T23:59:59Z",
  "estimated_hours": 10
}

### Response Body (Error)

``
{
  "message": "No objective found"
}

``
