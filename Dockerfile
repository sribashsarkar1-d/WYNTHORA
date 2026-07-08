FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install necessary build tools
RUN apk add --no-cache git gcc musl-dev

# Copy go mod and sum files
COPY backend/core-engine/go.mod backend/core-engine/go.sum ./
RUN go mod download

# Copy source code
COPY backend/core-engine/ .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/server

# Final stage
FROM alpine:latest  
RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# Copy binary from builder
COPY --from=builder /app/main .
COPY --from=builder /app/.env.development .
COPY --from=builder /app/.env.production .

# Expose port
EXPOSE 8080

# Run the binary
CMD ["./main"]
