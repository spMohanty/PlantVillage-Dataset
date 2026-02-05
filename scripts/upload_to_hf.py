
import os
import zipfile
import glob
from huggingface_hub import HfApi, create_repo

# Configuration
REPO_ID = "mohanty/PlantVillage"
RAW_DATA_DIR = "raw"
ZIP_FILENAME = "data.zip"
BUILDER_SCRIPT = "plant_village.py"
LEAF_MAP = "leaf_grouping/leaf-map.json"
SPLITS_DIR = "split_files"
HF_README = "README_HF.md"

def create_data_zip():
    if os.path.exists(ZIP_FILENAME):
        print(f"[{ZIP_FILENAME}] already exists. Skipping zip generation.")
        return

    print(f"Zipping [{RAW_DATA_DIR}] into [{ZIP_FILENAME}]...")
    # Compressing the 'raw' directory. 
    # The structure inside zip should be 'raw/color/...', 'raw/grayscale/...' 
    # to match logic in builder script if it expects 'data_dir' to contain 'raw' or be root?
    # plant_village.py logic: data_dir = dl_manager.download_and_extract(data_url)
    # inside data_dir, it looks for "color", "grayscale" etc.
    # So if we zip 'raw/color', extracting it might give 'raw/color' or just 'color' depending on how we zip.
    
    # Let's verify what `zip -r data.zip raw` does. It usually includes 'raw' as top folder.
    # If plant_village.py does `os.path.join(data_dir, "color")`, it implies `data_dir` HAS "color" inside it.
    # If `data.zip` contains `raw/color`, extraction gives `.../raw/color`.
    # Then `data_dir` would be `...`. `os.path.join(..., "color")` would look for `.../color`.
    # So if zip has `raw/color`, we need to handle that.
    
    # In my builder script:
    # `data_dir = dl_manager.download_and_extract(data_url)`
    # `if os.path.exists(os.path.join(base_dir, "color")): ...`
    
    # If I zip `raw/*` INTO root of zip, then extracting it gives `color`, `grayscale` at root of extracted dir.
    # That matches `os.path.join(data_dir, "color")`.
    
    with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RAW_DATA_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                # We want the path inside zip to START after RAW_DATA_DIR
                # e.g. raw/color/Apple/1.jpg -> color/Apple/1.jpg
                arcname = os.path.relpath(file_path, RAW_DATA_DIR)
                zipf.write(file_path, arcname)
    
    print("Zip creation complete.")

def upload_files():
    api = HfApi()
    
    # 1. Create Repo if not exists
    print(f"Creating/Verifying repo [{REPO_ID}]...")
    try:
        create_repo(REPO_ID, repo_type="dataset", exist_ok=True)
    except Exception as e:
        print(f"Note: {e}")

    # 2. Upload data.zip
    print(f"Uploading [{ZIP_FILENAME}]...")
    api.upload_file(
        path_or_fileobj=ZIP_FILENAME,
        path_in_repo="data.zip",
        repo_id=REPO_ID,
        repo_type="dataset"
    )

    # 3. Upload builder script
    print(f"Uploading [{BUILDER_SCRIPT}]...")
    api.upload_file(
        path_or_fileobj=BUILDER_SCRIPT,
        path_in_repo="plant_village.py",
        repo_id=REPO_ID,
        repo_type="dataset"
    )

    # 4. Upload leaf map
    print(f"Uploading [{LEAF_MAP}]...")
    api.upload_file(
        path_or_fileobj=LEAF_MAP,
        path_in_repo="leaf_grouping/leaf-map.json",
        repo_id=REPO_ID,
        repo_type="dataset"
    )

    # 5. Upload Splits
    print("Uploading split files...")
    split_files = glob.glob(os.path.join(SPLITS_DIR, "*.txt"))
    for file_path in split_files:
        filename = os.path.basename(file_path)
        print(f"  Uploading {filename}...")
        api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=f"splits/{filename}",
            repo_id=REPO_ID,
            repo_type="dataset"
        )
        
    # 6. Upload README
    if os.path.exists(HF_README):
        print(f"Uploading [{HF_README}] as README.md...")
        api.upload_file(
            path_or_fileobj=HF_README,
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="dataset"
        )
    else:
        print(f"Warning: {HF_README} not found. Skipping README update.")

    print("All uploads complete!")

def main():
    # Ensure we are in the root of the repo (where raw/ exists)
    if not os.path.exists(RAW_DATA_DIR):
        print(f"Error: '{RAW_DATA_DIR}' directory not found. Please run this script from the repository root.")
        return

    create_data_zip()
    upload_files()
    
    # Cleanup
    if os.path.exists(ZIP_FILENAME):
        print(f"Cleaning up {ZIP_FILENAME}...")
        os.remove(ZIP_FILENAME)

if __name__ == "__main__":
    main()
