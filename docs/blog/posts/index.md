---
date: 2024-10-24
categories:
  - Example category
tags:
  - Example tag
---

# Example post

## Example Heading 2

Example content.

```python
print("Example code block")
```

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        string name
        string email
    }
    ORDER {
        date ordered
    }
    LINE-ITEM {
        int quantity
    }
```

| Method   | Description                          |
| -------- | ------------------------------------ |
| `GET`    | :material-check: Fetch resource      |
| `PUT`    | :material-check-all: Update resource |
| `DELETE` | :material-close: Delete resource     |
