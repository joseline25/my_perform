# Purpose : endpoint allows the deletion of an existing objective by submitting a DELETE request with the objective ID

## Endpoint URL: DELETE /api/delete_objective/<objective_id>/

Method: DELETE
URL Parameters:
<objective_id> (integer, required): The unique identifier of the objective to be deleted.

## Response

### Status Codes

204 No Content: Objective deleted successfully.
404 Not Found: If no objective with the specified ID is found.

### Response Body (Success)

``
{
  "message": "This Objective is deleted"
}

``

### Response Body (Error)

``
{
  "message": "No Objective found"
}

``