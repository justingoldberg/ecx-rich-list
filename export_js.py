import json

with open("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data/utxos.json") as f:
    data = json.load(f)

with open("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data/utxos.js", "w") as f:
    f.write("// eCash (ECX) Top 500 Largest UTXOs - Snapshot at Block 973,728\n")
    f.write("window.ECX_TOP_500_UTXOS = ")
    json.dump(data, f)
    f.write(";\n")

print("Created data/utxos.js successfully")
