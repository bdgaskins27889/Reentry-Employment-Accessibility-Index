"""
REAI Visualization Module
Author: Barbara D. Gaskins
Description: Create visualizations for REAI analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class REAIVisualizer:
    """
    Create visualizations for REAI analysis results.
    """
    
    def __init__(self, results_df: pd.DataFrame):
        """
        Initialize visualizer with REAI results.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame containing REAI scores and component scores
        """
        self.df = results_df
        
    def plot_top_bottom_counties(self, n: int = 10, save_path: Optional[str] = None):
        """
        Create horizontal bar chart showing top and bottom n counties by REAI.
        
        Parameters:
        -----------
        n : int
            Number of top and bottom counties to display
        save_path : str, optional
            Path to save the figure
        """
        # Get top and bottom counties
        top_n = self.df.nsmallest(n, 'REAI_rank')
        bottom_n = self.df.nlargest(n, 'REAI_rank')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
        
        # Top counties
        ax1.barh(top_n['county'], top_n['REAI'], color='#2ecc71')
        ax1.set_xlabel('REAI Score', fontsize=12, fontweight='bold')
        ax1.set_title(f'Top {n} Counties by REAI', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        
        # Bottom counties
        ax2.barh(bottom_n['county'], bottom_n['REAI'], color='#e74c3c')
        ax2.set_xlabel('REAI Score', fontsize=12, fontweight='bold')
        ax2.set_title(f'Bottom {n} Counties by REAI', fontsize=14, fontweight='bold')
        ax2.invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def plot_component_scores(self, counties: Optional[List[str]] = None, 
                             save_path: Optional[str] = None):
        """
        Create radar/spider chart comparing component scores across counties.
        
        Parameters:
        -----------
        counties : list, optional
            List of county names to compare. If None, uses top 5 counties.
        save_path : str, optional
            Path to save the figure
        """
        if counties is None:
            counties = self.df.nsmallest(5, 'REAI_rank')['county'].tolist()
        
        # Filter data
        plot_df = self.df[self.df['county'].isin(counties)]
        
        # Component columns
        components = ['transportation_score', 'labor_market_score', 
                     'licensing_score', 'policy_score']
        component_labels = ['Transportation', 'Labor Market', 'Licensing', 'Policy']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        x = np.arange(len(component_labels))
        width = 0.15
        
        for i, county in enumerate(counties):
            county_data = plot_df[plot_df['county'] == county][components].values[0]
            ax.bar(x + i * width, county_data, width, label=county)
        
        ax.set_xlabel('Component', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score (0-100)', fontsize=12, fontweight='bold')
        ax.set_title('REAI Component Scores by County', fontsize=14, fontweight='bold')
        ax.set_xticks(x + width * (len(counties) - 1) / 2)
        ax.set_xticklabels(component_labels)
        ax.legend()
        ax.set_ylim(0, 100)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def plot_reai_distribution(self, save_path: Optional[str] = None):
        """
        Create histogram showing distribution of REAI scores.
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(self.df['REAI'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        ax.axvline(self.df['REAI'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {self.df["REAI"].mean():.2f}')
        ax.axvline(self.df['REAI'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f'Median: {self.df["REAI"].median():.2f}')
        
        ax.set_xlabel('REAI Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of REAI Scores Across Counties', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def plot_correlation_matrix(self, save_path: Optional[str] = None):
        """
        Create correlation heatmap for REAI components.
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
        """
        components = ['transportation_score', 'labor_market_score', 
                     'licensing_score', 'policy_score', 'REAI']
        
        corr_matrix = self.df[components].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax)
        
        ax.set_title('Correlation Matrix: REAI Components', 
                    fontsize=14, fontweight='bold')
        
        # Update labels
        labels = ['Transportation', 'Labor Market', 'Licensing', 'Policy', 'REAI']
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_yticklabels(labels, rotation=0)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def plot_scatter_comparison(self, x_var: str, y_var: str = 'REAI',
                               save_path: Optional[str] = None):
        """
        Create scatter plot comparing REAI with another variable.
        
        Parameters:
        -----------
        x_var : str
            Variable for x-axis (e.g., 'unemployment_rate', 'poverty_rate')
        y_var : str
            Variable for y-axis (default: 'REAI')
        save_path : str, optional
            Path to save the figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(self.df[x_var], self.df[y_var], alpha=0.6, s=100, color='#9b59b6')
        
        # Add trend line
        z = np.polyfit(self.df[x_var], self.df[y_var], 1)
        p = np.poly1d(z)
        ax.plot(self.df[x_var], p(self.df[x_var]), "r--", alpha=0.8, linewidth=2)
        
        # Calculate correlation
        corr = self.df[x_var].corr(self.df[y_var])
        
        ax.set_xlabel(x_var.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel(y_var.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(f'{y_var.upper()} vs {x_var.replace("_", " ").title()}\n(Correlation: {corr:.3f})', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def create_summary_dashboard(self, save_path: Optional[str] = None):
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Top 10 counties
        ax1 = fig.add_subplot(gs[0, 0])
        top_10 = self.df.nsmallest(10, 'REAI_rank')
        ax1.barh(top_10['county'], top_10['REAI'], color='#2ecc71')
        ax1.set_xlabel('REAI Score', fontweight='bold')
        ax1.set_title('Top 10 Counties', fontweight='bold')
        ax1.invert_yaxis()
        
        # 2. Distribution
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.hist(self.df['REAI'], bins=15, color='#3498db', edgecolor='black', alpha=0.7)
        ax2.axvline(self.df['REAI'].mean(), color='red', linestyle='--', linewidth=2)
        ax2.set_xlabel('REAI Score', fontweight='bold')
        ax2.set_ylabel('Frequency', fontweight='bold')
        ax2.set_title('REAI Distribution', fontweight='bold')
        
        # 3. Component comparison
        ax3 = fig.add_subplot(gs[1, :])
        top_5 = self.df.nsmallest(5, 'REAI_rank')['county'].tolist()
        components = ['transportation_score', 'labor_market_score', 
                     'licensing_score', 'policy_score']
        component_labels = ['Transportation', 'Labor Market', 'Licensing', 'Policy']
        
        x = np.arange(len(component_labels))
        width = 0.15
        
        for i, county in enumerate(top_5):
            county_data = self.df[self.df['county'] == county][components].values[0]
            ax3.bar(x + i * width, county_data, width, label=county)
        
        ax3.set_xlabel('Component', fontweight='bold')
        ax3.set_ylabel('Score', fontweight='bold')
        ax3.set_title('Component Scores: Top 5 Counties', fontweight='bold')
        ax3.set_xticks(x + width * 2)
        ax3.set_xticklabels(component_labels)
        ax3.legend(loc='upper right')
        ax3.set_ylim(0, 100)
        
        # 4. Correlation heatmap
        ax4 = fig.add_subplot(gs[2, 0])
        components_with_reai = components + ['REAI']
        corr_matrix = self.df[components_with_reai].corr()
        im = ax4.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        ax4.set_xticks(np.arange(len(components_with_reai)))
        ax4.set_yticks(np.arange(len(components_with_reai)))
        labels = ['Trans', 'Labor', 'License', 'Policy', 'REAI']
        ax4.set_xticklabels(labels, rotation=45, ha='right')
        ax4.set_yticklabels(labels)
        ax4.set_title('Component Correlations', fontweight='bold')
        plt.colorbar(im, ax=ax4)
        
        # 5. Scatter: Unemployment vs REAI
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.scatter(self.df['unemployment_rate'], self.df['REAI'], 
                   alpha=0.6, s=80, color='#9b59b6')
        z = np.polyfit(self.df['unemployment_rate'], self.df['REAI'], 1)
        p = np.poly1d(z)
        ax5.plot(self.df['unemployment_rate'], p(self.df['unemployment_rate']), 
                "r--", alpha=0.8, linewidth=2)
        ax5.set_xlabel('Unemployment Rate (%)', fontweight='bold')
        ax5.set_ylabel('REAI Score', fontweight='bold')
        ax5.set_title('REAI vs Unemployment', fontweight='bold')
        
        fig.suptitle('Reentry Employment Accessibility Index (REAI) Dashboard', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Demonstration with sample data
    from reai_calculator import REAICalculator, load_sample_data
    
    print("=" * 70)
    print("REAI Visualization Demo")
    print("=" * 70)
    print()
    
    # Load and calculate
    df = load_sample_data()
    calculator = REAICalculator()
    results = calculator.calculate_reai(df)
    
    # Create visualizer
    viz = REAIVisualizer(results)
    
    # Generate visualizations
    print("Generating visualizations...\n")
    
    print("1. Creating summary dashboard...")
    viz.create_summary_dashboard(save_path='/home/ubuntu/reai-project/visualizations/dashboard.png')
    
    print("\n2. Creating top/bottom counties chart...")
    viz.plot_top_bottom_counties(n=10, save_path='/home/ubuntu/reai-project/visualizations/top_bottom.png')
    
    print("\n3. Creating distribution plot...")
    viz.plot_reai_distribution(save_path='/home/ubuntu/reai-project/visualizations/distribution.png')
    
    print("\n4. Creating correlation matrix...")
    viz.plot_correlation_matrix(save_path='/home/ubuntu/reai-project/visualizations/correlation.png')
    
    print("\n" + "=" * 70)
    print("Visualization complete!")
    print("=" * 70)
