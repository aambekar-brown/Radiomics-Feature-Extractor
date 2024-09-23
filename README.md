# Radiomics Feature Extractor

## Overview
This tool performs radiomic feature extraction from medical images in both 2D and 3D formats, such as `.nii`, `.png`, and `.jpeg`. It generates CSV files containing various radiomic features based on selected categories: shape, first-order, wavelet, and texture features.

## Features
- Supports both 3D medical images (NIfTI format) and 2D image formats (PNG, JPEG).
- Handles multiple label masks as well as binary masks.
- Outputs feature data as CSV files.
- Intuitive UI with buttons to select the type of features for extraction.

## Usage Instructions
1. **Download the repository**:
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/aambekar-brown/Radiomics-Feature-Extractor.git
   cd Radiomics-Feature-Extractor
   ```
2. **Install Virtual Enviornment on your local machine**:
  ```bash
  python -m venv venv3_7
  call activate venv3_7
  pip install -r requirements.txt
  ```
3. **Run Feature Extractor**:
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
