### Scenario 3: Statistical Extraction - Measurement Tools & Effect Sizes

**Research Goal**: Extract quantitative data for meta-analysis

**Optimal Prompt**:
```
Extract from all RCT studies:
1. Measurement tools used for speaking assessment
2. Effect sizes (Cohen's d or similar)
3. Sample sizes (intervention and control groups)
4. Organize in a table format

For missing values, indicate "Not reported".
```

**Optimal AI Response Structure**:
```
📊 RCT Studies: Measurement Tools & Effect Sizes (27 studies)

| Study | Measurement Tool | Intervention Group | Control Group | Effect Size | Outcome Measure | Page |
|-------|------------------|-------------------|---------------|-------------|-----------------|------|
| Smith et al. (2023) | IELTS Speaking Test | n=60 | n=60 | d=0.72 | Overall speaking score | p.12 |
| Chen et al. (2024) | TOEFL Speaking Section | n=45 | n=45 | d=0.58 | Integrated speaking tasks | p.8 |
| Lee et al. (2023) | Custom rubric (0-100) | n=85 | n=80 | d=0.61 | Fluency, accuracy, complexity | p.15 |
| Martinez et al. (2023) | ACTFL OPI | n=38 | n=35 | d=0.49 | Oral proficiency level | p.6 |
| Wang et al. (2024) | Conversation analysis | n=50 | n=48 | d=0.44 | Turn-taking, repair strategies | p.10 |
| Kim et al. (2023) | Pronunciation accuracy (%) | n=40 | n=38 | d=0.68 | Segmental accuracy | p.14 |
| Johnson et al. (2024) | Self-assessment survey | n=55 | n=52 | d=0.35 | Perceived fluency | p.9 |
| Garcia et al. (2023) | IELTS Speaking Test | n=72 | n=70 | d=0.55 | Pronunciation & fluency | p.11 |
| Brown et al. (2024) | Custom speaking test | n=65 | n=60 | d=0.42 | Communicative competence | p.7 |
| Davis et al. (2023) | TOEFL iBT Speaking | n=80 | n=78 | d=0.61 | Independent speaking | p.13 |
| Miller et al. (2024) | Versant English Test | n=48 | n=45 | d=0.51 | Sentence mastery, fluency | p.8 |
| Wilson et al. (2023) | IELTS Speaking + Custom | n=90 | n=88 | d=0.59 | Multiple dimensions | p.16 |
| Taylor et al. (2024) | LinguaFolio rubric | n=42 | n=40 | d=0.38 | CEFR levels | p.5 |
| Anderson et al. (2023) | Not reported | n=55 | n=53 | η²=0.14* | Speaking scores | p.9 |
| Thomas et al. (2024) | ACTFL rubric | n=35 | n=33 | d=0.47 | Novice to Intermediate | p.12 |
| Moore et al. (2023) | Custom analytic rubric | n=68 | n=65 | d=0.53 | 6 dimensions | p.10 |
| Jackson et al. (2024) | Conversation test | n=52 | n=50 | Not reported | Interaction quality | p.14 |
| White et al. (2023) | IELTS Speaking | n=78 | n=75 | d=0.66 | Overall band score | p.8 |
| Harris et al. (2024) | Pronunciation test | n=44 | n=42 | d=0.71 | Intelligibility rating | p.11 |
| Martin et al. (2023) | TOEFL Speaking | n=60 | n=58 | d=0.48 | Integrated tasks | p.9 |
| Clark et al. (2024) | Custom speaking exam | n=50 | n=48 | d=0.39 | Fluency & accuracy | p.7 |
| Lewis et al. (2023) | Self-recording analysis | n=38 | n=35 | Not reported | Speaking time | p.13 |
| Walker et al. (2024) | ACTFL OPI | n=42 | n=40 | d=0.52 | Proficiency level gain | p.6 |
| Hall et al. (2023) | Custom rubric | n=55 | n=52 | d=0.44 | Comprehensibility | p.15 |
| Allen et al. (2024) | IELTS + Pronunciation | n=70 | n=68 | d=0.57 | Multiple outcomes | p.12 |
| Young et al. (2023) | Conversation analysis | n=48 | n=45 | d=0.41 | Pragmatic competence | p.10 |
| King et al. (2024) | TOEFL iBT Speaking | n=82 | n=80 | d=0.63 | All 4 tasks | p.14 |

*Note: η² converted to d using standard formula

## 📈 Summary Statistics

**Measurement Tool Distribution**:
- IELTS Speaking Test: 8 studies (30%)
- TOEFL Speaking Section: 5 studies (19%)
- ACTFL OPI/Rubric: 4 studies (15%)
- Custom rubrics: 7 studies (26%)
- Other standardized tests: 3 studies (11%)

**Effect Size Statistics**:
- Mean effect size: d=0.53 (SD=0.11)
- Median effect size: d=0.52
- Range: d=0.35 to d=0.72
- 95% CI: d=0.48-0.58

**Sample Size Statistics**:
- Mean intervention group: n=58 (range 35-90)
- Mean control group: n=56 (range 33-88)
- Total participants across 27 RCTs: N=3,078

**Data Completeness**:
- Effect size reported: 25/27 studies (93%)
- Sample size reported: 27/27 studies (100%)
- Measurement tool specified: 26/27 studies (96%)

## 🔍 Methodological Notes

**Most Common Outcome Measures**:
1. Overall speaking proficiency (14 studies)
2. Fluency + accuracy (9 studies)
3. Pronunciation (6 studies)
4. Pragmatic/interactional competence (4 studies)

**Assessment Timing**:
- Immediate post-test: 27 studies (100%)
- Delayed post-test (1-3 months): 8 studies (30%)
- Long-term follow-up (>6 months): 0 studies

**Inter-rater Reliability** (when reported):
- Kappa > 0.80: 18 studies
- ICC > 0.85: 12 studies
- Not reported: 9 studies

📖 **Complete References**: All 27 RCT studies with full citation information

📊 **Export Options**:
- CSV format: `outputs/rct_effect_sizes.csv`
- Excel format: `outputs/rct_summary.xlsx`
- BibTeX entries: `outputs/rct_references.bib`

⚠️ **Data Quality Warning**: 2 studies did not report effect sizes, 1 study used non-standard measurement tool. Interpret with caution.
```

**Why This Response is Optimal**:
- Complete table with all requested fields
- "Not reported" explicitly stated for missing data
- Summary statistics for meta-analysis
- Methodological notes for quality assessment
- Export options for further analysis
- Data quality warnings

---

