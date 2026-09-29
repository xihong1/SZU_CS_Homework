import docx
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\课件\数值计算方法\实验14'

files = ['李圣元2024150118实验十四.docx', '李圣元2024150118实验13.docx', '数值计算方法实验14.docx']

for f in files:
    path = os.path.join(base, f)
    print(f"\n{'='*80}")
    print(f"FILE: {f}")
    print('='*80)
    try:
        doc = docx.Document(path)
        for i, p in enumerate(doc.paragraphs):
            if p.text.strip():
                print(f"[{i}] {p.text}")
        
        # Also extract tables
        for ti, table in enumerate(doc.tables):
            print(f"\n--- Table {ti} ---")
            for ri, row in enumerate(table.rows):
                cells = [cell.text for cell in row.cells]
                print(f"  Row {ri}: {' | '.join(cells)}")
    except Exception as e:
        print(f"Error: {e}")
