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
    ├── _flask_app				<- (soon) Flask application for deployment
    │
    ├── _images
   	│
	├── _references 
    │    
    └── Final_Notebook.ipynb


## Contact Information:

**Steven Yan**

<img src="images/mail_icon.png"> **Email:**  [stevenyan@uchicago.edu][1]

<img src="images/linkedin_icon.png"> **LinkedIn:**   [https://www.linkedin.com/in/datascisteven][2]

<img src="images/github_icon.png"> **Github:** [https://www.github.com/datascisteven][3]


