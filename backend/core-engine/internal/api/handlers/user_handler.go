package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
)

type UserHandler struct {
	userService ports.UserService
}

func NewUserHandler(userService ports.UserService) *UserHandler {
	return &UserHandler{userService: userService}
}

func (h *UserHandler) GetProfile(c *gin.Context) {
	userIDStr := c.Param("id")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid user id", nil)
		return
	}

	user, err := h.userService.GetProfile(c.Request.Context(), userID)
	if err != nil {
		utils.RespondError(c, http.StatusNotFound, "ERROR", "user not found", nil)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id":        user.ID,
		"email":     user.Email,
		"org_id":    user.OrgID,
		"role_id":   user.RoleID,
		"is_active": user.IsActive,
	})
}

func (h *UserHandler) DeleteUser(c *gin.Context) {
	userIDStr := c.Param("id")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid user id", nil)
		return
	}

	err = h.userService.DeleteUser(c.Request.Context(), userID)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
