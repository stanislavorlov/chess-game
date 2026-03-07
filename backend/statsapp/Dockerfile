FROM golang:1.24-bookworm AS builder

WORKDIR /app

# Check cache for modules
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the stats API. CGO is enabled by default, which is needed for confluent-kafka-go
RUN CGO_ENABLED=1 GOOS=linux go build -o statsapp main.go

# Generate a small image
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/statsapp /app/statsapp

EXPOSE 8081

CMD ["/app/statsapp"]
