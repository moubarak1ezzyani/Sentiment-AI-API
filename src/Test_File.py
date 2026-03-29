import importlib

modules = ["os", "requests", "jwt", "dotenv", "fastapi", "pydantic"]

for m in modules:
    try:
        importlib.import_module(m)
        print(f"{m} ✅ trouvé")
    except ImportError:
        print(f"{m} ❌ manquant")
        