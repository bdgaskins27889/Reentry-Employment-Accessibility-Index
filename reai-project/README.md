# Reentry Employment Accessibility Index (REAI)

**Author:** Barbara D. Gaskins  
**Project Type:** Graduate Portfolio - Data Science Capstone  
**Institution:** Bellevue University

---

## Project Overview

The **Reentry Employment Accessibility Index (REAI)** is a county-level composite index designed to measure structural employment accessibility for returning citizens (formerly incarcerated individuals) in North Carolina. Rather than predicting individual employment outcomes, the REAI evaluates systemic conditions that shape opportunity across geographic regions.

This project addresses a critical gap in reentry research by focusing on **structural barriers** rather than individual-level outcomes, providing actionable insights for workforce development, reentry programming, and policy evaluation.

---

## Key Features

- **Composite Index Methodology**: Integrates four key dimensions of employment accessibility
- **CRISP-DM Framework**: Follows industry-standard data mining methodology
- **Public Data Sources**: Uses only publicly available, aggregate-level data
- **Reproducible Analysis**: Complete Python implementation with documented code
- **Comprehensive Visualizations**: Interactive dashboards and publication-ready charts
- **Sensitivity Analysis**: Tests robustness of rankings under alternative weighting schemes

---

## Research Questions

1. Which North Carolina counties exhibit the highest and lowest levels of structural employment accessibility for returning citizens?
2. Which structural factors contribute most significantly to disparities in employment accessibility across counties?
3. Are there observable regional patterns in employment accessibility across urban, suburban, and rural counties?
4. How sensitive are county rankings to changes in index weighting and component selection?
5. How does the REAI correlate with broader economic indicators such as unemployment and poverty rates?

---

## REAI Components

The index is constructed from four weighted components:

| Component | Weight | Description |
|-----------|--------|-------------|
| **Transportation & Mobility Access** | 30% | Vehicle availability, commute times, broadband access |
| **Local Labor Market Demand** | 35% | Unemployment rates, employment growth, poverty rates |
| **Occupational Licensing Burden** | 20% | State-level licensing requirements and barriers |
| **Fair-Chance Policy Environment** | 15% | Ban-the-Box policies, fair-chance hiring protections |

All components are normalized to a 0-100 scale and combined into a final REAI score.

---

## Data Sources

This project utilizes **10 publicly available datasets**:

### 1-4. U.S. Census Bureau - American Community Survey (ACS) 5-Year Estimates
- **Vehicle Availability** (Table B08201)
- **Commute Time** (Table B08303)
- **Poverty Rates** (Table S1701)
- **Broadband Access** (Table B28002)

### 5-6. Bureau of Labor Statistics (BLS)
- **Local Area Unemployment Statistics (LAUS)**
- **Quarterly Census of Employment and Wages (QCEW)**

### 7. Institute for Justice
- **License to Work 3rd Edition** - Occupational licensing burdens

### 8-9. National Conference of State Legislatures (NCSL) & LawAtlas
- **Ban-the-Box Policies**
- **Fair-Chance Hiring Laws**

### 10. North Carolina Department of Adult Correction
- **Post-Release Employment Outcomes**

See [`docs/datasets_documentation.md`](docs/datasets_documentation.md) for detailed information.

---

## Project Structure

```
reai-project/
├── data/                          # Data files
│   ├── nc_counties_master.csv     # Raw county-level data
│   ├── nc_counties_reai_results.csv  # REAI scores and rankings
│   └── reai_sensitivity_analysis.csv # Alternative weighting scenarios
├── src/                           # Source code
│   ├── data_loader.py             # Data loading and preparation
│   ├── reai_calculator.py         # REAI calculation engine
│   └── reai_visualizer.py         # Visualization functions
├── visualizations/                # Output charts and graphs
│   ├── reai_dashboard.png
│   ├── top_bottom_counties.png
│   ├── correlation_matrix.png
│   └── ...
├── notebooks/                     # Jupyter notebooks (optional)
├── docs/                          # Documentation
│   ├── datasets_documentation.md
│   └── methodology.md
├── main.py                        # Main analysis script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/reai-project.git
cd reai-project
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Optional: Set Census API Key**
```bash
export CENSUS_API_KEY="your_api_key_here"
```
Get a free API key at: https://api.census.gov/data/key_signup.html

---

## Usage

### Run Complete Analysis

Execute the main analysis script to:
- Load and prepare all data sources
- Calculate REAI scores for all NC counties
- Perform sensitivity analysis
- Generate visualizations

```bash
python main.py
```

### Use Individual Modules

**Load Data:**
```python
from src.data_loader import REAIDataLoader

loader = REAIDataLoader()
data = loader.create_master_dataset()
```

**Calculate REAI:**
```python
from src.reai_calculator import REAICalculator

calculator = REAICalculator()
results = calculator.calculate_reai(data)
```

**Create Visualizations:**
```python
from src.reai_visualizer import REAIVisualizer

viz = REAIVisualizer(results)
viz.create_summary_dashboard(save_path='dashboard.png')
```

---

## Methodology (CRISP-DM)

This project follows the **Cross-Industry Standard Process for Data Mining (CRISP-DM)** framework:

### 1. Business Understanding
- Identify how structural employment access affects reentry success and community safety
- Connect employment accessibility to violence reduction and recidivism

### 2. Data Understanding
- Evaluate publicly available labor, transportation, licensing, and policy datasets
- Assess data quality, coverage, and limitations

### 3. Data Preparation
- Clean, normalize, and harmonize county-level data
- Handle missing values and align geographic identifiers

### 4. Modeling
- Construct weighted composite index (REAI)
- Normalize all components to 0-100 scale

### 5. Evaluation
- Conduct sensitivity testing of weights
- Validate against economic indicators
- Assess internal consistency

### 6. Deployment
- Present findings through rankings and visualizations
- Develop white paper with policy implications
- Share code and data publicly on GitHub

---

## Key Findings

*(Results will be populated after running the analysis)*

### Overall Statistics
- **Mean REAI Score:** [To be calculated]
- **Standard Deviation:** [To be calculated]
- **Range:** [To be calculated]

### Top 5 Counties
1. [County Name] - Score: [XX.XX]
2. [County Name] - Score: [XX.XX]
3. [County Name] - Score: [XX.XX]
4. [County Name] - Score: [XX.XX]
5. [County Name] - Score: [XX.XX]

### Component Analysis
- **Strongest Factor:** [Component name]
- **Weakest Factor:** [Component name]
- **Correlation with Unemployment:** [r = X.XXX]
- **Correlation with Poverty:** [r = X.XXX]

---

## Ethical Considerations

This project adheres to strict ethical standards:

- ✅ **No Individual-Level Data**: Uses only aggregate, county-level data
- ✅ **No Criminal Justice Records**: Avoids individual criminal history or employment records
- ✅ **Public Data Only**: All sources are publicly available and non-sensitive
- ✅ **Anti-Stigmatization**: Measures structural conditions, not individual behavior
- ✅ **Transparency**: Complete methodology and code are open-source

---

## Connection to Community Violence Reduction

Employment accessibility is increasingly recognized as a key social determinant of public safety. Research demonstrates that:

- **Reduced Recidivism**: Stable employment post-release is associated with lower rates of re-arrest
- **Violence Prevention**: Employment programs for at-risk youth reduce violent-crime arrests by 33-43% ([Heller et al., 2017](https://doi.org/10.1093/qje/qjw033))
- **Community Stability**: Economic opportunity functions as a protective factor against criminal behavior

By identifying counties where employment accessibility is structurally constrained, the REAI highlights areas where investments in workforce access could contribute to violence prevention efforts.

---

## Future Enhancements

- [ ] Expand to additional states beyond North Carolina
- [ ] Integrate real-time data updates via APIs
- [ ] Develop interactive web dashboard
- [ ] Add machine learning models for predictive analysis
- [ ] Incorporate additional policy variables (e.g., expungement laws)
- [ ] Create county-specific policy recommendations

---

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs or issues
- Suggest new features or data sources
- Submit pull requests with improvements
- Share feedback on methodology

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Citation

If you use this work in your research or practice, please cite:

```
Gaskins, B. D. (2026). Reentry Employment Accessibility Index (REAI): 
Measuring Structural Employment Accessibility for Returning Citizens in North Carolina. 
Bellevue University Graduate Portfolio Project.
```

---

## Contact

**Barbara D. Gaskins**  
- Email: bdgaskins27889@gmail.com  
- Phone: 252.495.3173  
- LinkedIn: [linkedin.com/in/barbaradgaskins](https://linkedin.com/in/barbaradgaskins)

---

## Acknowledgments

- **Bellevue University** - Graduate Data Science Program
- **U.S. Census Bureau** - American Community Survey data
- **Bureau of Labor Statistics** - Employment and labor market data
- **Institute for Justice** - Occupational licensing research
- **National Conference of State Legislatures** - Policy data
- **North Carolina Department of Adult Correction** - Reentry research

---

## References

1. Heller, S. B., Pollack, H. A., Ander, R., & Ludwig, J. (2017). Preventing youth violence and dropout: A randomized field experiment. *Quarterly Journal of Economics*, 132(2), 761–802. https://doi.org/10.1093/qje/qjw033

2. Institute for Justice. (2022). *License to Work: A national study of burdens from occupational licensing* (3rd ed.). https://ij.org/report/license-to-work-3/

3. National Conference of State Legislatures. (2023). *Ban-the-Box and fair chance hiring laws*. https://www.ncsl.org/civil-and-criminal-justice/ban-the-box

4. Berger-Gross, A. (2022). *The Impact of Post-Release Employment on Recidivism in North Carolina*. NC Department of Commerce. https://tools.nccareers.org/cfs/reports/Impact_of_post_release_employment_on_recidivism_2022.01.14.pdf

5. U.S. Census Bureau. (2023). *American Community Survey 5-year estimates*. https://www.census.gov/data/developers/data-sets/acs-5year.html

---

**Last Updated:** January 2026
