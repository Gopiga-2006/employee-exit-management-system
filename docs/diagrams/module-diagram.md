# Module Diagram

```mermaid
flowchart TB
    Core[Core] --> Routers[API Routers]
    Routers --> Services[Service Layer]
    Services --> Models[ORM Models]
    Services --> Schemas[Pydantic Schemas]
    Models --> Database[MySQL Database]
```

## Main Modules
- `app/api/`: REST API routers.
- `app/core/`: settings, security helpers, and database setup.
- `app/models/`: SQLAlchemy models.
- `app/schemas/`: request and response schemas.
- `app/services/`: business logic.
- `tests/`: automated tests added in later development work.
