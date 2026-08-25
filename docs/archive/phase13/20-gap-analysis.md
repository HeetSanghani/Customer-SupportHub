# 20. Architecture Gap Analysis

- **Current**: JSON file storage for business data.
- **Target**: MySQL relational database with SQLAlchemy async ORM repositories.
- **Gap**: Creation of DB tables, migration script, and MySQL repository implementations in `data_access/`.
