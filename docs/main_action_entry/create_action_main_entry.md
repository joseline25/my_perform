# Purpose : This endpoint allows users to create a new action main entry

``
@api_view(['POST'])
def create_action_main_entry(request):
    if request.method == 'POST':
        serializer = ActionMainEntryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

``

Endpoint URL : POST /api/action-main-entries/create/

Method: POST
Request Body: JSON object representing the action main entry to be created. The request body should conform to the structure defined by the ActionMainEntryPostSerializer.

## Response

## Status Codes

201 Created: Action main entry successfully created.
400 Bad Request: Invalid request data provided.
Response Body: JSON representation of the newly created action main entry.

The response contains the same fields as the request body, along with any additional fields generated by the server (e.g., auto-generated ID).

## Sample Request Body

`` {
  "name": "Meeting with Team",
  "what_you_did_today": "Discussed project progress and upcoming tasks.",
  "objective": 3,
  "duration": 60,
  "achievements": "Work-Product",
  "collaborators": [1, 2, 3]
}
``

## Sample Response

```python
{
  "id": 1,
  "name": "Meeting with Team",
  "what_you_did_today": "Discussed project progress and upcoming tasks.",
  "objective": 3,
  "duration": 60,
  "achievements": "Work-Product",
  "collaborators": [1, 2, 3]
}

```

## Error Responses

400 Bad Request: Invalid request data provided. The response body will contain details about the validation errors.
