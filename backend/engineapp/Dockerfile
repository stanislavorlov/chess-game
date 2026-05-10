# Stage 1: Build
FROM golang:1.24-bookworm AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o /engineapp .

# Stage 2: Runtime
FROM debian:bookworm-slim

WORKDIR /app

# Install ca-certificates for any HTTPS requests
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /engineapp /app/engineapp

# Expose HTTP port
EXPOSE 8082
# Expose gRPC port
EXPOSE 50051

CMD [ "./engineapp" ]
