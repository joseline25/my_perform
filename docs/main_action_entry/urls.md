# ActionMainEntry Urls

| URL                       | Verb   | Functionality                                      |
|---------------------------------------------------|--------|----------------------------------------------------|
| /action-main-entries/                             | GET    | Fetches all action main entries                     |
| /action-main-entries/{id}/                        | GET    | Fetches a single action main entry with the given ID |
| /action-main-entries/delete/{id}/                        | DELETE | Removes the identified action main entry            |
| /action-main-entries/update/{id}/                        | PUT    | Updates the entire action main entry with the request data |
| /action-main-entries/                             | POST   | Creates a new action main entry based on the request data |
| /action-main-entries/{date}/                      | GET    | Fetches actions for a particular date               |
| /action-main-entries/{start_date}/{end_date}/      | GET    | Fetches action entries within a timeframe           |
| /action-main-entries/{objective_id}/              | GET    | Fetches all action main entries for a specific objective |
