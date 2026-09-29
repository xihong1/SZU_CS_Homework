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
            tree = ET.parse(f)
    
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    paragraphs = []
    for p in tree.findall('.//w:p', ns):
        texts = []
        for t in p.findall('.//w:t', ns):
            if t.text:
                texts.append(t.text)
        text = ''.join(texts)
        if text.strip():
            paragraphs.append(text)
    
    return paragraphs

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
