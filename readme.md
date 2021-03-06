API for todo app.

documentation (OpenAPI): https://todoapptests.herokuapp.com/api/openapi/

    Supports:
    - JWT Authentication
    - Creating user
    - Adding new task
    - Updating existing task
    - Deleting existing task
    - Shows all user's tasks to current user
    - Shows all tasks to admin
    - Filtering by status, or by priority, or both

# JWT Authentication

See documentation for details on making requests!

    url: "api/v1/token/" 
    Response: 2 objects. 
    'access' - token for authentication. Lives 15 minutes, then expires
    'refresh' - token for refreshing 'access' token. Lives 1 day

    url: "api/v1/token/refresh"
    Used for get new 'access' token, when old one expired

    Response: 2 objects.
    new 'access' token
    new 'refresh' token

# How to filter tasks?

This part needs upgrade, but it works

    url: /api/v1/tasks/?status={int: 1 or 2 or 3}&priority={int: 1 or 2 or 3}

    Priority:
    1 - "High Priority"
    2 - "Medium Priority"
    3 - "Low Priority"

    Status:
    1 - "Not Started"
    2 - "In Progress"
    3 - "Done"


    Examples:
    - /api/v1/tasks/?status=3&priority=3
    Shows tasks, which have priority 3 ("High priority") and status 3 ("Done")

    - /api/v1/tasks/?priority=3
    Shows tasks which have priority 3 ("High Priority")