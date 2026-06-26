package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

type contextKey string

const (
	UserIDKey contextKey = "user_id"
	UserIPKey contextKey = "user_ip"
)

// extractUserId tries to parse JWT from Authorization header, fallback to X-User-ID
func extractUserId(r *http.Request) string {
	authHeader := r.Header.Get("Authorization")
	if authHeader != "" && strings.HasPrefix(authHeader, "Bearer ") {
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		token, _, err := new(jwt.Parser).ParseUnverified(tokenString, jwt.MapClaims{})
		if err == nil {
			if claims, ok := token.Claims.(jwt.MapClaims); ok {
				if sub, ok := claims["sub"].(string); ok {
					return sub
				}
			}
		}
	}
	// Fallback to custom header if provided
	return r.Header.Get("X-User-ID")
}

func getIpAddress(r *http.Request) string {
	ip := r.Header.Get("X-Forwarded-For")
	if ip == "" {
		ip = r.RemoteAddr
	}
	return ip
}

// RequestInfoMiddleware extracts the user ID and IP address and adds them to the request context
func RequestInfoMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		userID := extractUserId(r)
		userIP := getIpAddress(r)

		ctx := context.WithValue(r.Context(), UserIDKey, userID)
		ctx = context.WithValue(ctx, UserIPKey, userIP)

		next(w, r.WithContext(ctx))
	}
}

// GetUserID retrieves the user ID from the context
func GetUserID(ctx context.Context) string {
	if val, ok := ctx.Value(UserIDKey).(string); ok {
		return val
	}
	return ""
}

// GetUserIP retrieves the user IP from the context
func GetUserIP(ctx context.Context) string {
	if val, ok := ctx.Value(UserIPKey).(string); ok {
		return val
	}
	return ""
}
