# REAI Project: Dataset Documentation

This document provides detailed information about the datasets used in the Reentry Employment Accessibility Index (REAI) project for North Carolina counties.

## Dataset Overview

The REAI project utilizes **10 publicly available datasets** across four key dimensions: transportation and mobility access, labor market demand, occupational licensing burden, and fair-chance policy environment.

---

## Dataset 1: American Community Survey (ACS) 5-Year Estimates - Vehicle Availability

**Source:** U.S. Census Bureau

**URL:** https://data.census.gov/table/ACSDT5Y2022.B08201

**Description:** County-level data on household vehicle availability, which serves as a proxy for transportation access for employment.

**Key Variables:**
- Total households
- Households with no vehicle available
- Households with 1 vehicle available
- Households with 2+ vehicles available

**Geographic Level:** County (all 100 NC counties)

**Time Period:** 2018-2022 (5-year estimates)

**Format:** CSV/API

**Access Method:** Census Bureau Data API or direct download from data.census.gov

---

## Dataset 2: American Community Survey (ACS) 5-Year Estimates - Commute Time

**Source:** U.S. Census Bureau

**URL:** https://data.census.gov/table/ACSDT5Y2022.B08303

**Description:** County-level data on average commute times to work, indicating transportation burden and accessibility.

**Key Variables:**
- Mean travel time to work (minutes)
- Distribution of workers by travel time categories
- Total workers 16 years and over

**Geographic Level:** County (all 100 NC counties)

**Time Period:** 2018-2022 (5-year estimates)

**Format:** CSV/API

**Access Method:** Census Bureau Data API or direct download from data.census.gov

---

## Dataset 3: American Community Survey (ACS) 5-Year Estimates - Poverty Rates

**Source:** U.S. Census Bureau

**URL:** https://data.census.gov/table/ACSDT5Y2022.S1701

**Description:** County-level poverty rates, which contextualize economic conditions affecting employment accessibility.

**Key Variables:**
- Percentage of population below poverty level
- Percentage of population below 150% of poverty level
- Total population for whom poverty status is determined

**Geographic Level:** County (all 100 NC counties)

**Time Period:** 2018-2022 (5-year estimates)

**Format:** CSV/API

**Access Method:** Census Bureau Data API or direct download from data.census.gov

---

## Dataset 4: American Community Survey (ACS) 5-Year Estimates - Broadband Access

**Source:** U.S. Census Bureau

**URL:** https://data.census.gov/table/ACSDT5Y2022.B28002

**Description:** County-level data on broadband internet access, relevant for job search and remote work opportunities.

**Key Variables:**
- Total households
- Households with broadband internet subscription
- Households with no internet access

**Geographic Level:** County (all 100 NC counties)

**Time Period:** 2018-2022 (5-year estimates)

**Format:** CSV/API

**Access Method:** Census Bureau Data API or direct download from data.census.gov

---

## Dataset 5: Bureau of Labor Statistics - Local Area Unemployment Statistics (LAUS)

**Source:** U.S. Bureau of Labor Statistics

**URL:** https://www.bls.gov/lau/

**Description:** Monthly and annual county-level unemployment rates and labor force statistics for North Carolina.

**Key Variables:**
- Unemployment rate (%)
- Labor force size
- Number of employed persons
- Number of unemployed persons

**Geographic Level:** County (all 100 NC counties)

**Time Period:** Annual averages 2020-2023

**Format:** CSV/Excel

**Access Method:** BLS Data Tools or direct download from https://www.bls.gov/lau/tables.htm

---

## Dataset 6: Bureau of Labor Statistics - Quarterly Census of Employment and Wages (QCEW)

**Source:** U.S. Bureau of Labor Statistics

**URL:** https://www.bls.gov/cew/

**Description:** County-level employment and wage data by industry, providing insight into local labor market composition.

**Key Variables:**
- Total employment by county
- Average weekly wages
- Number of establishments
- Industry composition (NAICS codes)

**Geographic Level:** County (all 100 NC counties)

**Time Period:** Annual averages 2020-2023

**Format:** CSV

**Access Method:** BLS QCEW Data Files or API

---

## Dataset 7: Institute for Justice - License to Work 3rd Edition

**Source:** Institute for Justice

**URL:** https://ij.org/report/license-to-work-3/ltw3-data/

**Description:** State-level occupational licensing requirements for 102 lower-income occupations, including fees, training requirements, and exam burdens.

**Key Variables:**
- Number of days of education/training required
- Fees required for licensure
- Number of exams required
- Occupations requiring licenses

**Geographic Level:** State (North Carolina)

**Time Period:** 2022

**Format:** Excel/CSV

**Access Method:** Direct download from Institute for Justice website

---

## Dataset 8: National Conference of State Legislatures - Ban-the-Box Policies

**Source:** National Conference of State Legislatures (NCSL)

**URL:** https://www.ncsl.org/civil-and-criminal-justice/ban-the-box

**Description:** State and local-level policies that remove criminal history questions from job applications.

**Key Variables:**
- Presence of Ban-the-Box policy (state level)
- Scope of policy (public sector, private sector, or both)
- Year of policy adoption

**Geographic Level:** State and local (North Carolina)

**Time Period:** Current as of 2023

**Format:** PDF/Web content (requires manual coding)

**Access Method:** NCSL website and policy briefs

---

## Dataset 9: LawAtlas - Ban-the-Box Policy Dataset

**Source:** LawAtlas (Public Health Law Research)

**URL:** https://lawatlas.org/datasets/ban-the-box

**Description:** Comprehensive dataset of Ban-the-Box statutes, regulations, and executive orders across all 50 states and DC.

**Key Variables:**
- Policy type (statute, regulation, executive order)
- Applicability (public/private sector)
- Scope of restrictions
- Enforcement mechanisms

**Geographic Level:** State (North Carolina)

**Time Period:** Updated through 2023

**Format:** Excel/CSV

**Access Method:** Direct download from LawAtlas website

---

## Dataset 10: North Carolina Department of Adult Correction - Post-Release Employment Outcomes

**Source:** North Carolina Department of Adult Correction / NC Department of Commerce

**URL:** https://tools.nccareers.org/cfs/reports/Impact_of_post_release_employment_on_recidivism_2022.01.14.pdf

**Description:** Research report with data on employment outcomes for individuals released from North Carolina prisons, including county-level employment rates.

**Key Variables:**
- Employment rate within 1 year of release
- County of release
- Recidivism rates by employment status

**Geographic Level:** County (North Carolina)

**Time Period:** 2021-2022 cohorts

**Format:** PDF report (data extraction required)

**Access Method:** Direct download from NC Commerce website

---

## Data Integration Strategy

All datasets will be harmonized to the county level (100 NC counties) using Federal Information Processing Standards (FIPS) codes. Variables will be normalized using min-max scaling to create comparable sub-scores across different measurement scales.

### Data Preparation Steps:

1. **Download and Import:** Acquire all datasets from source URLs
2. **Geographic Alignment:** Ensure all data use consistent county identifiers (FIPS codes)
3. **Temporal Alignment:** Use most recent available data (2020-2023 where possible)
4. **Missing Data Handling:** Document missing values and apply imputation or exclusion rules
5. **Normalization:** Scale all variables to 0-100 range for index construction
6. **Validation:** Cross-check data against known economic indicators

---

## Ethical Considerations

All datasets used in this project are:
- Publicly available
- Aggregate-level (no individual-level data)
- Non-sensitive (no criminal justice records or personal identifiers)
- Appropriate for academic and policy research purposes

This approach ensures compliance with data privacy standards and minimizes risk of stigmatization of justice-impacted individuals.

---

## References

1. U.S. Census Bureau. (2023). *American Community Survey 5-year estimates*. Retrieved from https://www.census.gov/data/developers/data-sets/acs-5year.html

2. U.S. Bureau of Labor Statistics. (2023). *Local Area Unemployment Statistics*. Retrieved from https://www.bls.gov/lau/

3. Institute for Justice. (2022). *License to Work: A national study of burdens from occupational licensing* (3rd ed.). Retrieved from https://ij.org/report/license-to-work-3/

4. National Conference of State Legislatures. (2023). *Ban-the-Box and fair chance hiring laws*. Retrieved from https://www.ncsl.org/civil-and-criminal-justice/ban-the-box

5. Berger-Gross, A. (2022). *The Impact of Post-Release Employment on Recidivism in North Carolina*. NC Department of Commerce. Retrieved from https://tools.nccareers.org/cfs/reports/Impact_of_post_release_employment_on_recidivism_2022.01.14.pdf
