import pytest
import torch
import asyncio
from app.contracts.economy import EconomicIndicatorContract
from app.feature_store.economy_features import EconomyFeatureStore
from app.domains.economy.finance.lstm_predictor import MarketLSTM
from app.ai.interfaces.base_agent import BaseAutonomousAgent
from app.ai.nlp.rag_pipeline import RAGPipeline

def test_feature_store_compute():
    fs = EconomyFeatureStore()
    
    # Mock data
    data = [
        EconomicIndicatorContract(country_code="US", year=2021, indicator_code="GDP_USD", value=100.0, source="WB"),
        EconomicIndicatorContract(country_code="US", year=2022, indicator_code="GDP_USD", value=150.0, source="WB"),
        EconomicIndicatorContract(country_code="US", year=2023, indicator_code="GDP_USD", value=200.0, source="WB")
    ]
    
    tensor = fs.compute_features(data)
    
    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (3, 1)
    
    # Check normalization: min is 100 (0.0), max is 200 (1.0), middle is 150 (0.5)
    assert tensor[0].item() == 0.0
    assert tensor[1].item() == 0.5
    assert tensor[2].item() == 1.0
    
def test_market_lstm_registry():
    model = MarketLSTM()
    
    # Mock input tensor of shape (batch, seq_len, features)
    # Our LSTM takes 5 features
    mock_features = torch.randn(1, 10, 5)
    mock_labels = torch.randn(1, 1)
    
    # Train
    metrics = model.train(mock_features, mock_labels, epochs=2)
    assert "loss" in metrics
    assert isinstance(metrics["loss"], float)
    
    # Predict
    prediction = model.predict(mock_features)
    assert prediction.shape == (1, 1)

class TestAgent(BaseAutonomousAgent):
    def perceive(self, world_state):
        self.memory.append(world_state)
        
    def reason(self, context):
        return f"Decided based on {context}"
        
    def act(self):
        return {"action": "buy"}

@pytest.mark.asyncio
async def test_agent_and_rag():
    agent = TestAgent("US_FED", "CentralBank")
    agent.perceive({"inflation": 0.05})
    assert len(agent.memory) == 1
    
    rag = RAGPipeline()
    context = await rag.get_context("What is the inflation?", "US")
    assert "inflation" in context.lower()
    
    decision = agent.reason(context)
    assert "Decided based on" in decision
    
    action = agent.act()
    assert action["action"] == "buy"
