---
name: go-grpc-microservice
description: 'Authoring, refactoring, or optimizing Go backend microservices, gRPC protobuf handlers, and concurrent worker patterns.'
---

# Goal
Provide high-performance, idiomatically sound Go code following modern Clean Architecture principles, ensuring concurrency safety and strict memory management.

# Instructions
1. **Explicit Error Handling:** Never swallow errors or use blank identifiers (`_`) for active failures. Wrap downstream errors using `fmt.Errorf("context: %w", err)` to maintain trace decoration.
2. **Concurrency Guardrails:** When spawning goroutines, always enforce context propagation (`ctx`). Ensure maps or shared state mutations utilize `sync.Mutex` or channel communication to explicitly eliminate data races.
3. **Protobuf & gRPC Integration:** Ensure all server implementations map smoothly to generated `.pb.go` structures. Validate incoming request parameters explicitly before invoking service-layer business logic.
4. **Performance & Profiling:** Use pointer receivers for large structs to avoid stack-copying overhead. When working with slice allocations of known lengths, initialize using `make([]T, 0, length)` to minimize underlying array reallocations.

# Constraints
- Do not use the `init()` function for setting up dependencies (e.g., database connections, configurations); utilize explicit dependency injection.
- Avoid naked returns in long or complex functions.
- Run all unit tests with the race detector enabled (`go test -race ./...`).