# DIY Kits Data Analysis

Analysis tools and recommendations for the DIY Kits Master Bible Google Sheet / Excel workbook.

## Purpose

This project provides comprehensive analysis of the DIY Kits product database to help optimize the OpenAI Agent Builder workflow for querying product information. The analysis covers 209 sheets (3 system sheets + 206 product sheets).

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Files

### Analysis Scripts
- **`analyze_diy_data.py`** - Main analysis script that:
  - Maps all 209 sheet names
  - Analyzes structure differences between system sheets and product sheets
  - Tests fuzzy matching algorithms for tab name lookup
  - Generates common question banks
  - Creates test scenarios

- **`deep_dive_product_sheet.py`** - Deep dive into a single product sheet ("Pretty in Pink") to understand exact column structure

### Output Files (Generated)
- **`output_sheet_names.json`** - Complete list of all sheets, categorized
- **`output_structure_analysis.json`** - Detailed structure analysis of first 3 sheets + sample product sheets
- **`output_fuzzy_matching_tests.json`** - Fuzzy matching test results with scores
- **`output_common_questions.json`** - Bank of common question types users might ask
- **`output_test_scenarios.json`** - Comprehensive test cases for validating the agent
- **`output_pretty_in_pink_structure.json`** - Deep dive structure of one product sheet

### Documentation
- **`AGENT_RECOMMENDATIONS.md`** - ⭐ **MAIN DOCUMENT** - Comprehensive recommendations for setting up your OpenAI Agent Builder workflow

## Quick Start

Run the main analysis:
```bash
source venv/bin/activate
python analyze_diy_data.py
```

Run deep dive on a specific product:
```bash
python deep_dive_product_sheet.py
```

## Key Insights

### Data Structure
- **209 total sheets**
- **3 system sheets:** Checklist, NEW Checklist, Format
- **206 product sheets** with standardized structure:
  - Row 1: Product category
  - Row 2: Product name + headers
  - Row 3: Column headers (Flower, Color, Type, Farm, Sizes...)
  - Row 4+: Flower data with quantities
  - Bottom rows: Total stems and pricing

### Common Issues Identified
1. **Truncated sheet names** (e.g., "Jingle Bells Traditional Holida")
2. **Inconsistent formatting** (& vs and vs n)
3. **Status suffixes** in names ("- done", "- waiting quote")
4. **Case sensitivity** in fuzzy matching (all-caps queries fail)

### Recommendations
See `AGENT_RECOMMENDATIONS.md` for:
- Multi-agent workflow architecture
- Fuzzy matching configuration (70% threshold)
- Detailed agent instructions
- Common question handling patterns
- Error handling strategies
- 13+ test scenarios
- Implementation checklist

## Product Sheet Column Structure

```
| A        | B     | C    | D    | E-H (Bouquet)    | J-L (DIY Combo)  | M+ (Bulk/Recipe) |
|----------|-------|------|------|------------------|------------------|------------------|
| Flower   | Color | Type | Farm | XS / S / M / L   | S / M / L        | Recipe, etc.     |
```

**Flower Types:**
- `FC` = Focal flowers (roses, main flowers)
- `FL` = Filler flowers (spray roses, carnations)
- `L` = Line flowers (delphinium, snapdragon)
- `G` = Greenery (eucalyptus, ferns)
- `A` = Accent flowers

## Size Options

**Bouquet Sizes:**
- XS (Extra Small)
- S (Small)
- M (Medium)
- L (Large)

**DIY Combo Sizes:**
- S (Small)
- M (Medium)
- L (Large)

## Fuzzy Matching Results

The analysis tested 12 different query patterns with fuzzy matching:

| Query              | Best Match         | Score | Status |
|--------------------|--------------------|-------|--------|
| "Pretty in Pink"   | Pretty in Pink     | 100%  | ✅ Perfect |
| "pretty pink"      | Pretty in Pink     | 72%   | ✅ Good |
| "Pretty n Pink"    | Pretty in Pink     | 96%   | ✅ Excellent |
| "PRETTY IN PINK"   | Pink Fall DIY      | 30%   | ❌ FAILS |
| "Garden Party"     | Kale Garden Party  | 83%   | ✅ Good |

**Critical Finding:** All-caps queries fail. Solution: Convert all user queries to Title Case before matching.

## Testing

The project includes 13+ test scenarios covering:
1. Exact matching
2. Case insensitivity
3. Fuzzy matching
4. Material list queries
5. Total stem count queries
6. Error handling (nonexistent products, ambiguous queries, invalid sizes)

See `output_test_scenarios.json` for full details.

## Next Steps

1. Read `AGENT_RECOMMENDATIONS.md` thoroughly
2. Implement the multi-agent workflow in OpenAI Agent Builder
3. Update your Zapier Google Sheets integration with new instructions
4. Run all test scenarios from `output_test_scenarios.json`
5. Iterate based on real employee usage

## Contributing

To add more analysis or modify existing scripts:

1. Edit the Python scripts
2. Re-run the analysis
3. Check the updated JSON output files
4. Update documentation as needed

## Questions?

Review the comprehensive recommendations in `AGENT_RECOMMENDATIONS.md` which covers:
- Complete agent instructions
- Error handling patterns
- Implementation checklist
- Success metrics
- Common pitfalls to avoid

---

**Last Updated:** October 20, 2025

