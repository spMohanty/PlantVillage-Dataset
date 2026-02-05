
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PlantVillage Dataset"""


import json
import os
import datasets


_CITATION = """\
@article{Mohanty_Hughes_Salathé_2016,
title={Using deep learning for image-based plant disease detection},
volume={7},
DOI={10.3389/fpls.2016.01419},
journal={Frontiers in Plant Science},
author={Mohanty, Sharada P. and Hughes, David P. and Salathé, Marcel},
year={2016},
month={Sep}} 
"""

_DESCRIPTION = """\
The PlantVillage Dataset is an open access repository of 54,306 images of healthy and diseased plant leaves, collected to advance research in automated plant disease diagnosis. It covers 14 crop species and 26 diseases.
"""

_HOMEPAGE = "https://github.com/spMohanty/PlantVillage-Dataset"

_LICENSE = "CC BY-SA 3.0"  # Assuming generic open license, verify if possible

_CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

class PlantVillage(datasets.GeneratorBasedBuilder):
    """PlantVillage Dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "image_path": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=_CLASS_NAMES),
                    "crop": datasets.Value("string"),
                    "disease": datasets.Value("string"),
                    "leaf_id": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        
        # Define URLs
        # We use the repo URL. Assumes files are at root or in splits/ folder.
        repo_url = "https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main"
        data_url = f"{repo_url}/data.zip"
        leaf_map_url = f"{repo_url}/leaf_grouping/leaf-map.json"
        
        # Download and extract data
        data_dir = dl_manager.download_and_extract(data_url)
        leaf_map_path = dl_manager.download(leaf_map_url)

        splits = []
        name = self.config.name # 'color', 'grayscale', 'segmented' or 'default' (which we assume is color)
        
        if name == "default":
             name = "color"
             
        # Download split files for this config
        train_split_url = f"{repo_url}/splits/{name}_train.txt"
        test_split_url = f"{repo_url}/splits/{name}_test.txt"
        
        train_split_path = dl_manager.download(train_split_url)
        test_split_path = dl_manager.download(test_split_url)
        
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": data_dir,
                    "split_file_path": train_split_path,
                    "leaf_map_path": leaf_map_path,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_dir": data_dir,
                    "split_file_path": test_split_path,
                    "leaf_map_path": leaf_map_path,
                },
            ),
        ]

    def _generate_examples(self, data_dir, split_file_path, leaf_map_path):
        """Yields examples."""
        
        leaf_map = {}
        if os.path.exists(leaf_map_path):
            with open(leaf_map_path, "r") as f:
                leaf_map = json.load(f)
        
        with open(split_file_path, "r") as f:
            file_list = [line.strip() for line in f if line.strip()]

        for idx, file_rel_path in enumerate(file_list):
            # file_rel_path is like "raw/color/Apple/1.jpg"
            # data_dir is the root of extracted zip. 
            # Note: zip extracts to a folder. If zip contains "raw/...", then data_dir/raw/... exists.
            
            file_path = os.path.join(data_dir, file_rel_path)
            
            # Extract metadata from path
            # Expected format: raw/<type>/<class>/<filename>
            parts = file_rel_path.split("/")
            if len(parts) < 4:
                continue
            
            # parts[0] = raw, parts[1] = data_type, parts[2] = class, parts[3] = filename
            class_name = parts[2]
            file_name = parts[3]

            # Extract crop and disease
            sub_parts = class_name.split("___")
            crop = sub_parts[0]
            disease = sub_parts[1] if len(sub_parts) > 1 else "unknown"

            # Logic to determine leaf_id
            image_identifier = file_name.replace("_final_masked", "")
            if "___" in image_identifier:
                image_identifier = image_identifier.split("___")[-1]
            
            image_identifier = image_identifier.split("copy")[0]
            image_identifier = image_identifier.replace(".jpg", "").replace(".JPG", "").replace(".png", "").replace(".PNG", "")
            image_identifier = image_identifier.strip()
            
            leaf_id = "unknown"
            lookup_key = image_identifier.lower().strip()
            
            if lookup_key in leaf_map:
                suggestions = leaf_map[lookup_key]
                if len(suggestions) == 1:
                    leaf_id = suggestions[0]
                else:
                    found = False
                    for suggestion in suggestions:
                       if class_name in suggestion:
                           leaf_id = suggestion
                           found = True
                           break
                    if not found:
                         leaf_id = f"fallback_{image_identifier}" 
            else:
                leaf_id = f"fallback_{image_identifier}"

            yield idx, {
                "image": file_path,
                "image_path": file_rel_path,
                "label": class_name,
                "crop": crop,
                "disease": disease,
                "leaf_id": leaf_id,
            }
