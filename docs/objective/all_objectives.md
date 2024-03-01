# All Objectives

**Endpoint:** `/objectives/`\
**HTTP Method:** GET

## Description

This endpoint retrieves all objectives and associated users from the database.

### Request

- No request parameters required.

### Response

The response will be a JSON object with the following structure:

```json
{
  "objectives": [
    {
      "id": 1,
      "name": "Objective 1",
      ...
    },
    ...
  ],
  "users": [
    {
      "id": 1,
      "name": "User 1",
      ...
    },
    ...
  ]
}
