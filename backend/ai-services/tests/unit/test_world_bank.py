import pytest
from app.plugins.world_bank import WorldBankPlugin

@pytest.mark.asyncio
async def test_world_bank_health():
    plugin = WorldBankPlugin()
    is_healthy = await plugin.health_check()
    assert is_healthy is True

@pytest.mark.asyncio
async def test_world_bank_normalize_and_validate():
    plugin = WorldBankPlugin(indicator_code="NY.GDP.MKTP.CD")
    
    # Mock data structure matching World Bank API
    mock_raw_data = [
        {"page": 1, "pages": 1, "per_page": 50, "total": 1},
        [
            {
                "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
                "country": {"id": "US", "value": "United States"},
                "countryiso3code": "USA",
                "date": "2023",
                "value": 27360000000.0,
                "unit": "",
                "obs_status": "",
                "decimal": 0
            },
            {
                "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
                "country": {"id": "US", "value": "United States"},
                "countryiso3code": "USA",
                "date": "2023",
                "value": -5000.0, # Invalid negative GDP
                "unit": "",
                "obs_status": "",
                "decimal": 0
            }
        ]
    ]
    
    normalized = plugin.normalize(mock_raw_data)
    assert len(normalized) == 2
    assert normalized[0].country_code == "US"
    assert normalized[0].value == 27360000000.0
    
    # Validate should filter out the negative GDP
    is_valid = plugin.validate(normalized)
    assert is_valid is True
    assert len(plugin.validated_data) == 1
    assert plugin.validated_data[0].value > 0
