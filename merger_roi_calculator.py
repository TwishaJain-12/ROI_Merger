"""
Merger ROI Calculator
Based on academic research and financial theory

References:
1. Damodaran, A. (2005). "The Value of Synergy" - NYU Stern
2. Bruner, R. F. (2004). "Applied Mergers and Acquisitions"
3. Koller, T., Goedhart, M., & Wessels, D. (2015). "Valuation: Measuring and Managing the Value of Companies"
"""

from typing import Dict, Tuple
import math


class MergerROICalculator:
    """
    Calculate Merger ROI using multiple academic methodologies
    """
    
    def __init__(self, discount_rate: float = 0.10, tax_rate: float = 0.25):
        """
        Initialize calculator with standard financial parameters
        
        Args:
            discount_rate: Weighted Average Cost of Capital (WACC) - typically 8-12%
            tax_rate: Corporate tax rate - typically 21-25%
        """
        self.discount_rate = discount_rate
        self.tax_rate = tax_rate
    
    def calculate_synergies(self, company_a: Dict, company_b: Dict, 
                           synergy_rate: float = 0.10) -> Dict:
        """
        Calculate operational and financial synergies
        
        Based on Damodaran (2005) synergy framework:
        - Operating synergies: Cost savings from economies of scale
        - Financial synergies: Tax benefits, lower cost of capital
        
        Args:
            company_a: Financial data for acquiring company
            company_b: Financial data for target company
            synergy_rate: Expected synergy as % of combined costs (default 10%)
        
        Returns:
            Dictionary with synergy breakdown
        """
        combined_costs = company_a['operating_costs'] + company_b['operating_costs']
        
        # Operating synergies (cost reduction)
        operating_synergies = combined_costs * synergy_rate
        
        # Financial synergies (tax shield from debt)
        combined_ebitda = company_a['ebitda'] + company_b['ebitda']
        tax_shield = combined_ebitda * self.tax_rate * 0.05  # 5% additional tax benefit
        
        # Revenue synergies (cross-selling, market expansion)
        combined_revenue = company_a['annual_revenue'] + company_b['annual_revenue']
        revenue_synergies = combined_revenue * 0.03  # 3% revenue increase
        
        total_synergies = operating_synergies + tax_shield + revenue_synergies
        
        return {
            'operating_synergies': operating_synergies,
            'financial_synergies': tax_shield,
            'revenue_synergies': revenue_synergies,
            'total_annual_synergies': total_synergies
        }
    
    def calculate_merger_cost(self, company_b: Dict, premium: float = 0.30) -> float:
        """
        Calculate total merger cost including acquisition premium
        
        Based on market practice: typical premium is 20-40% above market value
        
        Args:
            company_b: Target company data
            premium: Acquisition premium (default 30%)
        
        Returns:
            Total merger cost
        """
        base_cost = company_b['market_value']
        premium_cost = base_cost * premium
        transaction_costs = base_cost * 0.02  # 2% for legal, advisory fees
        
        total_cost = base_cost + premium_cost + transaction_costs
        
        return total_cost
    
    def calculate_npv(self, annual_synergies: float, merger_cost: float, 
                     years: int = 5) -> float:
        """
        Calculate Net Present Value of merger
        
        NPV = Σ(Synergies_t / (1 + r)^t) - Initial Investment
        
        Based on Koller et al. (2015) DCF methodology
        
        Args:
            annual_synergies: Expected annual synergies
            merger_cost: Total cost of merger
            years: Time horizon for analysis (default 5 years)
        
        Returns:
            Net Present Value
        """
        pv_synergies = 0
        for year in range(1, years + 1):
            # Synergies grow at 2% annually
            synergy_value = annual_synergies * (1.02 ** year)
            discount_factor = (1 + self.discount_rate) ** year
            pv_synergies += synergy_value / discount_factor
        
        npv = pv_synergies - merger_cost
        
        return npv
    
    def calculate_roi(self, annual_synergies: float, merger_cost: float) -> float:
        """
        Calculate simple ROI percentage
        
        ROI = (Total Benefits - Total Costs) / Total Costs × 100
        
        Using 5-year cumulative synergies
        
        Args:
            annual_synergies: Annual synergy value
            merger_cost: Total merger cost
        
        Returns:
            ROI percentage
        """
        # 5-year cumulative synergies with 2% growth
        total_benefits = sum(annual_synergies * (1.02 ** year) for year in range(1, 6))
        
        roi = ((total_benefits - merger_cost) / merger_cost) * 100
        
        return roi
    
    def calculate_payback_period(self, annual_synergies: float, 
                                 merger_cost: float) -> float:
        """
        Calculate payback period in years
        
        Time required to recover the initial investment
        
        Args:
            annual_synergies: Annual synergy value
            merger_cost: Total merger cost
        
        Returns:
            Payback period in years
        """
        if annual_synergies <= 0:
            return float('inf')
        
        cumulative = 0
        year = 0
        
        while cumulative < merger_cost and year < 20:
            year += 1
            synergy_value = annual_synergies * (1.02 ** year)
            cumulative += synergy_value
        
        return year if cumulative >= merger_cost else float('inf')
    
    def calculate_irr(self, annual_synergies: float, merger_cost: float, 
                     years: int = 5) -> float:
        """
        Calculate Internal Rate of Return
        
        IRR is the discount rate that makes NPV = 0
        
        Args:
            annual_synergies: Annual synergy value
            merger_cost: Initial investment
            years: Time horizon
        
        Returns:
            IRR as percentage
        """
        # Newton-Raphson method to find IRR
        irr_guess = 0.15  # Start with 15%
        tolerance = 0.0001
        max_iterations = 100
        
        for _ in range(max_iterations):
            npv = -merger_cost
            npv_derivative = 0
            
            for year in range(1, years + 1):
                synergy_value = annual_synergies * (1.02 ** year)
                discount_factor = (1 + irr_guess) ** year
                npv += synergy_value / discount_factor
                npv_derivative -= year * synergy_value / ((1 + irr_guess) ** (year + 1))
            
            if abs(npv) < tolerance:
                return irr_guess * 100
            
            irr_guess = irr_guess - npv / npv_derivative
            
            if irr_guess < -0.99:  # Prevent negative IRR below -99%
                irr_guess = -0.99
        
        return irr_guess * 100
    
    def analyze_merger(self, company_a: Dict, company_b: Dict, 
                      synergy_rate: float = 0.10, 
                      premium: float = 0.30) -> Dict:
        """
        Complete merger analysis with recommendation
        
        Args:
            company_a: Acquiring company financial data
            company_b: Target company financial data
            synergy_rate: Expected synergy rate (default 10%)
            premium: Acquisition premium (default 30%)
        
        Returns:
            Complete analysis with recommendation
        """
        # Calculate synergies
        synergies = self.calculate_synergies(company_a, company_b, synergy_rate)
        annual_synergies = synergies['total_annual_synergies']
        
        # Calculate merger cost
        merger_cost = self.calculate_merger_cost(company_b, premium)
        
        # Calculate financial metrics
        npv = self.calculate_npv(annual_synergies, merger_cost)
        roi = self.calculate_roi(annual_synergies, merger_cost)
        payback_period = self.calculate_payback_period(annual_synergies, merger_cost)
        irr = self.calculate_irr(annual_synergies, merger_cost)
        
        # Combined metrics
        combined_revenue = company_a['annual_revenue'] + company_b['annual_revenue']
        combined_ebitda = company_a['ebitda'] + company_b['ebitda'] + annual_synergies
        combined_assets = company_a['total_assets'] + company_b['total_assets']
        
        # Decision criteria based on academic research
        recommendation = self._make_recommendation(roi, npv, payback_period, irr)
        
        return {
            'company_a': company_a['company_name'],
            'company_b': company_b['company_name'],
            'merger_cost': round(merger_cost, 2),
            'synergies': {
                'operating': round(synergies['operating_synergies'], 2),
                'financial': round(synergies['financial_synergies'], 2),
                'revenue': round(synergies['revenue_synergies'], 2),
                'total_annual': round(annual_synergies, 2)
            },
            'financial_metrics': {
                'roi_percentage': round(roi, 2),
                'npv': round(npv, 2),
                'irr_percentage': round(irr, 2),
                'payback_period_years': round(payback_period, 2)
            },
            'combined_company': {
                'revenue': round(combined_revenue, 2),
                'ebitda': round(combined_ebitda, 2),
                'assets': round(combined_assets, 2)
            },
            'recommendation': recommendation['decision'],
            'confidence': recommendation['confidence'],
            'reasoning': recommendation['reasoning']
        }
    
    def _make_recommendation(self, roi: float, npv: float, 
                            payback_period: float, irr: float) -> Dict:
        """
        Make merger recommendation based on multiple criteria
        
        Decision framework based on Bruner (2004):
        - ROI > 20%: Strong positive
        - NPV > 0: Value creating
        - Payback < 5 years: Acceptable risk
        - IRR > WACC: Exceeds cost of capital
        
        Args:
            roi: Return on Investment percentage
            npv: Net Present Value
            payback_period: Payback period in years
            irr: Internal Rate of Return percentage
        
        Returns:
            Recommendation with confidence level
        """
        score = 0
        reasons = []
        
        # ROI criteria
        if roi > 30:
            score += 3
            reasons.append(f"Excellent ROI of {roi:.1f}%")
        elif roi > 20:
            score += 2
            reasons.append(f"Strong ROI of {roi:.1f}%")
        elif roi > 10:
            score += 1
            reasons.append(f"Moderate ROI of {roi:.1f}%")
        else:
            reasons.append(f"Low ROI of {roi:.1f}%")
        
        # NPV criteria
        if npv > 0:
            score += 2
            reasons.append(f"Positive NPV of ${npv:,.0f}")
        else:
            reasons.append(f"Negative NPV of ${npv:,.0f}")
        
        # Payback period criteria
        if payback_period < 3:
            score += 2
            reasons.append(f"Quick payback of {payback_period:.1f} years")
        elif payback_period < 5:
            score += 1
            reasons.append(f"Acceptable payback of {payback_period:.1f} years")
        else:
            reasons.append(f"Long payback of {payback_period:.1f} years")
        
        # IRR criteria
        if irr > self.discount_rate * 100 * 1.5:
            score += 2
            reasons.append(f"High IRR of {irr:.1f}%")
        elif irr > self.discount_rate * 100:
            score += 1
            reasons.append(f"IRR of {irr:.1f}% exceeds WACC")
        else:
            reasons.append(f"IRR of {irr:.1f}% below WACC")
        
        # Final decision
        if score >= 7:
            decision = "YES - STRONGLY RECOMMEND"
            confidence = "High"
        elif score >= 5:
            decision = "YES - RECOMMEND"
            confidence = "Medium"
        elif score >= 3:
            decision = "MAYBE - PROCEED WITH CAUTION"
            confidence = "Low"
        else:
            decision = "NO - DO NOT RECOMMEND"
            confidence = "High"
        
        return {
            'decision': decision,
            'confidence': confidence,
            'score': score,
            'reasoning': "; ".join(reasons)
        }


# Example usage
if __name__ == "__main__":
    # Sample company data
    company_a = {
        'company_name': 'TechCorp Inc',
        'annual_revenue': 50000000,
        'operating_costs': 35000000,
        'total_assets': 80000000,
        'total_liabilities': 30000000,
        'market_value': 120000000,
        'ebitda': 18000000,
        'net_income': 12000000,
        'cash_flow': 15000000
    }
    
    company_b = {
        'company_name': 'DataSystems Ltd',
        'annual_revenue': 35000000,
        'operating_costs': 25000000,
        'total_assets': 60000000,
        'total_liabilities': 20000000,
        'market_value': 85000000,
        'ebitda': 12000000,
        'net_income': 8000000,
        'cash_flow': 10000000
    }
    
    calculator = MergerROICalculator(discount_rate=0.10, tax_rate=0.25)
    result = calculator.analyze_merger(company_a, company_b)
    
    print("=" * 60)
    print("MERGER ROI ANALYSIS")
    print("=" * 60)
    print(f"\nAcquiring Company: {result['company_a']}")
    print(f"Target Company: {result['company_b']}")
    print(f"\nMerger Cost: ${result['merger_cost']:,.2f}")
    print(f"\nAnnual Synergies:")
    print(f"  - Operating: ${result['synergies']['operating']:,.2f}")
    print(f"  - Financial: ${result['synergies']['financial']:,.2f}")
    print(f"  - Revenue: ${result['synergies']['revenue']:,.2f}")
    print(f"  - Total: ${result['synergies']['total_annual']:,.2f}")
    print(f"\nFinancial Metrics:")
    print(f"  - ROI: {result['financial_metrics']['roi_percentage']:.2f}%")
    print(f"  - NPV: ${result['financial_metrics']['npv']:,.2f}")
    print(f"  - IRR: {result['financial_metrics']['irr_percentage']:.2f}%")
    print(f"  - Payback Period: {result['financial_metrics']['payback_period_years']:.2f} years")
    print(f"\n{'=' * 60}")
    print(f"RECOMMENDATION: {result['recommendation']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print("=" * 60)
