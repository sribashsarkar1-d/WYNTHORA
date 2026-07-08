package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"net/http"
)

type BillingHandler struct {
	Service services.BillingService
}

func NewBillingHandler(svc services.BillingService) *BillingHandler {
	return &BillingHandler{Service: svc}
}

func (h *BillingHandler) GetComputeUsage(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"usage": 100})
}
func (h *BillingHandler) CheckoutSession(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"session_id": "cs_test_123"})
}
func (h *BillingHandler) GetLatestInvoices(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"invoices": []string{}})
}
func (h *BillingHandler) UpgradeTier(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"message": "tier upgraded"})
}
func (h *BillingHandler) StripeWebhook(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"received": true})
}
func (h *BillingHandler) ListSubs(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"subs": []string{}})
}
func (h *BillingHandler) CancelSub(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusNoContent, "Deleted", nil)
}
func (h *BillingHandler) GetMethods(c *gin.Context) {
	utils.RespondSuccess(c, http.StatusOK, "Success", gin.H{"methods": []string{}})
}
