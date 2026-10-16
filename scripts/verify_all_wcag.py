import re
import os
import sys

def rel_lum(hex_col):
    hex_col = hex_col.strip('#')
    if len(hex_col) == 3:
        hex_col = ''.join(c * 2 for c in hex_col)
    rgb = [int(hex_col[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

def contrast_ratio(c1, c2):
    l1, l2 = rel_lum(c1), rel_lum(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

dist_path = os.path.join(os.path.dirname(__file__), '..', 'dist', 'index.html')

if not os.path.exists(dist_path):
    print(f"Error: Build output not found at {dist_path}. Run 'npm run build' first.")
    sys.exit(1)

with open(dist_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("="*80)
print("RAMESH PAL RESEARCH - WCAG 2.2 AA VERIFICATION AUDIT SUITE")
print("="*80)

failures = 0

# -------------------------------------------------------------
# 1. ISSUE 1: LINK & BUTTON ACCESSIBLE NAMES (WCAG 2.5.3 & 4.1.2)
# -------------------------------------------------------------
print("\n" + "="*50)
print("SECTION 1: LINK & BUTTON ACCESSIBLE NAMES")
print("="*50)

tag_pattern = re.compile(r'(<(a|button)\b([^>]*)>(.*?)</\2>)', re.DOTALL)
elements = tag_pattern.findall(html)
print(f"Total interactive elements (<a> and <button>): {len(elements)}")

mismatches = []
missing_names = []

for idx, (full, tag, attrs, content) in enumerate(elements, 1):
    content_visible = re.sub(r'<[^>]*aria-hidden=[\"\']true[\"\'][^>]*>.*?</[^>]+>', ' ', content, flags=re.DOTALL)
    clean_text = ' '.join(re.sub(r'<[^>]+>', ' ', content_visible).split())
    aria_label_m = re.search(r'aria-label=[\"\']([^\"\']*)[\"\']', attrs)
    aria_val = aria_label_m.group(1).strip() if aria_label_m else ''

    if not clean_text and not aria_val and 'title=' not in attrs:
        missing_names.append((idx, tag, full[:60]))
        failures += 1

    if clean_text and clean_text != '&times;':
        norm_aria = ' '.join(aria_val.split()).lower()
        norm_clean = clean_text.lower()
        if aria_val and norm_clean not in norm_aria and not norm_aria.startswith(norm_clean):
            mismatches.append((idx, tag, clean_text, aria_val))
            failures += 1

if not missing_names:
    print(f"[PASS] 100% of {len(elements)} interactive controls have accessible names!")
else:
    print(f"[FAIL] Found {len(missing_names)} controls missing accessible names: {missing_names}")

if not mismatches:
    print(f"[PASS] 100% of labeled controls pass WCAG 2.5.3 (Label in Name)!")
else:
    print(f"[FAIL] Found {len(mismatches)} Label-in-Name mismatches: {mismatches}")


# -------------------------------------------------------------
# 2. ISSUE 2: DECORATIVE SVGS & SYMBOLS (WCAG 1.1.1)
# -------------------------------------------------------------
print("\n" + "="*50)
print("SECTION 2: DECORATIVE CONTENT (SVGs & SYMBOLS)")
print("="*50)

all_svgs = list(re.finditer(r'<svg\b([^>]*)>', html, re.I))
svg_unhidden = [m.group(0) for m in all_svgs if 'aria-hidden="true"' not in m.group(1)]

if not svg_unhidden:
    print(f"[PASS] 100% of SVGs ({len(all_svgs)}/{len(all_svgs)}) have aria-hidden='true'!")
else:
    print(f"[FAIL] {len(svg_unhidden)} SVGs missing aria-hidden='true': {svg_unhidden[:3]}")
    failures += len(svg_unhidden)

symbol_targets = [
    ('&rarr;', r'<span[^>]*aria-hidden=[\"\']true[\"\'][^>]*>&rarr;</span>'),
    ('&times;', r'<span[^>]*aria-hidden=[\"\']true[\"\'][^>]*>&times;</span>'),
    ('&bull;', r'<span[^>]*aria-hidden=[\"\']true[\"\'][^>]*>&bull;</span>'),
    ('&middot;', r'<span[^>]*aria-hidden=[\"\']true[\"\'][^>]*>&middot;</span>'),
]

for sym, pat in symbol_targets:
    total_raw = html.count(sym)
    wrapped_matches = len(re.findall(pat, html))
    if total_raw > 0:
        if total_raw == wrapped_matches:
            print(f"[PASS] Symbol '{sym}': all {total_raw} instances wrapped in aria-hidden='true'")
        else:
            print(f"[FAIL] Symbol '{sym}': {total_raw} total, only {wrapped_matches} wrapped!")
            failures += (total_raw - wrapped_matches)


# -------------------------------------------------------------
# 3. ISSUE 3: ACCESSIBLE TABLES (WCAG 1.3.1)
# -------------------------------------------------------------
print("\n" + "="*50)
print("SECTION 3: ACCESSIBLE DATA TABLES")
print("="*50)

tables = list(re.finditer(r'<table\b([^>]*)>(.*?)</table>', html, re.DOTALL))
print(f"Total tables: {len(tables)}")
for i, t in enumerate(tables, 1):
    content = t.group(2)
    has_caption = '<caption' in content
    ths = list(re.finditer(r'<th\b([^>]*)>(.*?)</th>', content, re.DOTALL))
    missing_scope = [th.group(0) for th in ths if 'scope=' not in th.group(1)]
    
    if not has_caption:
        print(f"[FAIL] Table #{i} missing <caption> element!")
        failures += 1
    else:
        print(f"[PASS] Table #{i} contains semantic <caption>")
        
    if missing_scope:
        print(f"[FAIL] Table #{i} has {len(missing_scope)} <th> elements missing scope attribute!")
        failures += len(missing_scope)
    else:
        print(f"[PASS] Table #{i}: all {len(ths)} <th> elements have valid scope attributes")


# -------------------------------------------------------------
# 4. ISSUE 4: COLOR CONTRAST VERIFICATION (WCAG 1.4.3)
# -------------------------------------------------------------
print("\n" + "="*50)
print("SECTION 4: COLOR CONTRAST VERIFICATION")
print("="*50)

palette_checks = [
    ("Charcoal Pine on Ivory Canvas (#111827 on #FAF9F5)", "#111827", "#FAF9F5", 4.5),
    ("Muted Charcoal on Ivory Canvas (#374151 on #FAF9F5)", "#374151", "#FAF9F5", 4.5),
    ("Dehradun Mountain Pine on Ivory Canvas (#064E3B on #FAF9F5)", "#064E3B", "#FAF9F5", 4.5),
    ("Charcoal Pine on White Card (#111827 on #FFFFFF)", "#111827", "#FFFFFF", 4.5),
    ("Muted Charcoal on White Card (#374151 on #FFFFFF)", "#374151", "#FFFFFF", 4.5),
    ("Burnished Bronze on Amber Parchment (#92400E on #FEF3C7)", "#92400E", "#FEF3C7", 4.5),
    ("White text on Mountain Pine (#FFFFFF on #064E3B)", "#FFFFFF", "#064E3B", 4.5),
    ("White text on Charcoal Pine (#FFFFFF on #111827)", "#FFFFFF", "#111827", 4.5),
    ("Slate 300 on Alpine Obsidian Footer (#CBD5E1 on #0E161B)", "#CBD5E1", "#0E161B", 4.5),
]

for name, c1, c2, req in palette_checks:
    cr = contrast_ratio(c1, c2)
    res = "PASS" if cr >= req else "FAIL"
    if res == "FAIL":
        failures += 1
    print(f"[{res}] {name} -> {cr:.2f}:1 (Required: {req}:1)")

print("\n" + "="*80)
if failures == 0:
    print("ALL WCAG 2.2 AA VERIFICATION CHECKS PASSED (ZERO DEFECTS)!")
else:
    print(f"TOTAL FAILURES DETECTED: {failures}")
print("="*80)

sys.exit(0 if failures == 0 else 1)
