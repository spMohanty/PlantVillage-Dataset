---
language:
- en
license: cc-by-sa-3.0
task_categories:
- image-classification
tags:
- agriculture
- plant-disease
- biology
dataset_info:
  features:
  - name: image
    dtype: image
  - name: image_path
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          '0': Apple___Apple_scab
          '1': Apple___Black_rot
          '2': Apple___Cedar_apple_rust
          '3': Apple___healthy
          '4': Blueberry___healthy
          '5': Cherry_(including_sour)___Powdery_mildew
          '6': Cherry_(including_sour)___healthy
          '7': Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot
          '8': Corn_(maize)___Common_rust_
          '9': Corn_(maize)___Northern_Leaf_Blight
          '10': Corn_(maize)___healthy
          '11': Grape___Black_rot
          '12': Grape___Esca_(Black_Measles)
          '13': Grape___Leaf_blight_(Isariopsis_Leaf_Spot)
          '14': Grape___healthy
          '15': Orange___Haunglongbing_(Citrus_greening)
          '16': Peach___Bacterial_spot
          '17': Peach___healthy
          '18': Pepper,_bell___Bacterial_spot
          '19': Pepper,_bell___healthy
          '20': Potato___Early_blight
          '21': Potato___Late_blight
          '22': Potato___healthy
          '23': Raspberry___healthy
          '24': Soybean___healthy
          '25': Squash___Powdery_mildew
          '26': Strawberry___Leaf_scorch
          '27': Strawberry___healthy
          '28': Tomato___Bacterial_spot
          '29': Tomato___Early_blight
          '30': Tomato___Late_blight
          '31': Tomato___Leaf_Mold
          '32': Tomato___Septoria_leaf_spot
          '33': Tomato___Spider_mites Two-spotted_spider_mite
          '34': Tomato___Target_Spot
          '35': Tomato___Tomato_Yellow_Leaf_Curl_Virus
          '36': Tomato___Tomato_mosaic_virus
          '37': Tomato___healthy
  - name: crop
    dtype: string
  - name: disease
    dtype: string
  - name: leaf_id
    dtype: string
  config_name: color
  splits:
  - name: train
    num_bytes: 43596
    num_examples: 43596
  - name: test
    num_bytes: 10709
    num_examples: 10709
  download_size: 2000000000
  dataset_size: 2000000000
---

# PlantVillage Dataset

[![Paper](https://img.shields.io/badge/Paper-Read-green)](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2016.01419/full)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/spMohanty/PlantVillage-Dataset)

<img src="https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/generated_for_paper/plantvillage.jpg" alt="PlantVillage Dataset Sample" width="600"/>

The **PlantVillage Dataset** is an open access repository of **54,306 images** of healthy and diseased plant leaves, collected to advance research in automated plant disease diagnosis. It covers **14 crop species** and **26 diseases**.

This dataset was introduced in the paper [**"Using Deep Learning for Image-Based Plant Disease Detection"**](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2016.01419/full) by Mohanty et al. (2016).

## Quick Start

The dataset comes with pre-defined **80/20 train/test splits** that preserve the leaf grouping logic (ensuring images of the same leaf do not appear in both sets).

```python
from datasets import load_dataset

# Load the default configuration (color images)
# This automatically downloads the train and test splits.
dataset = load_dataset("mohanty/PlantVillage", "color")

print(dataset)
# DatasetDict({
#     train: Dataset({ features: [...], num_rows: 43596 }),
#     test: Dataset({ features: [...], num_rows: 10709 })
# })
```

## Dataset Configurations

You can choose from three configurations depending on your needs:

| Configuration | Description | Usage |
|---|---|---|
| **`color`** | Original RGB images (Default) | `load_dataset("mohanty/PlantVillage", "color")` |
| **`grayscale`** | Grayscale versions | `load_dataset("mohanty/PlantVillage", "grayscale")` |
| **`segmented`** | Background removed, leaf segmented | `load_dataset("mohanty/PlantVillage", "segmented")` |

## Advanced: Custom Splitting

**Note:** The dataset **already includes** a standard train/test split (as shown in Quick Start), which is recommended for benchmarking. The instructions below are only for **advanced users** who require custom cross-validation folds.

If you require a different split ratio or cross-validation scheme, you **must** strictly respect the `leaf_id` to prevent data leakage. Multiple images often capture the same physical leaf; separating them across train/test sets will bias your evaluation.

Here is a complete example of how to reshuffle and split the dataset 80/20:

```python
import numpy as np
from datasets import load_dataset, concatenate_datasets

# 1. Load the full dataset (combining default train/test splits)
dataset = load_dataset("mohanty/PlantVillage", "color")
full_dataset = concatenate_datasets([dataset["train"], dataset["test"]])

# 2. Get unique leaf IDs representing physical leaves
all_leaf_ids = np.unique(full_dataset["leaf_id"])

# 3. Shuffle and Split Leaf IDs (e.g., 80% train, 20% test)
np.random.seed(42)
np.random.shuffle(all_leaf_ids)

split_ratio = 0.8
split_idx = int(len(all_leaf_ids) * split_ratio)

train_leaf_ids = set(all_leaf_ids[:split_idx])
test_leaf_ids = set(all_leaf_ids[split_idx:])

# 4. Filter the full dataset to create new splits
# This ensures all images of a specific leaf are exclusively in one split
custom_train = full_dataset.filter(lambda x: x["leaf_id"] in train_leaf_ids)
custom_test = full_dataset.filter(lambda x: x["leaf_id"] in test_leaf_ids)

print(f"Custom Train Size: {len(custom_train)}")
print(f"Custom Test Size: {len(custom_test)}")
```

## Dataset Features

- **`image`**: PIL Image.
- **`label`**: Class label (e.g., `Apple___Black_rot`).
- **`leaf_id`**: Unique identifier for the physical leaf. 
- **`crop`**: Crop name.
- **`disease`**: Disease name.

## Citation

```bibtex
@article{Mohanty_Hughes_Salathé_2016,
title={Using deep learning for image-based plant disease detection},
volume={7},
DOI={10.3389/fpls.2016.01419},
journal={Frontiers in Plant Science},
author={Mohanty, Sharada P. and Hughes, David P. and Salathé, Marcel},
year={2016},
month={Sep}} 
```

## Author

Sharada Mohanty <sharada.mohanty@epfl.ch>  
Marcel Salathé <Marcel.Salathe@epfl.ch>  
**Digital Epidemiology Lab, EPFL**
