from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class DynamicBayesianNetwork:
    """
    Computes probabilities for macro events (e.g. Recession Risk) 
    based on dynamic factors like GDP, Inflation, Oil, War, Trade, Debt.
    """
    def __init__(self):
        self.model = BayesianNetwork([
            ('War', 'Oil'),
            ('Trade', 'GDP'),
            ('Oil', 'Inflation'),
            ('Inflation', 'Recession'),
            ('GDP', 'Recession'),
            ('Debt', 'Recession')
        ])
        
        # CPD for War (True=1, False=0)
        cpd_war = TabularCPD(variable='War', variable_card=2, values=[[0.9], [0.1]])
        
        # CPD for Trade Tension (High=1, Low=0)
        cpd_trade = TabularCPD(variable='Trade', variable_card=2, values=[[0.7], [0.3]])
        
        # CPD for Debt (High=1, Low=0)
        cpd_debt = TabularCPD(variable='Debt', variable_card=2, values=[[0.6], [0.4]])
        
        # CPD for Oil (High=1, Low=0) given War
        cpd_oil = TabularCPD(variable='Oil', variable_card=2, 
                             values=[[0.8, 0.2], 
                                     [0.2, 0.8]],
                             evidence=['War'], evidence_card=[2])
                             
        # CPD for GDP (Drop=1, Growth=0) given Trade
        cpd_gdp = TabularCPD(variable='GDP', variable_card=2,
                             values=[[0.8, 0.4],
                                     [0.2, 0.6]],
                             evidence=['Trade'], evidence_card=[2])
                             
        # CPD for Inflation (High=1, Low=0) given Oil
        cpd_inflation = TabularCPD(variable='Inflation', variable_card=2,
                                   values=[[0.9, 0.3],
                                           [0.1, 0.7]],
                                   evidence=['Oil'], evidence_card=[2])
                                   
        # CPD for Recession (Yes=1, No=0) given Inflation, GDP, Debt
        # 2 * 2 * 2 = 8 columns
        # Order: Inflation (0,0,0,0,1,1,1,1), GDP (0,0,1,1,0,0,1,1), Debt (0,1,0,1,0,1,0,1)
        cpd_recession = TabularCPD(variable='Recession', variable_card=2,
                                   values=[
                                       [0.95, 0.8, 0.6, 0.4, 0.5, 0.3, 0.2, 0.05], # Prob of No Recession
                                       [0.05, 0.2, 0.4, 0.6, 0.5, 0.7, 0.8, 0.95]  # Prob of Recession
                                   ],
                                   evidence=['Inflation', 'GDP', 'Debt'], evidence_card=[2, 2, 2])
                                   
        self.model.add_cpds(cpd_war, cpd_trade, cpd_debt, cpd_oil, cpd_gdp, cpd_inflation, cpd_recession)
        assert self.model.check_model()
        self.inference = VariableElimination(self.model)
        
    def calculate_recession_risk(self, evidence=None):
        """
        Calculate the probability of a recession.
        Evidence is a dict, e.g., {'War': 1, 'Debt': 1}
        """
        if evidence is None:
            evidence = {}
            
        result = self.inference.query(variables=['Recession'], evidence=evidence)
        # Returns the probability of Recession=1
        return result.values[1]

if __name__ == "__main__":
    dbn = DynamicBayesianNetwork()
    risk_base = dbn.calculate_recession_risk()
    print(f"Base Recession Risk: {risk_base*100:.1f}%")
    
    risk_war = dbn.calculate_recession_risk({'War': 1})
    print(f"Recession Risk with WAR: {risk_war*100:.1f}%")
    
    risk_all = dbn.calculate_recession_risk({'War': 1, 'Debt': 1, 'Trade': 1})
    print(f"Recession Risk with WAR, DEBT, TRADE TENSION: {risk_all*100:.1f}%")
