# 09. Business Data Access Architecture

## Repository Abstraction Layer
The Python data access services in `supporthub-ai-architecture/data_access/` currently read JSON files. 

Future design introduces an abstract repository interface (`IBusinessDataRepository`):
```
AI Tools -> ToolRegistry -> Business Data Service -> Database Repository (SQLAlchemy/MySQL)
```
