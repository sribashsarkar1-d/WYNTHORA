package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
)

type AuthHandler struct {
	authService ports.AuthService
}

func NewAuthHandler(authService ports.AuthService) *AuthHandler {
	return &AuthHandler{authService: authService}
}

func (h *AuthHandler) Login(c *gin.Context) {
	var req struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	token, err := h.authService.Login(c.Request.Context(), req.Email, req.Password)
	if err != nil {
		utils.RespondError(c, http.StatusUnauthorized, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"token": token})
}

func (h *AuthHandler) Register(c *gin.Context) {
	var req struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
		OrgName  string `json:"orgName"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	user, err := h.authService.Register(c.Request.Context(), req.Email, req.Password, req.OrgName)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusCreated, "Success", map[string]interface{}{"user_id": user.ID})
}

func (h *AuthHandler) VerifyMFA(c *gin.Context) {
	var req struct {
		UserID string `json:"user_id" binding:"required"`
		Code   string `json:"code" binding:"required"`
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

	token, err := h.authService.VerifyMFA(c.Request.Context(), uid, req.Code)
	if err != nil {
		utils.RespondError(c, http.StatusUnauthorized, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"token": token})
}

func (h *AuthHandler) GenerateApiKey(c *gin.Context) {
	var req struct {
		Name string `json:"name" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", err.Error(), nil)
		return
	}

	userID, _ := c.Get("userID")
	uid, ok := userID.(uuid.UUID)
	if !ok {
		utils.RespondError(c, http.StatusUnauthorized, "ERROR", "unauthorized", nil)
		return
	}

	key, err := h.authService.GenerateApiKey(c.Request.Context(), uid, req.Name)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusCreated, "Success", map[string]interface{}{"api_key": key})
}

func (h *AuthHandler) GetApiKeys(c *gin.Context) {
	userID, _ := c.Get("userID")
	uid, ok := userID.(uuid.UUID)
	if !ok {
		utils.RespondError(c, http.StatusUnauthorized, "ERROR", "unauthorized", nil)
		return
	}

	keys, err := h.authService.GetApiKeys(c.Request.Context(), uid)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"api_keys": keys})
}

func (h *AuthHandler) RevokeApiKey(c *gin.Context) {
	keyIDStr := c.Param("id")
	keyID, err := uuid.Parse(keyIDStr)
	if err != nil {
		utils.RespondError(c, http.StatusBadRequest, "ERROR", "invalid key id", nil)
		return
	}

	err = h.authService.RevokeApiKey(c.Request.Context(), keyID)
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}

func (h *AuthHandler) GetAllUsers(c *gin.Context) {
	users, err := h.authService.GetAllUsers(c.Request.Context())
	if err != nil {
		utils.RespondError(c, http.StatusInternalServerError, "ERROR", err.Error(), nil)
		return
	}

	// Normally we'd use a DTO to not expose password hashes
	// For brevity, we map to simple responses
	var resp []map[string]interface{}
	for _, u := range users {
		resp = append(resp, map[string]interface{}{
			"id":        u.ID,
			"email":     u.Email,
			"org_id":    u.OrgID,
			"role_id":   u.RoleID,
			"is_active": u.IsActive,
		})
	}

	utils.RespondSuccess(c, http.StatusOK, "Success", map[string]interface{}{"users": resp})
}
