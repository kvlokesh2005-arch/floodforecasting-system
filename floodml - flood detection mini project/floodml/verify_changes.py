import os

os.chdir(os.path.dirname(__file__))

files = [
    'app.py',
    'satellite_upload_module.py',
    'UI_UX_IMPROVEMENTS_REPORT.md',
    'FINAL_UPDATE_SUMMARY.txt'
]

print("File Verification:")
print("-" * 50)

all_good = True
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024
        print(f"OK: {f} ({size:.1f} KB)")
    else:
        print(f"MISSING: {f}")
        all_good = False

print("-" * 50)
if all_good:
    print("Status: ALL FILES VERIFIED")
else:
    print("Status: SOME FILES MISSING")
