# Purpose : endpoint allows the modification of an existing objective by submitting a PUT request with the updated data

## Endpoint URL: PUT /api/update_objective/<objective_id>/

Method: PUT
URL Parameters:
<objective_id> (integer, required): The unique identifier of the objective to be updated.

## Request Body

Content-Type: application/json
Parameters: Same as those required for creating a new objective.

## Response

### Status Codes

200 OK: Objective updated successfully.
400 Bad Request: If the request contains invalid data.
404 Not Found: If no objective with the specified ID is found.

### Response Body (Success)

``
{
  "objective_id": 1,
  "objective_name": "Updated Objective",
  ...
}

``

### Response Body (Error)

``
{
  "message": "No objective found"
}

``