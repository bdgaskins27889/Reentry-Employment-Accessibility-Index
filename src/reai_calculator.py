"""
Reentry Employment Accessibility Index (REAI) Calculator
Author: Barbara D. Gaskins
Description: Calculate county-level employment accessibility scores for returning citizens
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


class REAICalculator:
    """
    Calculate the Reentry Employment Accessibility Index (REAI) for North Carolina counties.
    
    The REAI is a composite index measuring structural employment accessibility for
    returning citizens based on four key dimensions:
    1. Transportation and Mobility Access
    2. Local Labor Market Demand
    3. Occupational Licensing Burden
    4. Fair-Chance Policy Environment
    """
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize the REAI Calculator.
        
        Parameters:
        -----------
        weights : dict, optional
            Custom weights for index components. Default weights are:
            - transportation: 0.30
            - labor_market: 0.35
            - licensing: 0.20
            - policy: 0.15
        """
        self.default_weights = {
            'transportation': 0.30,
            'labor_market': 0.35,
            'licensing': 0.20,
            'policy': 0.15
        }
        self.weights = weights if weights else self.default_weights
        self._validate_weights()
        
    def _validate_weights(self):
        """Ensure weights sum to 1.0"""
        total = sum(self.weights.values())
        if not np.isclose(total, 1.0):
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def normalize_score(self, series: pd.Series, reverse: bool = False) -> pd.Series:
        """
        Normalize a series to 0-100 scale using min-max normalization.
        
        Parameters:
        -----------
        series : pd.Series
            Input data to normalize
        reverse : bool
            If True, reverse the scale (higher raw values = lower scores)
            
        Returns:
        --------
        pd.Series : Normalized scores (0-100)
        """
        min_val = series.min()
        max_val = series.max()
        
        if max_val == min_val:
            return pd.Series([50.0] * len(series), index=series.index)
        
        normalized = (series - min_val) / (max_val - min_val) * 100
        
        if reverse:
            normalized = 100 - normalized
            
        return normalized
    
    def calculate_transportation_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Transportation and Mobility Access score.
        
        Components:
        - Vehicle availability (higher = better)
        - Average commute time (lower = better)
        - Broadband access (higher = better)
        
        Parameters:
        -----------
        df : pd.DataFrame
            Must contain: pct_no_vehicle, avg_commute_time, pct_broadband
            
        Returns:
        --------
        pd.Series : Transportation scores (0-100)
        """
        # Normalize each component
        vehicle_score = self.normalize_score(100 - df['pct_no_vehicle'], reverse=False)
        commute_score = self.normalize_score(df['avg_commute_time'], reverse=True)
        broadband_score = self.normalize_score(df['pct_broadband'], reverse=False)
        
        # Equal weighting of sub-components
        transport_score = (vehicle_score + commute_score + broadband_score) / 3
        
        return transport_score
    
    def calculate_labor_market_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Local Labor Market Demand score.
        
        Components:
        - Unemployment rate (lower = better)
        - Employment growth (higher = better)
        - Poverty rate (lower = better)
        
        Parameters:
        -----------
        df : pd.DataFrame
            Must contain: unemployment_rate, employment_growth, poverty_rate
            
        Returns:
        --------
        pd.Series : Labor market scores (0-100)
        """
        unemployment_score = self.normalize_score(df['unemployment_rate'], reverse=True)
        employment_growth_score = self.normalize_score(df['employment_growth'], reverse=False)
        poverty_score = self.normalize_score(df['poverty_rate'], reverse=True)
        
        # Weighted sub-components (unemployment weighted more heavily)
        labor_score = (
            unemployment_score * 0.40 +
            employment_growth_score * 0.30 +
            poverty_score * 0.30
        )
        
        return labor_score
    
    def calculate_licensing_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Occupational Licensing Burden score.
        
        This is a state-level measure applied uniformly, but can be adjusted
        by county-level factors if data becomes available.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Must contain: licensing_burden_index
            
        Returns:
        --------
        pd.Series : Licensing scores (0-100)
        """
        # State-level licensing burden (lower burden = higher score)
        licensing_score = self.normalize_score(df['licensing_burden_index'], reverse=True)
        
        return licensing_score
    
    def calculate_policy_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Fair-Chance Policy Environment score.
        
        Components:
        - Ban-the-Box policy presence (binary or scaled)
        - Fair-chance hiring protections
        - Expungement accessibility
        
        Parameters:
        -----------
        df : pd.DataFrame
            Must contain: ban_the_box_score, fair_chance_score
            
        Returns:
        --------
        pd.Series : Policy scores (0-100)
        """
        # Normalize policy indicators
        btb_score = self.normalize_score(df['ban_the_box_score'], reverse=False)
        fair_chance_score = self.normalize_score(df['fair_chance_score'], reverse=False)
        
        # Equal weighting
        policy_score = (btb_score + fair_chance_score) / 2
        
        return policy_score
    
    def calculate_reai(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the complete REAI for all counties.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Must contain all required variables for component scores
            
        Returns:
        --------
        pd.DataFrame : Original data with added component scores and REAI
        """
        # Calculate component scores
        df['transportation_score'] = self.calculate_transportation_score(df)
        df['labor_market_score'] = self.calculate_labor_market_score(df)
        df['licensing_score'] = self.calculate_licensing_score(df)
        df['policy_score'] = self.calculate_policy_score(df)
        
        # Calculate weighted REAI
        df['REAI'] = (
            df['transportation_score'] * self.weights['transportation'] +
            df['labor_market_score'] * self.weights['labor_market'] +
            df['licensing_score'] * self.weights['licensing'] +
            df['policy_score'] * self.weights['policy']
        )
        
        # Add ranking
        df['REAI_rank'] = df['REAI'].rank(ascending=False, method='min').astype(int)
        
        return df
    
    def sensitivity_analysis(self, df: pd.DataFrame, 
                           weight_scenarios: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """
        Perform sensitivity analysis with different weighting schemes.
        
        Parameters:
        -----------
        df : pd.DataFrame
            County data with component scores
        weight_scenarios : dict
            Dictionary of scenario names and their weight dictionaries
            
        Returns:
        --------
        pd.DataFrame : Rankings under different scenarios
        """
        results = pd.DataFrame(index=df.index)
        results['county'] = df['county']
        results['base_REAI'] = df['REAI']
        results['base_rank'] = df['REAI_rank']
        
        for scenario_name, weights in weight_scenarios.items():
            # Validate weights
            if not np.isclose(sum(weights.values()), 1.0):
                raise ValueError(f"Weights for {scenario_name} must sum to 1.0")
            
            # Calculate REAI with alternative weights
            scenario_reai = (
                df['transportation_score'] * weights['transportation'] +
                df['labor_market_score'] * weights['labor_market'] +
                df['licensing_score'] * weights['licensing'] +
                df['policy_score'] * weights['policy']
            )
            
            results[f'{scenario_name}_REAI'] = scenario_reai
            results[f'{scenario_name}_rank'] = scenario_reai.rank(ascending=False, method='min').astype(int)
        
        return results
    
    def get_summary_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate summary statistics for the REAI and its components.
        
        Parameters:
        -----------
        df : pd.DataFrame
            County data with REAI scores
            
        Returns:
        --------
        pd.DataFrame : Summary statistics
        """
        score_columns = ['REAI', 'transportation_score', 'labor_market_score', 
                        'licensing_score', 'policy_score']
        
        summary = df[score_columns].describe().T
        summary['weight'] = [1.0] + [self.weights[k] for k in self.weights.keys()]
        
        return summary[['weight', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]


def load_sample_data() -> pd.DataFrame:
    """
    Generate sample data for demonstration purposes.
    
    In production, this would load real data from Census, BLS, etc.
    
    Returns:
    --------
    pd.DataFrame : Sample county-level data
    """
    np.random.seed(42)
    
    # List of NC counties (sample)
    counties = [
        'Wake', 'Mecklenburg', 'Guilford', 'Forsyth', 'Durham', 
        'Buncombe', 'Cumberland', 'New Hanover', 'Gaston', 'Union',
        'Onslow', 'Cabarrus', 'Iredell', 'Pitt', 'Rowan',
        'Alamance', 'Davidson', 'Catawba', 'Johnston', 'Orange'
    ]
    
    n = len(counties)
    
    data = {
        'county': counties,
        'fips': [f'37{str(i).zfill(3)}' for i in range(1, n+1)],
        
        # Transportation variables
        'pct_no_vehicle': np.random.uniform(3, 15, n),
        'avg_commute_time': np.random.uniform(18, 32, n),
        'pct_broadband': np.random.uniform(70, 95, n),
        
        # Labor market variables
        'unemployment_rate': np.random.uniform(3.0, 7.5, n),
        'employment_growth': np.random.uniform(-2, 5, n),
        'poverty_rate': np.random.uniform(8, 22, n),
        
        # Licensing (state-level, uniform for NC)
        'licensing_burden_index': [65] * n,  # NC has moderate licensing burden
        
        # Policy variables
        'ban_the_box_score': [75] * n,  # NC has state-level Ban-the-Box
        'fair_chance_score': np.random.uniform(50, 85, n)  # Varies by local implementation
    }
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Demonstration
    print("=" * 70)
    print("Reentry Employment Accessibility Index (REAI) Calculator")
    print("=" * 70)
    print()
    
    # Load sample data
    print("Loading sample data...")
    df = load_sample_data()
    print(f"Loaded data for {len(df)} counties\n")
    
    # Initialize calculator
    calculator = REAICalculator()
    print("Using default weights:")
    for component, weight in calculator.weights.items():
        print(f"  {component}: {weight:.2%}")
    print()
    
    # Calculate REAI
    print("Calculating REAI scores...")
    results = calculator.calculate_reai(df)
    
    # Display top 10 counties
    print("\nTop 10 Counties by REAI Score:")
    print("-" * 70)
    top_10 = results.nsmallest(10, 'REAI_rank')[
        ['county', 'REAI', 'REAI_rank', 'transportation_score', 
         'labor_market_score', 'licensing_score', 'policy_score']
    ]
    print(top_10.to_string(index=False))
    
    # Summary statistics
    print("\n\nSummary Statistics:")
    print("-" * 70)
    summary = calculator.get_summary_statistics(results)
    print(summary.to_string())
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)
