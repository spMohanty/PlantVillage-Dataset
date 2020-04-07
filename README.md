# PlantVillage-Dataset

## Download dataset

With [git](https://git-scm.com/downloads) installed, you can download the dataset by : 
```
git clone https://github.com/spMohanty/PlantVillage-Dataset
cd PlantVillage-Dataset
```

Or you can download specific folders through [svn](https://subversion.apache.org/) by replacing `<folderYouWant>` with the appropriate path:
```
svn checkout https://github.com/spMohanty/PlantVillage-Dataset/trunk/<folderYouWant>
```
For example, if you want to download the folder `raw/color/Grape___Esca_(Black_Measles)`, do it like so:
```
svn checkout https://github.com/spMohanty/PlantVillage-Dataset/trunk/raw/color/Grape___Esca_\(Black_Measles)
```



The different versions of the dataset are present in the `raw` directory : 
* `color` : Original RGB images
* `grayscale` : grayscaled version of the raw images
* `segmented` : RGB images with just the leaf segmented and color corrected.

TO-DO : Add Usage Documentation. In case of any confusion while trying to use this code now, please shoot an email to `sharada.mohanty@epfl.ch`
