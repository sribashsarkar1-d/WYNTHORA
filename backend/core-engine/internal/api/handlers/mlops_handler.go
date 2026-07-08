package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type MlopsHandler struct {
	Service services.MlopsService
}

func NewMlopsHandler(svc services.MlopsService) *MlopsHandler {
	return &MlopsHandler{Service: svc}
}

func (h *MlopsHandler) UploadWeights(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "weights uploaded"})
}
func (h *MlopsHandler) GetMetrics(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"metrics": map[string]interface{}{}})
}
func (h *MlopsHandler) PromoteVersion(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "version promoted"})
}
func (h *MlopsHandler) S3Sync(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "s3 sync started"})
}
func (h *MlopsHandler) Rollback(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
func (h *MlopsHandler) ListModels(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"models": []string{}})
}
func (h *MlopsHandler) GetModel(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"model": map[string]interface{}{}})
}
func (h *MlopsHandler) DeleteModel(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
func (h *MlopsHandler) ListDatasets(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"datasets": []string{}})
}
func (h *MlopsHandler) DeleteDataset(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
