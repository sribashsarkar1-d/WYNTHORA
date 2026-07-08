package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type GisHandler struct {
	Service services.GisService
}

func NewGisHandler(svc services.GisService) *GisHandler {
	return &GisHandler{Service: svc}
}

func (h *GisHandler) GetTiles(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"tile": "data"})
}
func (h *GisHandler) GetHeatmaps(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"heatmaps": []string{}})
}
func (h *GisHandler) CreateCustomLayer(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusCreated, "Success", gin.H{"message": "layer created"})
}
func (h *GisHandler) GetTopology(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"topology": map[string]interface{}{}})
}
func (h *GisHandler) GetMarkers(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"markers": []string{}})
}
func (h *GisHandler) DeleteLayer(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
