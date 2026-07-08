package domain

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type AiModels struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID        *uuid.UUID `gorm:"column:org_id"`
	Name         string     `gorm:"column:name"`
	Architecture string     `gorm:"column:architecture"`
	IsActive     bool       `gorm:"column:is_active"`
	CreatedAt    *time.Time `gorm:"column:created_at"`
}

func (m *AiModels) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type AuditLogs struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	UserID     *uuid.UUID `gorm:"column:user_id"`
	OrgID      *uuid.UUID `gorm:"column:org_id"`
	Action     string     `gorm:"column:action"`
	IpAddress  string     `gorm:"column:ip_address"`
	UserAgent  string     `gorm:"column:user_agent"`
	ResourceID *uuid.UUID `gorm:"column:resource_id"`
	Timestamp  *time.Time `gorm:"column:timestamp"`
}

func (m *AuditLogs) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type ClimateTimeSeries struct {
	Time           time.Time `gorm:"column:time"`
	IsoCode        string    `gorm:"column:iso_code"`
	AvgTempCelsius *float64  `gorm:"column:avg_temp_celsius"`
	Co2Ppm         *float64  `gorm:"column:co2_ppm"`
	SeaLevelRiseMm *float64  `gorm:"column:sea_level_rise_mm"`
}

type CollabCursors struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	SessionID   *uuid.UUID `gorm:"column:session_id"`
	UserID      *uuid.UUID `gorm:"column:user_id"`
	PosX        *float64   `gorm:"column:pos_x"`
	PosY        *float64   `gorm:"column:pos_y"`
	LastUpdated *time.Time `gorm:"column:last_updated"`
}

func (m *CollabCursors) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type CollabSessions struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	RequestID *uuid.UUID `gorm:"column:request_id"`
	StartedBy *uuid.UUID `gorm:"column:started_by"`
	IsActive  bool       `gorm:"column:is_active"`
	CreatedAt *time.Time `gorm:"column:created_at"`
}

func (m *CollabSessions) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type ComputeUsageLogs struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID          *uuid.UUID `gorm:"column:org_id"`
	RequestID      *uuid.UUID `gorm:"column:request_id"`
	ComputeMinutes float64    `gorm:"column:compute_minutes"`
	GpuType        string     `gorm:"column:gpu_type"`
	CostIncurred   float64    `gorm:"column:cost_incurred"`
	LoggedAt       *time.Time `gorm:"column:logged_at"`
}

func (m *ComputeUsageLogs) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Countries struct {
	IsoCode string `gorm:"column:iso_code"`
	Name    string `gorm:"column:name"`
	Region  string `gorm:"column:region"`
}

type DataSources struct {
	ID                 uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	Name               string    `gorm:"column:name"`
	ApiEndpoint        string    `gorm:"column:api_endpoint"`
	AuthConfig         string    `gorm:"column:auth_config"`
	RefreshRateSeconds int       `gorm:"column:refresh_rate_seconds"`
}

func (m *DataSources) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type EconomicTimeSeries struct {
	Time          time.Time `gorm:"column:time"`
	IsoCode       string    `gorm:"column:iso_code"`
	GdpUsd        *float64  `gorm:"column:gdp_usd"`
	InflationRate *float64  `gorm:"column:inflation_rate"`
	InterestRate  *float64  `gorm:"column:interest_rate"`
	DebtToGdp     *float64  `gorm:"column:debt_to_gdp"`
}

type GeopoliticalEvents struct {
	ID          uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	IsoCode     string    `gorm:"column:iso_code"`
	EventType   string    `gorm:"column:event_type"`
	Severity    int       `gorm:"column:severity"`
	Description string    `gorm:"column:description"`
	EventDate   time.Time `gorm:"column:event_date"`
}

func (m *GeopoliticalEvents) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type GisTopologyLayers struct {
	ID            uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	Name          string     `gorm:"column:name"`
	LayerType     string     `gorm:"column:layer_type"`
	S3GeojsonPath string     `gorm:"column:s3_geojson_path"`
	UpdatedAt     *time.Time `gorm:"column:updated_at"`
}

func (m *GisTopologyLayers) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type InvoiceLedgers struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID              *uuid.UUID `gorm:"column:org_id"`
	StripeInvoiceID    string     `gorm:"column:stripe_invoice_id"`
	AmountDue          float64    `gorm:"column:amount_due"`
	Currency           string     `gorm:"column:currency"`
	Status             string     `gorm:"column:status"`
	BillingPeriodStart *time.Time `gorm:"column:billing_period_start"`
	BillingPeriodEnd   *time.Time `gorm:"column:billing_period_end"`
	IssuedAt           *time.Time `gorm:"column:issued_at"`
}

func (m *InvoiceLedgers) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type MarketTickData struct {
	Time            time.Time `gorm:"column:time"`
	TickerID        uuid.UUID `gorm:"column:ticker_id"`
	PriceOpen       *float64  `gorm:"column:price_open"`
	PriceClose      *float64  `gorm:"column:price_close"`
	PriceHigh       *float64  `gorm:"column:price_high"`
	PriceLow        *float64  `gorm:"column:price_low"`
	Volume          string    `gorm:"column:volume"`
	VolatilityIndex *float64  `gorm:"column:volatility_index"`
}

type MarketTickers struct {
	ID          uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	Symbol      string    `gorm:"column:symbol"`
	CompanyName string    `gorm:"column:company_name"`
	Sector      string    `gorm:"column:sector"`
	Exchange    string    `gorm:"column:exchange"`
}

func (m *MarketTickers) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type ModelDeployments struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	VersionID   *uuid.UUID `gorm:"column:version_id"`
	Environment string     `gorm:"column:environment"`
	DeployedBy  *uuid.UUID `gorm:"column:deployed_by"`
	DeployedAt  *time.Time `gorm:"column:deployed_at"`
}

func (m *ModelDeployments) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type ModelVersions struct {
	ID            uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	ModelID       *uuid.UUID `gorm:"column:model_id"`
	VersionTag    string     `gorm:"column:version_tag"`
	DatasetID     *uuid.UUID `gorm:"column:dataset_id"`
	S3WeightsPath string     `gorm:"column:s3_weights_path"`
	AccuracyScore *float64   `gorm:"column:accuracy_score"`
	LossMetrics   string     `gorm:"column:loss_metrics"`
	CreatedAt     *time.Time `gorm:"column:created_at"`
}

func (m *ModelVersions) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type NewsSentimentLogs struct {
	ID              uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	Source          string    `gorm:"column:source"`
	Headline        string    `gorm:"column:headline"`
	FinbertScore    *float64  `gorm:"column:finbert_score"`
	ImpactedTickers string    `gorm:"column:impacted_tickers"`
	PublishedAt     time.Time `gorm:"column:published_at"`
}

func (m *NewsSentimentLogs) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Notifications struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	UserID    *uuid.UUID `gorm:"column:user_id"`
	Type      string     `gorm:"column:type"`
	Title     string     `gorm:"column:title"`
	Message   string     `gorm:"column:message"`
	IsRead    bool       `gorm:"column:is_read"`
	CreatedAt *time.Time `gorm:"column:created_at"`
}

func (m *Notifications) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type OauthTokens struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	UserID       *uuid.UUID `gorm:"column:user_id"`
	Provider     string     `gorm:"column:provider"`
	AccessToken  string     `gorm:"column:access_token"`
	RefreshToken string     `gorm:"column:refresh_token"`
	ExpiresAt    time.Time  `gorm:"column:expires_at"`
}

func (m *OauthTokens) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type OrgPlugins struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID       *uuid.UUID `gorm:"column:org_id"`
	PluginID    *uuid.UUID `gorm:"column:plugin_id"`
	IsEnabled   bool       `gorm:"column:is_enabled"`
	InstalledAt *time.Time `gorm:"column:installed_at"`
}

func (m *OrgPlugins) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type PaymentMethods struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID      *uuid.UUID `gorm:"column:org_id"`
	StripePmID string     `gorm:"column:stripe_pm_id"`
	CardLast4  string     `gorm:"column:card_last4"`
	CardBrand  string     `gorm:"column:card_brand"`
	IsDefault  bool       `gorm:"column:is_default"`
}

func (m *PaymentMethods) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Permissions struct {
	ID       uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	RoleID   *uuid.UUID `gorm:"column:role_id"`
	Resource string     `gorm:"column:resource"`
	Action   string     `gorm:"column:action"`
}

func (m *Permissions) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type PipelineRuns struct {
	ID              uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	SourceID        *uuid.UUID `gorm:"column:source_id"`
	Status          string     `gorm:"column:status"`
	RecordsIngested int        `gorm:"column:records_ingested"`
	ErrorLog        string     `gorm:"column:error_log"`
	StartedAt       *time.Time `gorm:"column:started_at"`
	CompletedAt     *time.Time `gorm:"column:completed_at"`
}

func (m *PipelineRuns) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Plugins struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	DeveloperID  *uuid.UUID `gorm:"column:developer_id"`
	Name         string     `gorm:"column:name"`
	Version      string     `gorm:"column:version"`
	Description  string     `gorm:"column:description"`
	S3BundlePath string     `gorm:"column:s3_bundle_path"`
	IsApproved   bool       `gorm:"column:is_approved"`
	CreatedAt    *time.Time `gorm:"column:created_at"`
}

func (m *Plugins) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Predictions struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	ResultID           *uuid.UUID `gorm:"column:result_id"`
	Domain             string     `gorm:"column:domain"`
	Metric             string     `gorm:"column:metric"`
	PredictedValue     *float64   `gorm:"column:predicted_value"`
	ConfidenceInterval string     `gorm:"column:confidence_interval"`
}

func (m *Predictions) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Scenarios struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	RequestID        *uuid.UUID `gorm:"column:request_id"`
	ParentScenarioID *uuid.UUID `gorm:"column:parent_scenario_id"`
	Name             string     `gorm:"column:name"`
	Variables        string     `gorm:"column:variables"`
	ProbabilityScore *float64   `gorm:"column:probability_score"`
	CreatedAt        *time.Time `gorm:"column:created_at"`
}

func (m *Scenarios) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type SimulationCheckpoints struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	RequestID   *uuid.UUID `gorm:"column:request_id"`
	TickNumber  string     `gorm:"column:tick_number"`
	StateHash   string     `gorm:"column:state_hash"`
	S3StatePath string     `gorm:"column:s3_state_path"`
	CreatedAt   *time.Time `gorm:"column:created_at"`
}

func (m *SimulationCheckpoints) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type SimulationRequests struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	UserID     *uuid.UUID `gorm:"column:user_id"`
	OrgID      *uuid.UUID `gorm:"column:org_id"`
	Name       string     `gorm:"column:name"`
	TargetYear int        `gorm:"column:target_year"`
	Status     string     `gorm:"column:status"`
	CreatedAt  *time.Time `gorm:"column:created_at"`
}

func (m *SimulationRequests) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type SimulationResults struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	RequestID  *uuid.UUID `gorm:"column:request_id"`
	ScenarioID *uuid.UUID `gorm:"column:scenario_id"`
	RawPayload string     `gorm:"column:raw_payload"`
	ComputedAt *time.Time `gorm:"column:computed_at"`
}

func (m *SimulationResults) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type Subscriptions struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID            *uuid.UUID `gorm:"column:org_id"`
	StripeSubID      string     `gorm:"column:stripe_sub_id"`
	PlanType         string     `gorm:"column:plan_type"`
	Status           string     `gorm:"column:status"`
	CurrentPeriodEnd time.Time  `gorm:"column:current_period_end"`
}

func (m *Subscriptions) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type SystemAlerts struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	Level       string     `gorm:"column:level"`
	ServiceName string     `gorm:"column:service_name"`
	Message     string     `gorm:"column:message"`
	IsResolved  bool       `gorm:"column:is_resolved"`
	CreatedAt   *time.Time `gorm:"column:created_at"`
}

func (m *SystemAlerts) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type TrainingDatasets struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	SourceID   *uuid.UUID `gorm:"column:source_id"`
	Name       string     `gorm:"column:name"`
	S3Path     string     `gorm:"column:s3_path"`
	NumRecords string     `gorm:"column:num_records"`
	CreatedAt  *time.Time `gorm:"column:created_at"`
}

func (m *TrainingDatasets) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type WebhookDeliveryHistories struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	EndpointID     *uuid.UUID `gorm:"column:endpoint_id"`
	EventType      string     `gorm:"column:event_type"`
	Payload        string     `gorm:"column:payload"`
	ResponseStatus int        `gorm:"column:response_status"`
	ResponseBody   string     `gorm:"column:response_body"`
	DeliveredAt    *time.Time `gorm:"column:delivered_at"`
}

func (m *WebhookDeliveryHistories) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}

type WebhookEndpoints struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey;column:id"`
	OrgID     *uuid.UUID `gorm:"column:org_id"`
	TargetUrl string     `gorm:"column:target_url"`
	SecretKey string     `gorm:"column:secret_key"`
	Events    string     `gorm:"column:events"`
	IsActive  bool       `gorm:"column:is_active"`
}

func (m *WebhookEndpoints) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}
