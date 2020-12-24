# Coding Exercise

Implement a Restful task list API as well as run this application in container.

- Spec
  - Fields of task:
      - name
          - Type: String
      - status
          - Type: Bool
          - Value
              - 0=Incomplete
              - 1=Complete
  - Reponse headers
      - Content-Type=application/json
  - Unit Test
  - DB migration strategy
  - Manage code base on Github

- Runtime Environment Requirement
    - Python 3.7
    - Flask 1.1
    - uWSGI LTS
    - MySQL 5.7
    - nginx 1.19.5
    - Ubuntu 18.04
    - Docker


### 1.  GET /tasks (list tasks)
```
{
    "result": [
        {"id": 1, "name": "name", "status": 0}
    ]
}
```

### 2.  POST /task  (create task)
```
request
{
  "name": "買晚餐"
}

response status code 201
{
    "result": {"name": "買晚餐", "status": 0, "id": 1}
}
```

### 3. PUT /task/<id> (update task)
```
request
{
  "name": "買早餐",
  "status": 1
  "id": 1
}

response status code 200
{
  "name": "買早餐",
  "status": 1,
  "id": 1
}
```

### 4. DELETE /task/<id> (delete task)
response status code 200
