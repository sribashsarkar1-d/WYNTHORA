package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type CollabHandler struct {
	Service services.CollabService
}

func NewCollabHandler(svc services.CollabService) *CollabHandler {
	return &CollabHandler{Service: svc}
}

func (h *CollabHandler) CreateSession(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusCreated, "Success", gin.H{"message": "session created"})
}
func (h *CollabHandler) GetActiveUsers(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"users": []string{}})
}
func (h *CollabHandler) UpdateCursors(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "cursors updated"})
}
func (h *CollabHandler) PostMessage(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "message sent"})
}
func (h *CollabHandler) DeleteSession(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
