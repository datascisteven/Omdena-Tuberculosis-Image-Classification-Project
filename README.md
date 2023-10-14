# Omdena Project for Chest X-Ray Image Classification for Respiratory Disease and Disorders (Myanmar Chapter)

# About the Project

This is some of the code that I contributed to the Omdena Myanmar Project as the Tuberculosis team lead for their project to democratize access to resources for the following respiratory lung disorders: tuberculosis, lung cancer, pneumonia, and COVID.  

Four teams worked alongside each other in building models for each disease for 8 weeks, and within each team, we selected the best model for deployment.  We had a team member who was experienced in Streamlit that developed a webapp for the model.

# Data Collection

In deciding to build a binary classification model, we grouped healthy individuals with individuals infected with a disease other than Tuberculosis into a single category called non-Tuberculosis. 

We conducted a thorough search of various internet resources for Tuberculosis Chest X-Ray images, and we immediately noted the major class imbalance in the images for most datasets. Ultimately, we tried to collect as many Tuberculosis images from various datasets as possible and complemented the datasets with an equal amount of healthy and sick with non-TB CXR images. There were more images avaialble through TBPortals, but we would have to apply for access to the dataset, which includes the Belarus dataset, but that was freely available on Kaggle.

Ultimately, we compiled our Tuberculosis and non-Tuberculosis images from the following sources:

Non-Tuberculosis:
- 3800 CXR images from healthy individuals: 
  - [TBX11K Nankai University](https://drive.google.com/file/d/1r-oNYTPiPCOUzSjChjCIYTdkjBTugqxR/view)
- 3800 CXR images from infected non-TB individuals: 
  - [TBX11K Nankai University](https://drive.google.com/file/d/1r-oNYTPiPCOUzSjChjCIYTdkjBTugqxR/view)


Tuberculosis:
- 1048 CXR images from TB infected individuals: 
  - [Belarus (converted from DICOM)](https://www.kaggle.com/datasets/raddar/drug-resistant-tuberculosis-xrays)
- 394 CXR images from the original NLM Datasets: 
  - [NLM-Montgomery](https://data.lhncbc.nlm.nih.gov/public/Tuberculosis-Chest-X-ray-Datasets/Montgomery-County-CXR-Set/MontgomerySet/index.html)
  - [NLM-Shenzhen](https://data.lhncbc.nlm.nih.gov/public/Tuberculosis-Chest-X-ray-Datasets/Shenzhen-Hospital-CXR-Set/index.html)
- 800 CXR images from the TBX11K Dataset: 
  - [TBX11K Dataset](https://www.kaggle.com/datasets/usmanshams/tbx-11)
- 45 and 52 TB CXR images from DA and DB Datasets:
  - [TBXPredict DA](https://sourceforge.net/projects/tbxpredict/files/data/)
  - [TBXPredict DB (Converted from DICOM)](https://sourceforge.net/projects/tbxpredict/files/data/)
   

## Folder Structure:

	├── README.md
    │
	├── _data
	│   ├── augmented_sorted		<- CXR images sorted by train/val/test including augmentations
	│   ├── MTG_ClinicalReadings	<- clinical readings in NLH Dataset for EDA
	│   └── SHZ_ClinicalReadings
    │
    ├── _flask_app				    <- (soon) Flask application for deployment
    │
    ├── _images
    │
    ├── _logs
	│   └── _DenseNet	            <- Tensorflow callback data for the final model
    │       ├── _checkpoints
    │       └── _tb_log
    │ 
	├── _reference 
    │    
    └── Final_Notebook.ipynb


## Contact Information:

**Steven Yan**

<img src="images/mail_icon.png"> **Email:**  [stevenyan@uchicago.edu][1]

<img src="images/linkedin_icon.png"> **LinkedIn:**   [https://www.linkedin.com/in/datascisteven][2]

<img src="images/github_icon.png"> **Github:** [https://www.github.com/datascisteven][3]


## References:

International Skin Imaging Collaboration. SIIM-ISIC 2020 Challenge Dataset. International Skin Imaging Collaboration [https://doi.org/10.34970/2020-ds01][4] (2020).

Rotemberg, V. _et al_. A patient-centric dataset of images and metadata for identifying melanomas using clinical context. _Sci. Data_ 8: 34 (2021). [https://doi.org/10.1038/s41597-021-00815-z][5]

ISIC 2019 data is provided courtesy of the following sources:

- BCN20000 Dataset: (c) Department of Dermatology, Hospital Clínic de Barcelona
- HAM10000 Dataset: (c) by ViDIR Group, Department of Dermatology, Medical University of Vienna; [https://doi.org/10.1038/sdata.2018.161][6]
- MSK Dataset: (c) Anonymous; [https://arxiv.org/abs/1710.05006][7] ; [https://arxiv.org/abs/1902.03368][8]

Tschandl, P. _et al_. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. _Sci. Data_ 5: 180161 doi: 10.1038/sdata.2018.161 (2018)

Codella, N. _et al_. “Skin Lesion Analysis Toward Melanoma Detection: A Challenge at the 2017 International Symposium on Biomedical Imaging (ISBI), Hosted by the International Skin Imaging Collaboration (ISIC)”, 2017; arXiv:1710.05006.

Marc Combalia, Noel C. F. Codella, Veronica Rotemberg, Brian Helba, Veronica Vilaplana, Ofer Reiter, Allan C. Halpern, Susana Puig, Josep Malvehy: “BCN20000: Dermoscopic Lesions in the Wild”, 2019; arXiv:1908.02288.

Codella, N. _et al_. “Skin Lesion Analysis Toward Melanoma Detection 2018: A Challenge Hosted by the International Skin Imaging Collaboration (ISIC)”, 2018; [https://arxiv.org/abs/1902.03368][9]


[1]:	mailto:stevenyan@uchicago.edu
[2]:	https://www.linkedin.com/in/datascisteven
[3]:	https://www.github.com/datascisteven
[4]:	https://doi.org/10.34970/2020-ds01
[5]:    https://doi.org/10.1038/s41597-021-00815-z
[6]:	https://doi.org/10.1038/sdata.2018.161
[7]:	https://arxiv.org/abs/1710.05006
[8]:	https://arxiv.org/abs/1902.03368
[9]:	https://arxiv.org/abs/1902.03368
