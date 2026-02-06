"""
Reentry Employment Accessibility Index (REAI) - Main Analysis Script
Author: Barbara D. Gaskins
Description: Complete workflow for REAI calculation and analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import REAIDataLoader
from reai_calculator import REAICalculator
from reai_visualizer import REAIVisualizer
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def main():
    """
    Main execution function for REAI analysis.
    """
    print("=" * 80)
    print(" " * 15 + "REENTRY EMPLOYMENT ACCESSIBILITY INDEX (REAI)")
    print(" " * 20 + "North Carolina County-Level Analysis")
    print(" " * 25 + "By Barbara D. Gaskins")
    print("=" * 80)
    print()
    
    # ========================================================================
    # PHASE 1: DATA LOADING
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 1: DATA LOADING AND PREPARATION")
    print("=" * 80)
    
    loader = REAIDataLoader()
    master_df = loader.create_master_dataset()
    
    # Save raw data
    raw_data_path = 'data/nc_counties_master.csv'
    loader.save_dataset(master_df, raw_data_path)
    
    print(f"\n✓ Master dataset created with {len(master_df)} counties")
    print(f"✓ Data saved to: {raw_data_path}")
    
    # ========================================================================
    # PHASE 2: REAI CALCULATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 2: REAI CALCULATION")
    print("=" * 80)
    
    calculator = REAICalculator()
    
    print("\nUsing component weights:")
    for component, weight in calculator.weights.items():
        print(f"  • {component.replace('_', ' ').title()}: {weight:.1%}")
    
    print("\nCalculating REAI scores...")
    results_df = calculator.calculate_reai(master_df)
    
    # Save results
    results_path = 'data/nc_counties_reai_results.csv'
    results_df.to_csv(results_path, index=False)
    print(f"✓ REAI scores calculated for all counties")
    print(f"✓ Results saved to: {results_path}")
    
    # ========================================================================
    # PHASE 3: RESULTS SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 3: RESULTS SUMMARY")
    print("=" * 80)
    
    print("\n📊 Summary Statistics:")
    print("-" * 80)
    summary = calculator.get_summary_statistics(results_df)
    print(summary.to_string())
    
    print("\n\n🏆 TOP 10 COUNTIES BY REAI SCORE:")
    print("-" * 80)
    top_10 = results_df.nsmallest(10, 'REAI_rank')[[
        'county', 'REAI', 'REAI_rank', 'transportation_score', 
        'labor_market_score', 'licensing_score', 'policy_score'
    ]]
    print(top_10.to_string(index=False))
    
    print("\n\n⚠️  BOTTOM 10 COUNTIES BY REAI SCORE:")
    print("-" * 80)
    bottom_10 = results_df.nlargest(10, 'REAI_rank')[[
        'county', 'REAI', 'REAI_rank', 'transportation_score', 
        'labor_market_score', 'licensing_score', 'policy_score'
    ]]
    print(bottom_10.to_string(index=False))
    
    # ========================================================================
    # PHASE 4: SENSITIVITY ANALYSIS
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 4: SENSITIVITY ANALYSIS")
    print("=" * 80)
    
    print("\nTesting alternative weighting schemes...")
    
    weight_scenarios = {
        'labor_focused': {
            'transportation': 0.20,
            'labor_market': 0.50,
            'licensing': 0.15,
            'policy': 0.15
        },
        'transport_focused': {
            'transportation': 0.50,
            'labor_market': 0.25,
            'licensing': 0.15,
            'policy': 0.10
        },
        'policy_focused': {
            'transportation': 0.25,
            'labor_market': 0.25,
            'licensing': 0.20,
            'policy': 0.30
        }
    }
    
    sensitivity_results = calculator.sensitivity_analysis(results_df, weight_scenarios)
    
    # Save sensitivity results
    sensitivity_path = 'data/reai_sensitivity_analysis.csv'
    sensitivity_results.to_csv(sensitivity_path, index=False)
    
    print(f"✓ Sensitivity analysis complete")
    print(f"✓ Results saved to: {sensitivity_path}")
    
    # Show top 5 under each scenario
    print("\n📊 Top 5 Counties Under Different Scenarios:")
    print("-" * 80)
    
    for scenario in ['base'] + list(weight_scenarios.keys()):
        rank_col = f'{scenario}_rank' if scenario != 'base' else 'base_rank'
        top_5 = sensitivity_results.nsmallest(5, rank_col)[['county', rank_col]]
        print(f"\n{scenario.replace('_', ' ').title()}:")
        for idx, row in top_5.iterrows():
            print(f"  {int(row[rank_col])}. {row['county']}")
    
    # ========================================================================
    # PHASE 5: VISUALIZATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 5: VISUALIZATION")
    print("=" * 80)
    
    print("\nGenerating visualizations...")
    
    viz = REAIVisualizer(results_df)
    
    # Create output directory
    os.makedirs('visualizations', exist_ok=True)
    
    # Generate all visualizations
    print("  • Creating summary dashboard...")
    viz.create_summary_dashboard(save_path='visualizations/reai_dashboard.png')
    
    print("  • Creating top/bottom counties chart...")
    viz.plot_top_bottom_counties(n=10, save_path='visualizations/top_bottom_counties.png')
    
    print("  • Creating distribution plot...")
    viz.plot_reai_distribution(save_path='visualizations/reai_distribution.png')
    
    print("  • Creating correlation matrix...")
    viz.plot_correlation_matrix(save_path='visualizations/correlation_matrix.png')
    
    print("  • Creating component comparison...")
    viz.plot_component_scores(save_path='visualizations/component_scores.png')
    
    print("  • Creating scatter plots...")
    viz.plot_scatter_comparison('unemployment_rate', 'REAI', 
                                save_path='visualizations/reai_vs_unemployment.png')
    viz.plot_scatter_comparison('poverty_rate', 'REAI', 
                                save_path='visualizations/reai_vs_poverty.png')
    
    print("\n✓ All visualizations saved to 'visualizations/' directory")
    
    # ========================================================================
    # PHASE 6: KEY FINDINGS
    # ========================================================================
    print("\n" + "=" * 80)
    print("PHASE 6: KEY FINDINGS")
    print("=" * 80)
    
    # Calculate key statistics
    mean_reai = results_df['REAI'].mean()
    std_reai = results_df['REAI'].std()
    
    highest_county = results_df.loc[results_df['REAI'].idxmax()]
    lowest_county = results_df.loc[results_df['REAI'].idxmin()]
    
    # Component contributions
    component_means = results_df[[
        'transportation_score', 'labor_market_score', 
        'licensing_score', 'policy_score'
    ]].mean()
    
    print(f"\n📈 Overall REAI Statistics:")
    print(f"  • Mean REAI Score: {mean_reai:.2f}")
    print(f"  • Standard Deviation: {std_reai:.2f}")
    print(f"  • Range: {results_df['REAI'].min():.2f} - {results_df['REAI'].max():.2f}")
    
    print(f"\n🏆 Highest Accessibility:")
    print(f"  • County: {highest_county['county']}")
    print(f"  • REAI Score: {highest_county['REAI']:.2f}")
    
    print(f"\n⚠️  Lowest Accessibility:")
    print(f"  • County: {lowest_county['county']}")
    print(f"  • REAI Score: {lowest_county['REAI']:.2f}")
    
    print(f"\n📊 Average Component Scores:")
    for component, score in component_means.items():
        component_name = component.replace('_score', '').replace('_', ' ').title()
        print(f"  • {component_name}: {score:.2f}")
    
    # Correlations with economic indicators
    corr_unemployment = results_df['REAI'].corr(results_df['unemployment_rate'])
    corr_poverty = results_df['REAI'].corr(results_df['poverty_rate'])
    
    print(f"\n🔗 Correlations with Economic Indicators:")
    print(f"  • REAI vs Unemployment Rate: {corr_unemployment:.3f}")
    print(f"  • REAI vs Poverty Rate: {corr_poverty:.3f}")
    
    # ========================================================================
    # COMPLETION
    # ========================================================================
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    
    print("\n📁 Output Files:")
    print(f"  • Raw Data: {raw_data_path}")
    print(f"  • REAI Results: {results_path}")
    print(f"  • Sensitivity Analysis: {sensitivity_path}")
    print(f"  • Visualizations: visualizations/ directory")
    
    print("\n💡 Next Steps:")
    print("  1. Review visualizations in the 'visualizations/' directory")
    print("  2. Examine detailed results in CSV files")
    print("  3. Conduct further analysis on specific counties or regions")
    print("  4. Integrate findings into policy recommendations")
    
    print("\n" + "=" * 80)
    print("Thank you for using the REAI Calculator!")
    print("For questions or feedback, contact: Barbara D. Gaskins")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
