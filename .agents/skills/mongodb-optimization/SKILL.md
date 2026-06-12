---
name: mongodb-optimization
description: "Designing, refactoring, or optimizing MongoDB collections, write operations, query structures, index configurations, and database connection pools."
---

# Goal
Formulate high-performance, resilient, and structurally sound MongoDB schema designs, query strategies, and connection lifecycles.

# Instructions
1. **Index Strategy**: Always ensure fields utilized frequently in query filters or sort constraints have matching indexes (especially compound indexes). 
2. **Schema Design Patterns**: Leverage appropriate schema mapping strategies (embedding vs referencing) relative to data scale, balancing transactional needs.
3. **Optimized Write Operations**: Minimize databaseroundtrips by utilizing bulk write operations (`InsertMany`, `UpdateMany`, `BulkWrite`) where concurrency permits.
4. **Connection Pool Management**: Maintain a single client instance throughout the application lifecycle to utilize MongoDB's built-in connection pool instead of instantiating clients on every request.
5. **Projection Filtering**: Avoid fetching entire documents when only a subset of fields is needed. Utilize projection queries to reduce network overhead.

# Constraints
- Do not execute unindexed queries that lead to collection scans in production environments.
- Enforce clean, structured BSON mappings in all application DTO schemas.
