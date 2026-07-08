package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type PluginHandler struct {
	Service services.PluginsService
}

func NewPluginHandler(svc services.PluginsService) *PluginHandler {
	return &PluginHandler{Service: svc}
}

func (h *PluginHandler) GetMarketplace(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"plugins": []string{}})
}
func (h *PluginHandler) Install(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "installed"})
}
func (h *PluginHandler) GetInstalled(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"installed": []string{}})
}
func (h *PluginHandler) Enable(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "enabled"})
}
func (h *PluginHandler) Uninstall(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
func (h *PluginHandler) Publish(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusCreated, "Success", gin.H{"message": "published"})
}
func (h *PluginHandler) GetReviews(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"reviews": []string{}})
}
func (h *PluginHandler) PostReview(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusCreated, "Success", gin.H{"message": "review posted"})
}
