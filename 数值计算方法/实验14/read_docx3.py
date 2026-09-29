import zipfile
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\课件\数值计算方法\实验14'

files = ['李圣元2024150118实验十四.docx', '李圣元2024150118实验13.docx']

for f in files:
    path = os.path.join(base, f)
    print(f"\n{'='*80}")
    print(f"FILE: {f}")
    print('='*80)
    try:
        with zipfile.ZipFile(path) as z:
            # List all files
            print("Files in archive:")
            for name in z.namelist():
                print(f"  {name}")
            
            # Try to read document.xml
            with z.open('word/document.xml') as f:
                content = f.read().decode('utf-8')
                # Print first 5000 chars
                print(f"\ndocument.xml content (first 5000 chars):")
                print(content[:5000])
    except Exception as e:
        import traceback
        traceback.print_exc()
