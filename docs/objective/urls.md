# Objective Urls

| URL                 | Verb    |Functionality                                            |
|------------------------------------------|--------|----------------------------------------------------------|
| /objectives/                             | GET    | Fetches all objectives                                   |
| /objectives/                             | POST   | Creates a new objective based on the request data         |
| /objectives/{objective_id}/               | GET    | Fetches a single objective with the given ID             |
| /objectives/update/{objective_id}/        | PUT    | Updates the entire objective with the request data       |
| /objectives/delete/{objective_id}/        | DELETE | Removes the identified objective                         |
| /objectives/{objective_id}/kpis/          | GET    | Fetches all KPIs for the specified objective             |
| /objectives/{objective_id}/kpis/          | POST   | Creates a new KPI for the specified objective            |
| /objectives/{objective_id}/actions/       | GET    | Fetches all actions for the specified objective          |
| /objectives/{objective_id}/questions/     | GET    | Fetches all questions for the specified objective        |
|objectives/{objective_id}/changes/         | GET    | Fetches all changes made on an objective|

## Publish an objective

| URL                                               | Verb   | Functionality                                      |
|---------------------------------------------------|--------|----------------------------------------------------|
| /objectives/publish_objective/{objective_id}/      | GET    | Publishes an objective with the given ID            |
| /objectives/published_objectives/                 | GET    | Fetches a list of published objectives              |
| /objectives/completed_objectives/                 | GET    | Fetches a list of completed objectives              |
