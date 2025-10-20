# OpenAI Agent Builder Recommendations for DIY Kits

## Executive Summary

This document provides comprehensive recommendations for improving your OpenAI Agent workflow for the DIY Kits Master Bible Google Sheet. Based on deep analysis of 209 sheets (3 system sheets + 206 product sheets), we've identified key patterns, challenges, and solutions.

---

## 1. Data Structure Overview

### Total Sheets: 209
- **System Sheets (First 3):**
  - `Checklist` - Internal tracking and organization
  - `NEW Checklist` - Updated checklist format
  - `Format` - Template sheet for creating new products

- **Product Sheets (206):** Each represents a unique DIY flower product with standardized structure

### Product Sheet Structure

Every product sheet follows this pattern:

**Row 1:** Product category (e.g., "Wedding Kit Pack")  
**Row 2:** Product name + headers for different offerings:
- `Bouquet` sizes
- `DIY Combos` sizes  
- Bulk order information (Intimate, MD, Grande sizes)

**Row 3:** Column headers:
```
| A: Flower | B: Color | C: Type | D: Farm | E-H: Bouquet (XS,S,M,L) | J-L: DIY Combo (S,M,L) | M+: Bulk/Recipe |
```

**Row 4+:** Flower data with quantities for each size

**Bottom rows:** Total stem counts and pricing information

**Flower Types:**
- `FC` = Focal flowers (roses, main flowers)
- `FL` = Filler flowers (spray roses, carnations, berries)
- `L` = Line flowers (delphinium, snapdragon)
- `G` = Greenery (eucalyptus, ferns)
- `A` = Accent flowers

---

## 2. Tab Name Challenges & Solutions

### 🚨 Critical Issues Identified

1. **Truncated Names:** Some sheet names are cut off (e.g., "Jingle Bells Traditional Holida", "Wedding Decor Fresh White Flowe")
2. **Inconsistent Formatting:** Mixed use of spaces, `&`, `and`, parentheses
3. **Status Suffixes:** Many tabs have suffixes like "- done", "- Natuflora done", "- waiting quote"
4. **Duplicate Variations:** Similar names (e.g., "Crazy for Daisies (White)" vs "Crazy for Daisies (VDay)")
5. **Case Sensitivity:** Fuzzy matching fails on all-caps queries ("PRETTY IN PINK" scores only 29.6%)

### ✅ Recommended Solution: Smart Tab Lookup Agent Step

Create an **initial agent step** specifically for tab name resolution:

```
STEP 1: Tab Name Resolution Agent

Instructions:
"You are a sheet name matcher. Given a user's product query, find the best matching sheet from this list of 206 products.

IMPORTANT RULES:
1. Ignore case differences (treat "Pretty in Pink", "pretty in pink", and "PRETTY IN PINK" the same)
2. Ignore common variations: & vs and vs n, spacing differences, punctuation
3. Many sheet names have suffixes like '- done', '- Natuflora done', '- waiting quote' - IGNORE these when matching
4. Some names are truncated - match on the visible portion
5. If user says just a color or keyword (e.g., 'pink', 'rustic'), return the top 3 closest matches and ASK the user to clarify
6. Return ONLY the exact sheet name as it appears in the list

PRODUCT SHEET NAMES:
[Insert the complete list of 206 product sheets from output_sheet_names.json]

Examples:
- User: 'pretty in pink' → Return: 'Pretty in Pink'
- User: 'pretty pink' → Return: 'Pretty in Pink'
- User: 'traditional holiday' → Return: 'Jingle Bells Traditional Holida'
- User: 'pink' → Ask: 'I found multiple products with "pink": Pretty in Pink, Hot Poppin Pink, Playful Pink, Wicked Pink, etc. Which one do you need?'
"
```

**Why this works:**
- Dedicated single-purpose step = more reliable
- Explicit rules handle your specific edge cases
- Clarification logic prevents wrong guesses
- Returns exact sheet name for next step

---

## 3. Common User Questions & Answer Patterns

Based on the use case, here are the question types your agent must handle:

### Question Type 1: Tab Lookup
**Examples:**
- "Find the Pretty in Pink tab"
- "Where is Rustic Charm?"
- "Show me Garden Party"

**Agent Response Pattern:**
```
STEP 1: Tab Resolution
STEP 2: Confirm found: "I found the '{Sheet Name}' sheet. What would you like to know about it?"
```

---

### Question Type 2: Material List (Most Common!)
**Examples:**
- "What materials are in Pretty in Pink small?"
- "What's included in the Medium Joyous Noel kit?"
- "List all flowers in Merry & Bright Large"

**Agent Instructions:**
```
After finding the correct sheet:

1. Read rows starting from row 4 until you hit a row starting with "Total Stems"
2. For each flower row:
   - Column A = Flower name
   - Column B = Color  
   - Column C = Type (FC/FL/L/G/A)
   - Columns E-H = Bouquet sizes (XS, S, M, L)
   - Columns J-L = DIY Combo sizes (S, M, L)
3. Skip rows where Column A is empty or just a type code (FC, FL, etc.)
4. Extract the requested size quantities
5. Format response as:
   
   {Product Name} - {Size} Kit
   - {Flower Name} ({Color}): {Quantity} stems
   - {Flower Name} ({Color}): {Quantity} stems
   Total stems: {Total}
```

**Column Index Reference:**
- Bouquet XS = Column E (index 5)
- Bouquet S = Column F (index 6)
- Bouquet M = Column G (index 7)
- Bouquet L = Column H (index 8)
- DIY Combo S = Column J (index 10)
- DIY Combo M = Column K (index 11)
- DIY Combo L = Column L (index 12)

---

### Question Type 3: Specific Flower Quantity
**Examples:**
- "How many roses in Pretty in Pink Medium?"
- "Does Merry & Bright have spray roses?"
- "How many stems of delphinium in Large?"

**Agent Instructions:**
```
1. Find the sheet
2. Search Column A for the flower name (use flexible matching: "rose" matches "Jessika Rose", "Secret Garden Rose", etc.)
3. Check the appropriate size column
4. If multiple flowers match (e.g., multiple rose varieties), list all:
   "Pretty in Pink Medium contains:
   - Jessika Rose (Light Pink): 30 stems
   - Secret Garden Rose (Blush): 25 stems
   Total roses: 55 stems"
```

---

### Question Type 4: Size Comparison
**Examples:**
- "What's the difference between Small and Medium?"
- "Compare all sizes for Pretty in Pink"
- "How many more stems in Large vs Medium?"

**Agent Instructions:**
```
Read the "Total Stems" row (usually second-to-last row with data)
Column D will say "Total Stems"
Columns E-H have bouquet totals
Columns J-L have combo totals
```

---

### Question Type 5: Total Stem Count
**Examples:**
- "How many total stems in Pretty in Pink Medium?"
- "What's the stem count for Large?"

**Agent Instructions:**
```
Find the row where Column D = "Total Stems"
Read the appropriate size column:
- Bouquet sizes: Columns E-H
- DIY Combo sizes: Columns J-L
```

**From our analysis, Pretty in Pink totals are:**
- Bouquet: XS=7, S=10, M=18, L=29
- DIY Combo: S=53, M=115, L=205

---

## 4. Error Handling & Edge Cases

### Case 1: Product Not Found
```
User: "Find the Unicorn Rainbow Sparkle kit"

Agent Response:
"I couldn't find a product called 'Unicorn Rainbow Sparkle' in our DIY kits. 

Would you like to:
1. Browse all available products
2. Search by color/theme (e.g., 'pink', 'rustic', 'wedding')
3. Try a different product name"
```

### Case 2: Ambiguous Query
```
User: "How many stems?"

Agent Response:
"I need a bit more information:
1. Which product? (e.g., Pretty in Pink, Merry & Bright)
2. Which size? (Bouquet: XS/S/M/L or DIY Combo: S/M/L)
3. Specific flower or total stems?"
```

### Case 3: Size Not Available
```
User: "How many stems in Pretty in Pink XL?"

Agent Response:
"Pretty in Pink doesn't have an XL size. Available sizes are:
- Bouquet: XS, S, M, L
- DIY Combo: S, M, L

Which size would you like to know about?"
```

### Case 4: Empty/Missing Data
```
If a cell is empty or 0:

Agent Response:
"The Medium size for Pretty in Pink includes 30 Jessika Roses, but this flower is not included in the Bouquet XS size."
```

---

## 5. Fuzzy Matching Configuration

**Recommended Threshold: 70%** (Your current 60% is too low)

### Test Results from Analysis:

| User Query | Best Match | Score | Status |
|------------|-----------|-------|--------|
| "Pretty in Pink" | Pretty in Pink | 100% | ✅ Perfect |
| "pretty pink" | Pretty in Pink | 72% | ✅ Good |
| "Pretty n Pink" | Pretty in Pink | 96% | ✅ Excellent |
| "Pretty & Pink" | Pretty in Pink | 81% | ✅ Good |
| "PRETTY IN PINK" | Pink Fall DIY | 30% | ❌ FAILS |
| "Garden Party" | Kale Garden Party | 83% | ✅ Good |
| "Rustic" | Wild and Rustic | 57% | ⚠️ Below threshold |
| "rustic charm" | Lucky Charm | 61% | ⚠️ Wrong match! |

**Critical Fix Needed:** Your Zapier tool must convert all queries to Title Case before matching to avoid the all-caps failure.

**Preprocessing Rules:**
```python
# Pseudo-code for your Zapier preprocessing
def preprocess_query(user_input):
    # Convert to title case
    query = user_input.title()
    
    # Normalize common variations
    query = query.replace(" And ", " & ")
    query = query.replace(" N ", " in ")
    
    # Remove status suffixes before matching
    suffixes_to_ignore = ["- done", "- Natuflora done", "- waiting quote", "- sample"]
    for suffix in suffixes_to_ignore:
        query = query.replace(suffix, "")
    
    return query.strip()
```

---

## 6. Testing Plan

We've generated 13+ test scenarios. Here are the critical ones:

### Priority 1: Must Pass ✅

1. **Exact Match**
   - Query: "Find Pretty in Pink"
   - Expected: Find sheet "Pretty in Pink"

2. **Case Insensitive**
   - Query: "find pretty in pink" (all lowercase)
   - Expected: Find sheet "Pretty in Pink"

3. **All Caps**  
   - Query: "PRETTY IN PINK"
   - Expected: Find sheet "Pretty in Pink"

4. **Material List - Small**
   - Query: "What materials are in Pretty in Pink small?"
   - Expected: List all flowers with S quantities from DIY Combo column J

5. **Material List - Medium**
   - Query: "What's in Merry & Bright Medium?"
   - Expected: List all flowers with M quantities

6. **Total Stems**
   - Query: "How many total stems in Pretty in Pink Large?"
   - Expected: "205 stems" (from Total Stems row, column L)

### Priority 2: Should Pass ⚠️

7. **Fuzzy Match - Abbreviation**
   - Query: "Pretty n Pink"
   - Expected: Find "Pretty in Pink"

8. **Fuzzy Match - Symbol**
   - Query: "Black & White"
   - Expected: Find "Classic Black & White"

9. **Truncated Name**
   - Query: "Jingle Bells Traditional Holiday"
   - Expected: Find "Jingle Bells Traditional Holida"

### Priority 3: Error Handling 🛡️

10. **Nonexistent Product**
    - Query: "Find Rainbow Unicorn"
    - Expected: "Product not found" + helpful suggestions

11. **Ambiguous Query**
    - Query: "How many roses?"
    - Expected: Ask for clarification (which product? which size?)

12. **Invalid Size**
    - Query: "Pretty in Pink XXL"
    - Expected: "Size not available" + list valid sizes

---

## 7. Agent Workflow Architecture

### Recommended Multi-Agent Structure

```
┌─────────────────────────────────────────┐
│         User Query                       │
│  "What's in Pretty in Pink Medium?"      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  AGENT 1: Query Understanding            │
│  - Extract product name                  │
│  - Extract size (if mentioned)           │
│  - Classify question type                │
│  - Handle case normalization             │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  AGENT 2: Sheet Lookup                   │
│  - Use fuzzy matching with 70% threshold │
│  - Apply preprocessing rules             │
│  - Return exact sheet name OR            │
│  - Ask for clarification if ambiguous    │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  ZAPIER: Google Sheets Read              │
│  - Read the identified sheet             │
│  - Range: A1:Z100 (get full structure)   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  AGENT 3: Data Extraction                │
│  - Parse based on question type          │
│  - Extract relevant rows/columns         │
│  - Calculate totals if needed            │
│  - Format response                       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  AGENT 4: Response Formatting            │
│  - Present data in readable format       │
│  - Add helpful context                   │
│  - Suggest related questions             │
└──────────────────┬──────────────────────┘
                   │
                 User
```

---

## 8. Improved Agent Instructions

### For Your Google Sheets Zapier Node:

**OLD (Current):**
```
"You have access to a google sheet which people use to go find questions related to DIY 
products. each DIY product is a tab name and isn't exact so sometimes it can be hard to 
match a product with its exact tab. On that tab it displays information regarding that 
product and answers any question the user would be using that sheet for."
```

**NEW (Recommended):**
```
SYSTEM: DIY Kits Product Information Assistant

You have access to the "DIY Kits Master Bible for Merchandising" Google Sheet containing 
206 DIY flower product sheets. Each product is a separate sheet/tab.

SHEET STRUCTURE:
- First 3 sheets are system sheets (Checklist, NEW Checklist, Format) - IGNORE these
- Sheets 4-209 are product sheets
- Each product sheet has:
  * Row 1: Product category
  * Row 2: Product name and offering types
  * Row 3: Column headers (Flower, Color, Type, Farm, Sizes...)
  * Row 4+: Flower data with quantities per size
  * Bottom rows: Total stems and pricing

COLUMN REFERENCE:
- A: Flower name
- B: Color
- C: Type (FC=Focal, FL=Filler, L=Line, G=Greenery, A=Accent)
- D: Farm
- E-H: Bouquet sizes (XS, S, M, L)
- J-L: DIY Combo sizes (S, M, L)

SIZE OPTIONS:
- Bouquet: Extra Small (XS), Small (S), Medium (M), Large (L)
- DIY Combo: Small (S), Medium (M), Large (L)

SHEET NAME MATCHING RULES:
1. Convert user input to Title Case before matching
2. Ignore: '- done', '- Natuflora done', '- waiting quote', etc.
3. Treat '&', 'and', 'n' as equivalent
4. Use fuzzy matching with 70% threshold
5. If <70% match or query too vague, list top 3 matches and ask user to clarify

WORKFLOW:
1. Extract product name from user query
2. Find matching sheet (use fuzzy matching)
3. If found: Read sheet data (range A1:Z100)
4. Parse based on question type:
   - Material list: Read rows 4 to "Total Stems", extract flower names and quantities
   - Specific flower: Search Column A, return quantity from size column
   - Total stems: Read "Total Stems" row
5. Format response with clear sections and totals

ERROR HANDLING:
- Product not found: Suggest similar products or ask for clarification
- Missing size info: List available sizes
- Ambiguous query: Ask for product name and/or size
- Empty data: Explain what's not available

RESPONSE FORMAT:
Always structure responses as:
1. Confirm product and size
2. List data clearly with labels
3. Provide totals
4. Offer to answer related questions

Example:
"Pretty in Pink - DIY Combo Medium Kit

Focal Flowers (FC):
- Jessika Rose (Light Pink): 30 stems
- Secret Garden Rose (Blush): 25 stems

Filler Flowers (FL):
- Lydia Spray Rose (Light Pink): 15 stems
- Chablis Spray Rose (Cream): 15 stems
- Spray Stock (Light Pink): 10 stems

Line Flowers (L):
- Delphinium (White): 20 stems

Total: 115 stems

Would you like to see another size or a different product?"
```

---

## 9. Product Sheet Name Reference

Save this list in your agent's knowledge base or as a lookup table:

```
PRODUCT SHEETS (206 total):

Holiday Collections:
- Merry & Bright
- Joyous Noel
- Jingle Bells Traditional Holida
- Modern Holiday Glam
- Antique Holiday Rose
- Peppermint Candy

Pink Collections:
- Pretty in Pink
- Hot Poppin Pink
- Playful Pink
- Cupids Flirty Pink
- Wicked Pink - Agrogana done
- Wicked Tinted Pink - Natuflora 
- Sincerely Pink - Natuflora done
- Shades Of Pink
- Delightfully Pink
- Dreamy Pink
- Tasty Pink Cake
- Pink Fall DIY
- Pink Paradise
- Pink Lovebirds
- Blushing Peach
- Blush Butterfly
- Blush & Berries - Natuflora don
- Blushing Berry - Natuflora done
- Burgundy Blush
- With Love - Natuflora done

[...continue with all 206 sheets grouped by theme/color...]

See output_sheet_names.json for complete list.
```

---

## 10. Next Steps & Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Update Zapier instructions with new detailed instructions above
- [ ] Add product sheet names list to agent knowledge base
- [ ] Implement query preprocessing (Title Case conversion)
- [ ] Set fuzzy matching threshold to 70%

### Phase 2: Multi-Agent Setup (Week 2)
- [ ] Create Query Understanding agent (extract product + size)
- [ ] Create Sheet Lookup agent (dedicated tab matching)
- [ ] Create Data Extraction agent (parse sheet structure)
- [ ] Create Response Formatting agent (user-friendly output)

### Phase 3: Testing (Week 3)
- [ ] Run all 13 priority test scenarios
- [ ] Test with real employee queries
- [ ] Collect failure cases and iterate
- [ ] Document edge cases

### Phase 4: Optimization (Week 4)
- [ ] Add caching for frequently accessed sheets
- [ ] Create quick-answer templates for common questions
- [ ] Add conversational memory (multi-turn conversations)
- [ ] Implement feedback collection

---

## 11. Common Pitfalls to Avoid

### ❌ DON'T:
1. Use a single generic instruction - break into specialized agents
2. Rely on exact string matching - always use fuzzy matching
3. Ignore case sensitivity - normalize all inputs
4. Return raw spreadsheet data - format it nicely
5. Guess when unsure - always ask for clarification
6. Forget to handle empty cells - check for null/0 values
7. Hard-code column numbers without labels - columns might shift

### ✅ DO:
1. Use multi-agent workflow with clear responsibilities
2. Implement robust fuzzy matching with preprocessing
3. Convert all queries to Title Case
4. Format responses with clear sections and totals
5. Ask clarifying questions when ambiguous
6. Handle empty/missing data gracefully
7. Reference columns by header names when possible

---

## 12. Success Metrics

Track these KPIs to measure agent performance:

1. **Accuracy Rate:** % of queries that return correct information
   - Target: >95%

2. **Resolution Rate:** % of queries answered without human intervention
   - Target: >85%

3. **Clarification Rate:** % of queries requiring follow-up
   - Target: <20%

4. **Sheet Matching Accuracy:** % of product names correctly matched
   - Target: >98%

5. **Response Time:** Average time to answer
   - Target: <10 seconds

6. **User Satisfaction:** Employee feedback
   - Target: 4.5/5 stars

---

## 13. Resources Generated

This analysis produced these files in your repo:

1. **output_sheet_names.json** - Complete list of all 209 sheets
2. **output_structure_analysis.json** - Detailed structure of first 3 + sample product sheets
3. **output_fuzzy_matching_tests.json** - Fuzzy matching test results with scores
4. **output_common_questions.json** - Bank of common question templates
5. **output_test_scenarios.json** - 13+ comprehensive test cases
6. **output_pretty_in_pink_structure.json** - Deep dive example of one product sheet
7. **analyze_diy_data.py** - Full analysis script (rerunnable)
8. **deep_dive_product_sheet.py** - Deep dive script for individual sheets

---

## Questions or Issues?

If you encounter issues during implementation:

1. Re-run the analysis scripts on updated data
2. Check the test scenarios file for expected vs actual behavior
3. Review the fuzzy matching results to tune threshold
4. Use the Pretty in Pink deep dive as a reference structure

---

**Document Version:** 1.0  
**Created:** October 20, 2025  
**Last Updated:** October 20, 2025  
**Contact:** Based on DIY Kits Master Bible for Merchandising.xlsx

