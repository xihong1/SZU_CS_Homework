import zipfile
import xml.etree.ElementTree as ET
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\课件\数值计算方法\实验14'

files = ['李圣元2024150118实验十四.docx', '李圣元2024150118实验13.docx']

def extract_docx_text(path):
    with zipfile.ZipFile(path) as z:
        with z.open('word/document.xml') as f:
            content = f.read().decode('utf-8')
    
    # Use regex to extract all w:t text
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', content)
    
    # Group by paragraph (split by paragraph markers)
    # Actually, let's find paragraphs by splitting on <w:p
    paragraphs_raw = content.split('<w:p ')
    
    results = []
    for p_block in paragraphs_raw[1:]:  # skip first (before first paragraph)
        # Extract all w:t texts from this paragraph
        p_texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p_block)
        text = ''.join(p_texts)
        if text.strip():
            results.append(text.strip())
    
    return results

for f in files:
    path = os.path.join(base, f)
    print(f"\n{'='*80}")
    print(f"FILE: {f}")
    print('='*80)
    try:
        paras = extract_docx_text(path)
        for i, p in enumerate(paras):
            print(f"[{i}] {p}")
    except Exception as e:
        import traceback
        traceback.print_exc()
