"""
Merger ROI Calculator
Based on academic research: Damodaran, Bruner, Koller
"""

from typing import Dict


class MergerROICalculator:
    """Calculate Merger ROI using academic methodologies"""
    
    def __init__(self, discount_rate: float = 0.10, tax_rate: float = 0.25):
        self.discount_rate = discount_rate
        self.tax_rate = tax_rate
    
    def calculate_synergies(self, company_a: Dict, company_b: Dict, 
                           synergy_rate: float = 0.10) -> Dict:
        """Calculate operational and financial synergies"""
        combined_costs = company_a['operating_costs'] + company_b['operating_costs']
        operating_synergies = combined_costs * synergy_rate
        
        combined_ebitda = company_a['ebitda'] + company_b['ebitda']
        tax_shield = combined_ebitda * self.tax_rate * 0.05
        
        combined_revenue = company_a['annual_revenue'] + company_b['annual_revenue']
        revenue_synergies = combined_revenue * 0.03
        
        total_synergies = operating_synergies + tax_shield + revenue_synergies
        
        return {
            'operating': round(operating_synergies, 2),
            'financial': round(tax_shield, 2),
            'revenue': round(revenue_synergies, 2),
            'total_annual': round(total_synergies, 2)
        }
    
    def calculate_merger_cost(self, company_b: Dict, premium: float = 0.30) -> float:
        """Calculate total merger cost including premium"""
        base_cost = company_b['market_value']
        premium_cost = base_cost * premium
        transaction_costs = base_cost * 0.02
        return base_cost + premium_cost + transaction_costs
    
    def calculate_npv(self, annual_synergies: float, merger_cost: float, 
                     years: int = 5) -> float:
        """Calculate Net Present Value"""
        pv_synergies = 0
        for year in range(1, years + 1):
            synergy_value = annual_synergies * (1.02 ** year)
            discount_factor = (1 + self.discount_rate) ** year
            pv_synergies += synergy_value / discount_factor
        return pv_synergies - merger_cost
    
    def calculate_roi(self, annual_synergies: float, merger_cost: float) -> float:
        """Calculate ROI percentage"""
        total_benefits = sum(annual_synergies * (1.02 ** year) for year in range(1, 6))
        return ((total_benefits - merger_cost) / merger_cost) * 100
    
    def calculate_payback_period(self, annual_synergies: float, 
                                 merger_cost: float) -> float:
        """Calculate payback period in years"""
        if annual_synergies <= 0:
            return float('inf')
        
        cumulative = 0
        year = 0
        while cumulative < merger_cost and year < 20:
            year += 1
            cumulative += annual_synergies * (1.02 ** year)
        return year if cumulative >= merger_cost else float('inf')
    
    def calculate_irr(self, annual_synergies: float, merger_cost: float, 
                     years: int = 5) -> float:
        """Calculate Internal Rate of Return"""
        irr_guess = 0.15
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
            if irr_guess < -0.99:
                irr_guess = -0.99
        
        return irr_guess * 100
    
    def analyze_merger(self, company_a: Dict, company_b: Dict, 
                      synergy_rate: float = 0.10, 
                      premium: float = 0.30) -> Dict:
        """Complete merger analysis with recommendation"""
        synergies = self.calculate_synergies(company_a, company_b, synergy_rate)
        annual_synergies = synergies['total_annual']
        
        merger_cost = self.calculate_merger_cost(company_b, premium)
        
        npv = self.calculate_npv(annual_synergies, merger_cost)
        roi = self.calculate_roi(annual_synergies, merger_cost)
        payback_period = self.calculate_payback_period(annual_synergies, merger_cost)
        irr = self.calculate_irr(annual_synergies, merger_cost)
        
        combined_revenue = company_a['annual_revenue'] + company_b['annual_revenue']
        combined_ebitda = company_a['ebitda'] + company_b['ebitda'] + annual_synergies
        combined_assets = company_a['total_assets'] + company_b['total_assets']
        
        recommendation = self._make_recommendation(roi, npv, payback_period, irr)
        
        return {
            'company_a': company_a['company_name'],
            'company_b': company_b['company_name'],
            'merger_cost': round(merger_cost, 2),
            'synergies': synergies,
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
        """Make merger recommendation based on multiple criteria"""
        score = 0
        reasons = []
        
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
        
        if npv > 0:
            score += 2
            reasons.append(f"Positive NPV of ${npv:,.0f}")
        else:
            reasons.append(f"Negative NPV of ${npv:,.0f}")
        
        if payback_period < 3:
            score += 2
            reasons.append(f"Quick payback of {payback_period:.1f} years")
        elif payback_period < 5:
            score += 1
            reasons.append(f"Acceptable payback of {payback_period:.1f} years")
        else:
            reasons.append(f"Long payback of {payback_period:.1f} years")
        
        if irr > self.discount_rate * 100 * 1.5:
            score += 2
            reasons.append(f"High IRR of {irr:.1f}%")
        elif irr > self.discount_rate * 100:
            score += 1
            reasons.append(f"IRR of {irr:.1f}% exceeds WACC")
        else:
            reasons.append(f"IRR of {irr:.1f}% below WACC")
        
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
