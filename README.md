# Radiomics Feature Extractor

## Overview
This tool performs radiomic feature extraction from medical images in both 2D and 3D formats, such as `.nii`, `.png`, and `.jpeg`. It generates CSV files containing various radiomic features based on selected categories: shape, first-order, wavelet, and texture features.

<p align="center">
  <img src="img/UI.png" alt="Alt text">
</p>

## Features
- Supports both 3D medical images (NIfTI format) and 2D image formats (PNG, JPEG).
- Handles multiple label masks as well as binary masks.
- Outputs feature data as CSV files.
- Intuitive UI with buttons to select the type of features for extraction.
- Important Note: Ensure that the image and mask filenames are identical, with '_mask' added to the mask file's name. For example, if the image file is 'Imagename.png' or 'Imagename.nii,' the corresponding mask file should be 'Imagename_mask.png' or 'Imagename_mask.nii.

## Usage Instructions
1. **Download the repository**:
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/aambekar-brown/Radiomics-Feature-Extractor.git
   cd Radiomics-Feature-Extractor
   ```
2. **Install Virtual Environment and all dependencies on your local machine**:

   **Using `conda`**
   - Instructions to install conda: https://docs.anaconda.com/miniconda/miniconda-install/

   - On **Windows/macOS/Linux**:
     ```bash
     conda create --name fe_env python=3.7
     conda activate fe_env
     conda install -c simpleitk SimpleITK
     pip install -r requirements.txt
     ```

   **Note for macOS and Linux users**: If tkinter is not installed on your system, you can install it as follows:
   
   - On macOS (if using Homebrew):
     ```bash
     brew install python-tk
     ```
   
   - On Linux (Debian/Ubuntu-based distros):
     ```bash
     sudo apt-get install python3-tk
     ```

4. **Run Feature Extractor**:
   ```bash
   cd code
   Feature_Extractor.bat
   ```

## References
[1] B. H. Menze, A. Jakab, S. Bauer, J. Kalpathy-Cramer, K. Farahani, J. Kirby, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)", IEEE Transactions on Medical Imaging 34(10), 1993-2024 (2015) DOI: 10.1109/TMI.2014.2377694

[2] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J.S. Kirby, et al., "Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features", Nature Scientific Data, 4:170117 (2017) DOI: 10.1038/sdata.2017.117

[3] S. Bakas, M. Reyes, A. Jakab, S. Bauer, M. Rempfler, A. Crimi, et al., "Identifying the Best Machine Learning Algorithms for Brain Tumor Segmentation, Progression Assessment, and Overall Survival Prediction in the BRATS Challenge", arXiv preprint arXiv:1811.02629 (2018)

[4] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J. Kirby, et al., "Segmentation Labels and Radiomic Features for the Pre-operative Scans of the TCGA-GBM collection", The Cancer Imaging Archive, 2017. DOI: 10.7937/K9/TCIA.2017.KLXWJJ1Q

[5] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J. Kirby, et al., "Segmentation Labels and Radiomic Features for the Pre-operative Scans of the TCGA-LGG collection", The Cancer Imaging Archive, 2017. DOI: 10.7937/K9/TCIA.2017.GJQ7R0EF

[6] van Griethuysen, J. J. M., Fedorov, A., Parmar, C., Hosny, A., Aucoin, N., Narayan, V., Beets-Tan, R. G. H., Fillon-Robin, J. C., Pieper, S., Aerts, H. J. W. L. (2017). Computational Radiomics System to Decode the Radiographic Phenotype. Cancer Research, 77(21), e104–e107. `https://doi.org/10.1158/0008-5472.CAN-17-0339 <https://doi.org/10.1158/0008-5472.CAN-17-0339>`_
