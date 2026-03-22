import os

base_path = r"G:\Mi unidad\DICTAMENES_2022"
subfolders = [
    "2_DT_STA_FEMA_025_2022_KM4_VALLE_DE_ANGELES",
    "4_APOYOS",
    "5_ANALASIS EXPORT SPS",
    "6_A_SITIO SAN PEDRO CATAMAS",
    "A2_DICTAMENES",
    "appsheet",
    "ASERRADERO BORJAS",
    "CORRALITOS",
    "JARAGUA",
    "Jaragua_2022",
    "JOHONNY_DUBON_MARAITA",
    "NE-0298-001-0412-2018_GUALACO",
    "NOEMY_BRUNER_EL_HATILLO",
    "SITIO SAN PEDRO CATAMAS",
    "VERO"
]

results = {}
print("Scanning folders...")
for folder in subfolders:
    path = os.path.join(base_path, folder)
    results[folder] = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx', '.doc')):
                    results[folder].append(os.path.join(root, file))
    else:
        print(f"Path does not exist: {path}")

print("-" * 60)
for folder, files in results.items():
    print(f"Folder: {folder} ({len(files)} files)")
    # Sort files to find the potentially most relevant (usually shorter names or root)
    files.sort(key=lambda x: (len(os.path.basename(x)), x))
    for f in files[:5]:
        print(f"  {f}")
    if len(files) > 5:
        print(f"  ... ")
print("-" * 60)
