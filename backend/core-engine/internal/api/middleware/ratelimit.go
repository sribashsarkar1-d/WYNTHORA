package middleware

import (
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/cache"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
)

// RateLimiter uses Redis to limit requests per IP
func RateLimiter(limit int, window time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		if cache.Client == nil {
			// If Redis isn't initialized yet, skip rate limiting
			c.Next()
			return
		}

		ip := c.ClientIP()
		key := "rate_limit:" + ip

		ctx := context.Background()

		// Increment the counter for this IP
		count, err := cache.Client.Incr(ctx, key).Result()
		if err != nil {
			utils.Logger.Error("Failed to increment rate limit counter")
			c.Next()
			return
		}

		if count == 1 {
			// Set expiration on first request
			cache.Client.Expire(ctx, key, window)
		}

		if count > int64(limit) {
			utils.RespondError(c, http.StatusTooManyRequests, "RATE_LIMIT_EXCEEDED", "Too many requests. Please try again later.", nil)
			c.Abort()
			return
		}

		c.Next()
	}
}
