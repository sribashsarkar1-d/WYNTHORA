package utils

import (
	"github.com/gin-gonic/gin"
)

type SuccessResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

type ErrorResponse struct {
	Success bool     `json:"success"`
	Code    string   `json:"code"`
	Message string   `json:"message"`
	Errors  []string `json:"errors"`
}

// RespondSuccess formats and sends a standard JSON success response.
func RespondSuccess(c *gin.Context, status int, message string, data interface{}) {
	if data == nil {
		data = map[string]interface{}{}
	}
	c.JSON(status, SuccessResponse{
		Success: true,
		Message: message,
		Data:    data,
	})
}

// RespondError formats and sends a standard JSON error response.
func RespondError(c *gin.Context, status int, code, message string, errors []string) {
	if errors == nil {
		errors = []string{}
	}
	c.JSON(status, ErrorResponse{
		Success: false,
		Code:    code,
		Message: message,
		Errors:  errors,
	})
}
