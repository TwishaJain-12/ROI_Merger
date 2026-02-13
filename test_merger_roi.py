"""
Test Merger ROI Calculator
Quick demonstration of the calculator
"""

from merger_roi_calculator import MergerROICalculator

def print_separator():
    print("=" * 70)

def test_merger_scenario(name, company_a, company_b, synergy_rate=0.10, premium=0.30):
    """Test a merger scenario and print results"""
    print_separator()
    print(f"SCENARIO: {name}")
    print_separator()
    
    calculator = MergerROICalculator(discount_rate=0.10, tax_rate=0.25)
    result = calculator.analyze_merger(company_a, company_b, synergy_rate, premium)
    
    print(f"\n📊 MERGER ANALYSIS")
    print(f"   Acquiring: {result['company_a']}")
    print(f"   Target: {result['company_b']}")
    
    print(f"\n💰 FINANCIAL OVERVIEW")
    print(f"   Merger Cost: ${result['merger_cost']:,.0f}")
    print(f"   Annual Synergies: ${result['synergies']['total_annual']:,.0f}")
    
    print(f"\n📈 KEY METRICS")
    print(f"   ROI: {result['financial_metrics']['roi_percentage']:.2f}%")
    print(f"   NPV: ${result['financial_metrics']['npv']:,.0f}")
    print(f"   IRR: {result['financial_metrics']['irr_percentage']:.2f}%")
    print(f"   Payback: {result['financial_metrics']['payback_period_years']:.1f} years")
    
    print(f"\n🎯 RECOMMENDATION")
    print(f"   Decision: {result['recommendation']}")
    print(f"   Confidence: {result['confidence']}")
    print(f"   Reasoning: {result['reasoning']}")
    
    print_separator()
    print()


# Sample company data
techcorp = {
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

datasystems = {
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

cloudnet = {
    'company_name': 'CloudNet Solutions',
    'annual_revenue': 42000000,
    'operating_costs': 30000000,
    'total_assets': 70000000,
    'total_liabilities': 25000000,
    'market_value': 95000000,
    'ebitda': 15000000,
    'net_income': 10000000,
    'cash_flow': 12000000
}

financehub = {
    'company_name': 'FinanceHub Corp',
    'annual_revenue': 80000000,
    'operating_costs': 60000000,
    'total_assets': 150000000,
    'total_liabilities': 50000000,
    'market_value': 200000000,
    'ebitda': 25000000,
    'net_income': 18000000,
    'cash_flow': 22000000
}


if __name__ == "__main__":
    print("\n")
    print("🚀 MERGER ROI CALCULATOR - TEST SCENARIOS")
    print()
    
    # Scenario 1: Good merger with high synergies
    test_merger_scenario(
        "Good Merger - High Synergies",
        techcorp,
        datasystems,
        synergy_rate=0.15,  # 15% synergies
        premium=0.25        # 25% premium
    )
    
    # Scenario 2: Standard merger
    test_merger_scenario(
        "Standard Merger - Moderate Terms",
        techcorp,
        cloudnet,
        synergy_rate=0.10,  # 10% synergies
        premium=0.30        # 30% premium
    )
    
    # Scenario 3: Risky merger with high premium
    test_merger_scenario(
        "Risky Merger - High Premium",
        datasystems,
        financehub,
        synergy_rate=0.08,  # 8% synergies
        premium=0.45        # 45% premium
    )
    
    # Scenario 4: Excellent merger with low premium
    test_merger_scenario(
        "Excellent Merger - Low Premium",
        techcorp,
        datasystems,
        synergy_rate=0.12,  # 12% synergies
        premium=0.20        # 20% premium
    )
    
    print("\n✅ All scenarios tested!")
    print("\nKey Takeaways:")
    print("  • Higher synergies = Better ROI")
    print("  • Lower premium = Better ROI")
    print("  • NPV must be positive for value creation")
    print("  • IRR should exceed cost of capital (10%)")
    print("  • Payback period should be < 5 years")
    print()
