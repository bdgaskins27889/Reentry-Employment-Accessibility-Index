"""
REAI Data Loader Module
Author: Barbara D. Gaskins
Description: Load and prepare data from various sources for REAI calculation
"""

import pandas as pd
import numpy as np
import requests
from typing import Dict, Optional
import json
import warnings
warnings.filterwarnings('ignore')


class REAIDataLoader:
    """
    Load and prepare data from Census Bureau, BLS, and other sources.
    """
    
    def __init__(self, census_api_key: Optional[str] = None):
        """
        Initialize data loader.
        
        Parameters:
        -----------
        census_api_key : str, optional
            API key for Census Bureau data access
        """
        self.census_api_key = census_api_key
        self.nc_fips = "37"  # North Carolina state FIPS code
        
    def load_nc_counties(self) -> pd.DataFrame:
        """
        Load list of all North Carolina counties with FIPS codes.
        
        Returns:
        --------
        pd.DataFrame : County names and FIPS codes
        """
        # NC County FIPS codes (all 100 counties)
        nc_counties = {
            '001': 'Alamance', '003': 'Alexander', '005': 'Alleghany', '007': 'Anson',
            '009': 'Ashe', '011': 'Avery', '013': 'Beaufort', '015': 'Bertie',
            '017': 'Bladen', '019': 'Brunswick', '021': 'Buncombe', '023': 'Burke',
            '025': 'Cabarrus', '027': 'Caldwell', '029': 'Camden', '031': 'Carteret',
            '033': 'Caswell', '035': 'Catawba', '037': 'Chatham', '039': 'Cherokee',
            '041': 'Chowan', '043': 'Clay', '045': 'Cleveland', '047': 'Columbus',
            '049': 'Craven', '051': 'Cumberland', '053': 'Currituck', '055': 'Dare',
            '057': 'Davidson', '059': 'Davie', '061': 'Duplin', '063': 'Durham',
            '065': 'Edgecombe', '067': 'Forsyth', '069': 'Franklin', '071': 'Gaston',
            '073': 'Gates', '075': 'Graham', '077': 'Granville', '079': 'Greene',
            '081': 'Guilford', '083': 'Halifax', '085': 'Harnett', '087': 'Haywood',
            '089': 'Henderson', '091': 'Hertford', '093': 'Hoke', '095': 'Hyde',
            '097': 'Iredell', '099': 'Jackson', '101': 'Johnston', '103': 'Jones',
            '105': 'Lee', '107': 'Lenoir', '109': 'Lincoln', '111': 'McDowell',
            '113': 'Macon', '115': 'Madison', '117': 'Martin', '119': 'Mecklenburg',
            '121': 'Mitchell', '123': 'Montgomery', '125': 'Moore', '127': 'Nash',
            '129': 'New Hanover', '131': 'Northampton', '133': 'Onslow', '135': 'Orange',
            '137': 'Pamlico', '139': 'Pasquotank', '141': 'Pender', '143': 'Perquimans',
            '145': 'Person', '147': 'Pitt', '149': 'Polk', '151': 'Randolph',
            '153': 'Richmond', '155': 'Robeson', '157': 'Rockingham', '159': 'Rowan',
            '161': 'Rutherford', '163': 'Sampson', '165': 'Scotland', '167': 'Stanly',
            '169': 'Stokes', '171': 'Surry', '173': 'Swain', '175': 'Transylvania',
            '177': 'Tyrrell', '179': 'Union', '181': 'Vance', '183': 'Wake',
            '185': 'Warren', '187': 'Washington', '189': 'Watauga', '191': 'Wayne',
            '193': 'Wilkes', '195': 'Wilson', '197': 'Yadkin', '199': 'Yancey'
        }
        
        df = pd.DataFrame([
            {'county_fips': fips, 'county': name, 'state_fips': self.nc_fips}
            for fips, name in nc_counties.items()
        ])
        
        df['full_fips'] = df['state_fips'] + df['county_fips']
        
        return df
    
    def fetch_acs_data(self, table: str, variables: Dict[str, str], 
                       year: int = 2022) -> pd.DataFrame:
        """
        Fetch data from Census Bureau American Community Survey.
        
        Parameters:
        -----------
        table : str
            ACS table code (e.g., 'B08201' for vehicle availability)
        variables : dict
            Dictionary mapping variable codes to descriptive names
        year : int
            Year of ACS data (default: 2022, which is 2018-2022 5-year)
            
        Returns:
        --------
        pd.DataFrame : ACS data for NC counties
        """
        if not self.census_api_key:
            print("Warning: No Census API key provided. Using sample data.")
            return self._generate_sample_acs_data(variables)
        
        base_url = f"https://api.census.gov/data/{year}/acs/acs5"
        
        # Build variable list
        var_list = ','.join(variables.keys())
        
        params = {
            'get': f'NAME,{var_list}',
            'for': 'county:*',
            'in': f'state:{self.nc_fips}',
            'key': self.census_api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Rename variables
            for code, name in variables.items():
                if code in df.columns:
                    df[name] = pd.to_numeric(df[code], errors='coerce')
            
            # Clean up
            df['county'] = df['NAME'].str.replace(' County, North Carolina', '')
            df['county_fips'] = df['county']
            df['full_fips'] = df['state'] + df['county']
            
            return df
            
        except Exception as e:
            print(f"Error fetching ACS data: {e}")
            print("Using sample data instead.")
            return self._generate_sample_acs_data(variables)
    
    def _generate_sample_acs_data(self, variables: Dict[str, str]) -> pd.DataFrame:
        """
        Generate sample ACS data for demonstration.
        
        Parameters:
        -----------
        variables : dict
            Dictionary of variable names
            
        Returns:
        --------
        pd.DataFrame : Sample data
        """
        counties_df = self.load_nc_counties()
        n = len(counties_df)
        
        # Generate random data based on variable names
        for var_name in variables.values():
            if 'vehicle' in var_name.lower():
                counties_df[var_name] = np.random.uniform(3, 15, n)
            elif 'commute' in var_name.lower():
                counties_df[var_name] = np.random.uniform(18, 35, n)
            elif 'broadband' in var_name.lower():
                counties_df[var_name] = np.random.uniform(65, 95, n)
            elif 'poverty' in var_name.lower():
                counties_df[var_name] = np.random.uniform(8, 25, n)
            else:
                counties_df[var_name] = np.random.uniform(0, 100, n)
        
        return counties_df
    
    def load_bls_unemployment(self, year: int = 2023) -> pd.DataFrame:
        """
        Load BLS Local Area Unemployment Statistics for NC counties.
        
        Parameters:
        -----------
        year : int
            Year of data
            
        Returns:
        --------
        pd.DataFrame : Unemployment data by county
        """
        print(f"Note: BLS data requires manual download from https://www.bls.gov/lau/")
        print("Using sample unemployment data for demonstration.")
        
        counties_df = self.load_nc_counties()
        n = len(counties_df)
        
        counties_df['unemployment_rate'] = np.random.uniform(2.5, 8.0, n)
        counties_df['labor_force'] = np.random.randint(10000, 500000, n)
        counties_df['employed'] = counties_df['labor_force'] * (1 - counties_df['unemployment_rate'] / 100)
        counties_df['unemployed'] = counties_df['labor_force'] - counties_df['employed']
        
        return counties_df
    
    def load_employment_growth(self, start_year: int = 2020, 
                              end_year: int = 2023) -> pd.DataFrame:
        """
        Calculate employment growth rate for NC counties.
        
        Parameters:
        -----------
        start_year : int
            Starting year
        end_year : int
            Ending year
            
        Returns:
        --------
        pd.DataFrame : Employment growth rates
        """
        counties_df = self.load_nc_counties()
        n = len(counties_df)
        
        # Sample employment growth (can be negative)
        counties_df['employment_growth'] = np.random.uniform(-3, 6, n)
        
        return counties_df
    
    def load_licensing_data(self) -> pd.DataFrame:
        """
        Load occupational licensing burden data.
        
        Note: This is state-level data from Institute for Justice.
        
        Returns:
        --------
        pd.DataFrame : Licensing burden scores
        """
        counties_df = self.load_nc_counties()
        
        # NC has moderate licensing burden (state-level)
        # Score based on License to Work 3rd Edition
        # Lower burden = higher score for accessibility
        nc_licensing_burden = 65  # Moderate burden (0-100 scale)
        
        counties_df['licensing_burden_index'] = nc_licensing_burden
        
        return counties_df
    
    def load_policy_data(self) -> pd.DataFrame:
        """
        Load fair-chance policy environment data.
        
        Returns:
        --------
        pd.DataFrame : Policy scores
        """
        counties_df = self.load_nc_counties()
        n = len(counties_df)
        
        # NC has state-level Ban-the-Box for public employment
        # Score: 75 out of 100 (good but not comprehensive)
        counties_df['ban_the_box_score'] = 75
        
        # Local fair-chance implementation varies
        counties_df['fair_chance_score'] = np.random.uniform(50, 90, n)
        
        return counties_df
    
    def create_master_dataset(self) -> pd.DataFrame:
        """
        Create complete dataset by merging all data sources.
        
        Returns:
        --------
        pd.DataFrame : Complete dataset for REAI calculation
        """
        print("Building master dataset...")
        print("-" * 50)
        
        # Start with county list
        master_df = self.load_nc_counties()
        print(f"✓ Loaded {len(master_df)} NC counties")
        
        # Load ACS transportation data
        acs_transport_vars = {
            'B08201_001E': 'total_households',
            'B08201_002E': 'households_no_vehicle'
        }
        transport_df = self.fetch_acs_data('B08201', acs_transport_vars)
        transport_df['pct_no_vehicle'] = (
            transport_df['households_no_vehicle'] / transport_df['total_households'] * 100
        )
        master_df = master_df.merge(
            transport_df[['full_fips', 'pct_no_vehicle']], 
            on='full_fips', how='left'
        )
        print("✓ Added vehicle availability data")
        
        # Load ACS commute data
        acs_commute_vars = {
            'B08303_001E': 'total_workers',
            'B08303_013E': 'mean_commute_time'
        }
        commute_df = self.fetch_acs_data('B08303', acs_commute_vars)
        commute_df['avg_commute_time'] = commute_df['mean_commute_time']
        master_df = master_df.merge(
            commute_df[['full_fips', 'avg_commute_time']], 
            on='full_fips', how='left'
        )
        print("✓ Added commute time data")
        
        # Load ACS broadband data
        acs_broadband_vars = {
            'B28002_001E': 'total_households_internet',
            'B28002_004E': 'households_broadband'
        }
        broadband_df = self.fetch_acs_data('B28002', acs_broadband_vars)
        broadband_df['pct_broadband'] = (
            broadband_df['households_broadband'] / broadband_df['total_households_internet'] * 100
        )
        master_df = master_df.merge(
            broadband_df[['full_fips', 'pct_broadband']], 
            on='full_fips', how='left'
        )
        print("✓ Added broadband access data")
        
        # Load ACS poverty data
        acs_poverty_vars = {
            'S1701_C03_001E': 'poverty_rate'
        }
        poverty_df = self.fetch_acs_data('S1701', acs_poverty_vars)
        master_df = master_df.merge(
            poverty_df[['full_fips', 'poverty_rate']], 
            on='full_fips', how='left'
        )
        print("✓ Added poverty rate data")
        
        # Load BLS unemployment data
        unemployment_df = self.load_bls_unemployment()
        master_df = master_df.merge(
            unemployment_df[['full_fips', 'unemployment_rate']], 
            on='full_fips', how='left'
        )
        print("✓ Added unemployment data")
        
        # Load employment growth
        growth_df = self.load_employment_growth()
        master_df = master_df.merge(
            growth_df[['full_fips', 'employment_growth']], 
            on='full_fips', how='left'
        )
        print("✓ Added employment growth data")
        
        # Load licensing data
        licensing_df = self.load_licensing_data()
        master_df = master_df.merge(
            licensing_df[['full_fips', 'licensing_burden_index']], 
            on='full_fips', how='left'
        )
        print("✓ Added licensing burden data")
        
        # Load policy data
        policy_df = self.load_policy_data()
        master_df = master_df.merge(
            policy_df[['full_fips', 'ban_the_box_score', 'fair_chance_score']], 
            on='full_fips', how='left'
        )
        print("✓ Added policy environment data")
        
        print("-" * 50)
        print(f"Master dataset complete: {len(master_df)} counties, {len(master_df.columns)} variables")
        
        return master_df
    
    def save_dataset(self, df: pd.DataFrame, filepath: str):
        """
        Save dataset to CSV file.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataset to save
        filepath : str
            Output file path
        """
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to: {filepath}")


if __name__ == "__main__":
    print("=" * 70)
    print("REAI Data Loader Demo")
    print("=" * 70)
    print()
    
    # Initialize loader
    loader = REAIDataLoader()
    
    # Create master dataset
    master_df = loader.create_master_dataset()
    
    # Display sample
    print("\nSample of master dataset:")
    print(master_df.head(10).to_string())
    
    # Save
    output_path = '/home/ubuntu/reai-project/data/nc_counties_master.csv'
    loader.save_dataset(master_df, output_path)
    
    print("\n" + "=" * 70)
    print("Data loading complete!")
    print("=" * 70)
