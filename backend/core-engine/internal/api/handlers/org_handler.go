package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
)

type OrgHandler struct {
	orgService ports.OrgService
}

func NewOrgHandler(orgService ports.OrgService) *OrgHandler {
	return &OrgHandler{orgService: orgService}
}

func (h *OrgHandler) GetMembers(c *gin.Context) {
	orgIDStr := c.Param("id")
	orgID, err := uuid.Parse(orgIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid org id", nil)
		return
	}

	members, err := h.orgService.GetMembers(c.Request.Context(), orgID)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	var resp []map[string]interface{}
	for _, m := range members {
		resp = append(resp, map[string]interface{}{
			"id":        m.ID,
			"email":     m.Email,
			"role_id":   m.RoleID,
			"is_active": m.IsActive,
		})
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"members": resp})
}

func (h *OrgHandler) CreateInvite(c *gin.Context) {
	orgIDStr := c.Param("id")
	orgID, err := uuid.Parse(orgIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid org id", nil)
		return
	}

	var req struct {
		Email string `json:"email" binding:"required"`
		Role  string `json:"role"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	invite, err := h.orgService.CreateInvite(c.Request.Context(), orgID, req.Email, req.Role)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusCreated, "Success", map[string]interface{}{"invite": invite})
}

func (h *OrgHandler) UpdateRoles(c *gin.Context) {
	orgIDStr := c.Param("id")
	orgID, err := uuid.Parse(orgIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid org id", nil)
		return
	}

	var req struct {
		UserID string `json:"user_id" binding:"required"`
		Role   string `json:"role" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	uid, err := uuid.Parse(req.UserID)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid user id", nil)
		return
	}

	err = h.orgService.UpdateUserRole(c.Request.Context(), orgID, uid, req.Role)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
