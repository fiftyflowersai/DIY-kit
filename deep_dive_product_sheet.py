"""
Deep dive into a single product sheet to fully understand the structure
"""

import openpyxl
import pandas as pd
import json

EXCEL_PATH = "data/DIY Kits Master Bible for Merchandising.xlsx"
print("Loading workbook...")
wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)

# Let's do a deep dive on "Pretty in Pink" since that was the example
sheet_name = "Pretty in Pink"
print(f"\n{'='*80}")
print(f"DEEP DIVE: {sheet_name}")
print(f"{'='*80}\n")

sheet = wb[sheet_name]

# Read first 30 rows to understand full structure
print("First 30 rows of the sheet:\n")
data = []
for row_idx, row in enumerate(sheet.iter_rows(max_row=30, values_only=True), 1):
    data.append(row)
    non_empty = [str(cell) if cell is not None else "" for cell in row]
    print(f"Row {row_idx:2d}: {non_empty[:20]}")  # Show first 20 columns

print("\n" + "="*80)
print("STRUCTURE ANALYSIS")
print("="*80)

# Row 1: Product category/type
row1 = [cell for cell in data[0] if cell]
print(f"\nRow 1 (Product Type): {row1}")

# Row 2: Product name and main headers
row2 = [cell for cell in data[1] if cell]
print(f"\nRow 2 (Product Name & Headers): {row2}")

# Row 3: Column headers
row3 = list(data[2])
print(f"\nRow 3 (Column Headers): {row3[:20]}")

# Identify column structure
print("\n" + "-"*80)
print("COLUMN STRUCTURE:")
print("-"*80)

# The columns appear to be:
# Column A: Flower name
# Column B: Color
# Column C: Type (FC = Focal, FL = Filler, LN = Line, GR = Greenery)
# Column D: Farm name
# Then sizes for Bouquet and DIY Combos

bouquet_sizes = ["XS", "S", "M", "L"]  # Columns E, F, G, H
combo_sizes = ["S", "M", "L"]  # Columns I, J, K

print("\nExpected columns:")
print("  A: Flower Name")
print("  B: Color")
print("  C: Type (FC/FL/LN/GR)")
print("  D: Farm")
print("  E-H: Bouquet sizes (XS, S, M, L)")
print("  I-K: DIY Combo sizes (S, M, L)")
print("  L+: Additional columns (Recipe, bulk sizes, notes)")

# Now let's parse the actual flower data
print("\n" + "="*80)
print("FLOWER DATA (Starting from row 4)")
print("="*80)

flowers = []
for row_idx in range(3, min(len(data), 30)):  # Start from row 4 (index 3)
    row = data[row_idx]
    
    # Skip empty rows or rows without flower names
    if not row[0] or not isinstance(row[0], str):
        continue
    
    # Skip rows that are section dividers
    if row[0] in ['FC ', 'FL', 'LN', 'GR']:
        continue
        
    flower_name = row[0]
    color = row[1] if len(row) > 1 else None
    flower_type = row[2] if len(row) > 2 else None
    farm = row[3] if len(row) > 3 else None
    
    bouquet_xs = row[4] if len(row) > 4 else None
    bouquet_s = row[5] if len(row) > 5 else None
    bouquet_m = row[6] if len(row) > 6 else None
    bouquet_l = row[7] if len(row) > 7 else None
    
    combo_s = row[8] if len(row) > 8 else None
    combo_m = row[9] if len(row) > 9 else None
    combo_l = row[10] if len(row) > 10 else None
    
    flower_info = {
        "name": flower_name,
        "color": color,
        "type": flower_type,
        "farm": farm,
        "bouquet": {
            "XS": bouquet_xs,
            "S": bouquet_s,
            "M": bouquet_m,
            "L": bouquet_l
        },
        "combo": {
            "S": combo_s,
            "M": combo_m,
            "L": combo_l
        }
    }
    
    flowers.append(flower_info)
    print(f"\n{flower_name} ({color})")
    print(f"  Type: {flower_type}, Farm: {farm}")
    print(f"  Bouquet sizes: XS={bouquet_xs}, S={bouquet_s}, M={bouquet_m}, L={bouquet_l}")
    print(f"  Combo sizes: S={combo_s}, M={combo_m}, L={combo_l}")

# Save the structured data
output = {
    "sheet_name": sheet_name,
    "product_type": row1[0] if row1 else None,
    "product_name": row2[0] if row2 else None,
    "flowers": flowers
}

with open(f"output_pretty_in_pink_structure.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n✓ Saved detailed structure to: output_pretty_in_pink_structure.json")

wb.close()
print("\nDone!")

