FROM golang:1.21-alpine

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o /engineapp .

# Expose HTTP port
EXPOSE 8082
# Expose gRPC port
EXPOSE 50051

CMD [ "/engineapp" ]
