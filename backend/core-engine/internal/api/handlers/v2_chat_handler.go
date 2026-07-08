package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type ChatHandler struct {
	Service services.ChatService
}

func NewChatHandler(svc services.ChatService) *ChatHandler {
	return &ChatHandler{Service: svc}
}

func (h *ChatHandler) Completions(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "completion generated"})
}
func (h *ChatHandler) GetHistory(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"history": []string{}})
}
func (h *ChatHandler) RagSync(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "rag sync complete"})
}
func (h *ChatHandler) GetPrompts(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"prompts": []string{}})
}
func (h *ChatHandler) DeleteThread(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
func (h *ChatHandler) Feedback(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "feedback received"})
}
