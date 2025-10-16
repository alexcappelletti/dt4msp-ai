import os
from PIL import Image
import pillow_heif





# Registra il decoder HEIC
pillow_heif.register_heif_opener()
# Directory di input e output
input_dir = "/app/images"
output_dir = "/app/images/converted" 
os.makedirs(output_dir, exist_ok=True)
heic_files = sorted([
	f for f in os.listdir(input_dir)
	if f.lower().endswith(".heic")
])[:10]
for filename in heic_files:
	input_path = os.path.join(input_dir, filename)
	output_path = os.path.join(output_dir, filename.lower().replace(".heic", ".jpeg"))
	try:
		img = Image.open(input_path)

		img.save(output_path, format="JPEG")
		print(f"✅ Converted: {filename} → {output_path}")
	except Exception as e:
		print(f"❌ Failed: {filename} → {e}")
