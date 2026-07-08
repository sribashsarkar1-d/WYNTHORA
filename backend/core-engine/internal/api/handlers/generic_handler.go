package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/postgres"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
)

type GenericHandler[T any] struct {
	repo *postgres.GenericRepo[T]
}

func NewGenericHandler[T any](repo *postgres.GenericRepo[T]) *GenericHandler[T] {
	return &GenericHandler[T]{repo: repo}
}

func (h *GenericHandler[T]) Create(c *gin.Context) {
	var entity T
	if err := c.ShouldBindJSON(&entity); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	if err := h.repo.Create(c.Request.Context(), &entity); err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusCreated, "Success", entity)
}

func (h *GenericHandler[T]) GetByID(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid uuid", nil)
		return
	}

	entity, err := h.repo.GetByID(c.Request.Context(), id)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}
	if entity == nil {
		utils.RespondError(c, http.StatusNotFound, "ERROR", "record not found", nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", entity)
}

func (h *GenericHandler[T]) List(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "20")
	offsetStr := c.DefaultQuery("offset", "0")

	limit, _ := strconv.Atoi(limitStr)
	offset, _ := strconv.Atoi(offsetStr)

	// Optional: extract org_id from query or context to enforce tenancy
	conditions := make(map[string]interface{})
	if orgID := c.Query("org_id"); orgID != "" {
		conditions["org_id = ?"] = orgID
	}

	entities, err := h.repo.List(c.Request.Context(), limit, offset, conditions)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"data": entities, "limit": limit, "offset": offset})
}

func (h *GenericHandler[T]) Update(c *gin.Context) {
	idStr := c.Param("id")
	_, err := uuid.Parse(idStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid uuid", nil)
		return
	}

	var entity T
	if err := c.ShouldBindJSON(&entity); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	// Assuming the JSON body doesn't contain ID, we should technically set it.
	// But in a pure generic handler, reflection would be needed to set ID securely.
	// For now, we trust the JSON payload includes the correct ID matching the path.

	if err := h.repo.Update(c.Request.Context(), &entity); err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", entity)
}

func (h *GenericHandler[T]) Delete(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid uuid", nil)
		return
	}

	if err := h.repo.Delete(c.Request.Context(), id); err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
