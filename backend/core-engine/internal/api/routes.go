package api

import (
	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/api/handlers"
	"github.com/sribash/world-simulation-engine/core-engine/internal/api/middleware"
	coreServices "github.com/sribash/world-simulation-engine/core-engine/internal/core/services"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/events"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/postgres"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/storage"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/websocket"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
	"github.com/sribash/world-simulation-engine/core-engine/internal/services"
)

func RegisterRestRoutes(r *gin.Engine, jwtSecret string, wsHub *websocket.Hub, storageProvider storage.Provider, eventDispatcher events.Dispatcher) {
	// Initialize Repositories
	userRepo := postgres.NewUserRepository(infrastructure.DB)
	orgRepo := postgres.NewOrgRepository(infrastructure.DB)
	roleRepo := postgres.NewRoleRepository(infrastructure.DB)
	apiKeyRepo := postgres.NewApiKeyRepository(infrastructure.DB)
	orgInviteRepo := postgres.NewOrgInviteRepository(infrastructure.DB)
	mfaRepo := postgres.NewMfaRepository(infrastructure.DB)

	// Initialize Services
	authService := coreServices.NewAuthService(userRepo, orgRepo, apiKeyRepo, mfaRepo, jwtSecret)
	orgService := coreServices.NewOrgService(userRepo, orgInviteRepo, roleRepo)
	userService := coreServices.NewUserService(userRepo)

	// Initialize Handlers
	authHandler := handlers.NewAuthHandler(authService)
	orgHandler := handlers.NewOrgHandler(orgService)
	userHandler := handlers.NewUserHandler(userService)
	// Phase 3 DI: Repositories
	simRepo := repositories.NewSimulationRepository(infrastructure.DB)
	marketRepo := repositories.NewMarketRepository(infrastructure.DB)
	mlopsRepo := repositories.NewMlopsRepository(infrastructure.DB)
	billingRepo := repositories.NewBillingRepository(infrastructure.DB)
	systemRepo := repositories.NewSystemRepository(infrastructure.DB)
	gisRepo := repositories.NewGisRepository(infrastructure.DB)
	collabRepo := repositories.NewCollabRepository(infrastructure.DB)
	chatRepo := repositories.NewChatRepository(infrastructure.DB)
	pluginsRepo := repositories.NewPluginsRepository(infrastructure.DB)

	// Phase 3 DI: Services
	simService := services.NewSimulationService(simRepo)
	marketService := services.NewMarketService(marketRepo)
	mlopsService := services.NewMlopsService(mlopsRepo)
	billingService := services.NewBillingService(billingRepo)
	systemService := services.NewSystemService(systemRepo)
	gisService := services.NewGisService(gisRepo)
	collabService := services.NewCollabService(collabRepo)
	chatService := services.NewChatService(chatRepo)
	pluginsService := services.NewPluginsService(pluginsRepo)

	simHandler := handlers.NewSimulationHandler(simService)
	marketHandler := handlers.NewMarketHandler(marketService)
	mlopsHandler := handlers.NewMlopsHandler(mlopsService)
	billingHandler := handlers.NewBillingHandler(billingService)
	systemHandler := handlers.NewSystemHandler(systemService)
	gisHandler := handlers.NewGisHandler(gisService)
	collabHandler := handlers.NewCollabHandler(collabService)
	chatHandler := handlers.NewChatHandler(chatService)
	pluginHandler := handlers.NewPluginHandler(pluginsService)

	v1 := r.Group("/api/v1")
	{
		// Public Auth routes
		auth := v1.Group("/auth")
		{
			auth.POST("/login", authHandler.Login)
			auth.POST("/register", authHandler.Register)
			auth.POST("/mfa/verify", authHandler.VerifyMFA)
		}

		// Protected V1 routes
		protected := v1.Group("")
		protected.Use(middleware.AuthMiddleware(jwtSecret))
		{
			// 1. Identity & Access API (12 Endpoints)
			protected.GET("/auth/users", authHandler.GetAllUsers)
			protected.POST("/auth/api-keys/generate", authHandler.GenerateApiKey)
			protected.GET("/auth/api-keys", authHandler.GetApiKeys)
			protected.DELETE("/auth/api-keys/:id", authHandler.RevokeApiKey)
			protected.GET("/users/:id/profile", userHandler.GetProfile)
			protected.DELETE("/users/:id", userHandler.DeleteUser)
			protected.PUT("/orgs/:id/roles", orgHandler.UpdateRoles)
			protected.GET("/orgs/:id/members", orgHandler.GetMembers)
			protected.POST("/orgs/:id/invites", orgHandler.CreateInvite)

			// 2. Simulation Core API (18 Endpoints)
			protected.POST("/simulations/run", simHandler.Run)
			protected.GET("/simulations/:id/status", simHandler.GetStatus)
			protected.POST("/simulations/:id/pause", simHandler.Pause)
			protected.POST("/scenarios/:id/branch", simHandler.BranchScenario)
			protected.GET("/simulations/:id/results", simHandler.GetResults)
			protected.GET("/simulations", simHandler.List)
			protected.DELETE("/simulations/:id", simHandler.Delete)
			protected.POST("/simulations/:id/resume", simHandler.Resume)
			protected.POST("/simulations/:id/stop", simHandler.Stop)
			protected.GET("/simulations/:id/logs", simHandler.GetLogs)
			protected.GET("/simulations/:id/metrics", simHandler.GetMetrics)
			protected.GET("/simulations/:id/scenarios", simHandler.GetScenarios)
			protected.GET("/scenarios/:id", simHandler.GetScenario)
			protected.PUT("/scenarios/:id", simHandler.UpdateScenario)
			protected.DELETE("/scenarios/:id", simHandler.DeleteScenario)
			protected.GET("/simulations/:id/predictions", simHandler.GetPredictions)
			protected.POST("/simulations/:id/export", simHandler.Export)
			protected.GET("/simulations/templates", simHandler.GetTemplates)

			// 3. Market & Data Pipeline API (15 Endpoints)
			protected.GET("/data/economic-indicators", marketHandler.GetEconomicIndicators)
			protected.GET("/data/climate-sensors", marketHandler.GetClimateSensors)
			protected.POST("/data/ingest-custom", marketHandler.IngestCustom)
			protected.POST("/market/predict-crash", marketHandler.PredictCrash)
			protected.GET("/market/sentiment-score", marketHandler.GetSentimentScore)
			protected.GET("/data/political", marketHandler.GetPolitical)
			protected.GET("/data/business", marketHandler.GetBusiness)
			protected.GET("/data/demographics", marketHandler.GetDemographics)
			protected.POST("/data/sync-airflow", marketHandler.SyncAirflow)
			protected.GET("/data/sources", marketHandler.GetSources)
			protected.POST("/data/sources", marketHandler.CreateSource)
			protected.PUT("/data/sources/:id", marketHandler.UpdateSource)
			protected.DELETE("/data/sources/:id", marketHandler.DeleteSource)
			protected.GET("/market/historical", marketHandler.GetHistorical)
			protected.GET("/market/volatility", marketHandler.GetVolatility)

			// 4. MLOps & Model Registry API (10 Endpoints)
			protected.POST("/models/upload-weights", mlopsHandler.UploadWeights)
			protected.GET("/models/:id/metrics", mlopsHandler.GetMetrics)
			protected.PUT("/models/:id/version/promote", mlopsHandler.PromoteVersion)
			protected.POST("/datasets/s3-sync", mlopsHandler.S3Sync)
			protected.DELETE("/models/:id/rollback", mlopsHandler.Rollback)
			protected.GET("/models", mlopsHandler.ListModels)
			protected.GET("/models/:id", mlopsHandler.GetModel)
			protected.DELETE("/models/:id", mlopsHandler.DeleteModel)
			protected.GET("/datasets", mlopsHandler.ListDatasets)
			protected.DELETE("/datasets/:id", mlopsHandler.DeleteDataset)

			// 5. Billing & Subscriptions API (8 Endpoints)
			protected.GET("/billing/compute-usage", billingHandler.GetComputeUsage)
			protected.POST("/billing/checkout-session", billingHandler.CheckoutSession)
			protected.GET("/billing/invoices/latest", billingHandler.GetLatestInvoices)
			protected.PUT("/billing/tier/upgrade", billingHandler.UpgradeTier)
			protected.POST("/billing/stripe-webhook", billingHandler.StripeWebhook)
			protected.GET("/billing/subs", billingHandler.ListSubs)
			protected.DELETE("/billing/subs/:id", billingHandler.CancelSub)
			protected.GET("/billing/methods", billingHandler.GetMethods)

			// 6. System & Integration API (14 Endpoints)
			protected.POST("/webhooks/register", systemHandler.RegisterWebhook)
			protected.GET("/system/health", systemHandler.GetHealth)
			protected.GET("/system/audit-logs", systemHandler.GetAuditLogs)
			protected.GET("/stream/sse", systemHandler.SseStream)
			protected.DELETE("/compliance/gdpr-purge", systemHandler.GdprPurge)
			protected.GET("/webhooks", systemHandler.ListWebhooks)
			protected.DELETE("/webhooks/:id", systemHandler.DeleteWebhook)
			protected.PUT("/webhooks/:id", systemHandler.UpdateWebhook)
			protected.POST("/webhooks/test", systemHandler.TestWebhook)
			protected.GET("/system/metrics", systemHandler.GetMetrics)
			protected.POST("/system/maintenance", systemHandler.Maintenance)
			protected.GET("/compliance/logs", systemHandler.GetComplianceLogs)
			protected.POST("/compliance/export", systemHandler.ExportCompliance)
			protected.GET("/system/alerts", systemHandler.GetAlerts)
		}
	}

	v2 := r.Group("/api/v2")
	{
		protected := v2.Group("")
		protected.Use(middleware.AuthMiddleware(jwtSecret))
		{
			// 7. V2: 3D GIS & Mapping API (6 Endpoints)
			protected.GET("/gis/tiles/:z/:x/:y", gisHandler.GetTiles)
			protected.GET("/gis/heatmaps/climate", gisHandler.GetHeatmaps)
			protected.POST("/gis/layers/custom", gisHandler.CreateCustomLayer)
			protected.GET("/gis/topology", gisHandler.GetTopology)
			protected.GET("/gis/markers", gisHandler.GetMarkers)
			protected.DELETE("/gis/layers/:id", gisHandler.DeleteLayer)

			// 8. V2: Real-Time Collab API (5 Endpoints)
			protected.POST("/collab/sessions", collabHandler.CreateSession)
			protected.GET("/collab/active-users", collabHandler.GetActiveUsers)
			protected.PUT("/collab/cursors", collabHandler.UpdateCursors)
			protected.POST("/collab/messages", collabHandler.PostMessage)
			protected.DELETE("/collab/sessions/:id", collabHandler.DeleteSession)

			// 9. V2: GenAI Chat API (6 Endpoints)
			protected.POST("/chat/completions", chatHandler.Completions)
			protected.GET("/chat/history", chatHandler.GetHistory)
			protected.POST("/chat/rag-sync", chatHandler.RagSync)
			protected.GET("/chat/prompts", chatHandler.GetPrompts)
			protected.DELETE("/chat/threads/:id", chatHandler.DeleteThread)
			protected.POST("/chat/feedback", chatHandler.Feedback)

			// 10. V2: Plugin Marketplace API (8 Endpoints)
			protected.GET("/plugins/marketplace", pluginHandler.GetMarketplace)
			protected.POST("/plugins/install", pluginHandler.Install)
			protected.GET("/plugins/installed", pluginHandler.GetInstalled)
			protected.PUT("/plugins/:id/enable", pluginHandler.Enable)
			protected.DELETE("/plugins/:id/uninstall", pluginHandler.Uninstall)
			protected.POST("/plugins/publish", pluginHandler.Publish)
			protected.GET("/plugins/:id/reviews", pluginHandler.GetReviews)
			protected.POST("/plugins/:id/reviews", pluginHandler.PostReview)
		}
	}
}
