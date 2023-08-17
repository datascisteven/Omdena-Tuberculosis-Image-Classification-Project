"""
This main would predict covid
"""
# %% Import
###############
##### LIB #####
###############
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
import sys

import random
from sklearn.model_selection import train_test_split

#######################
##### LOCAL LIB #######
#######################
## USER DEFINED:
ABS_PATH = "/home/jx/JX_Project/covid-xray-detection" # Define ur absolute path here
DATA_DIRECTORY = "data-latest"

## Custom Files:
def abspath(relative_path):
    return os.path.join(ABS_PATH, relative_path)

def abs_data_path(relative_path):
    return os.path.join(os.path.join(ABS_PATH, DATA_DIRECTORY), relative_path)

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(abspath("src_code"))

import jx_lib


# %% LOAD DATASET INFO: ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#######################
##### LOAD DATASET ####
#######################
LUT_HEADER = ["[patient id]", "[filename]", "[class]", "[data source]"]
# import data
TRAIN_DATA_LUT = pd.read_csv(abs_data_path("train.txt"), sep=" ", header=None, names=LUT_HEADER)
VALID_DATA_LUT = pd.read_csv(abs_data_path("test.txt"), sep=" ", header=None, names=LUT_HEADER)
# convert class to label 'y'
LABEL_TO_INT_LUT = {
    "positive": 1,
    "negative": 0,
}
INT_TO_LABEL_LUT = {
    1: "positive",
    0: "negative",
}
def class_to_binary(cls):
    return [LABEL_TO_INT_LUT[c] for c in cls]
TRAIN_DATA_LUT["Y"] = class_to_binary(TRAIN_DATA_LUT["[class]"])
VALID_DATA_LUT["Y"] = class_to_binary(VALID_DATA_LUT["[class]"])
# convert filename to absolute path:
def filename_to_abspath(filenames, tag):
    return [abs_data_path("{}/{}".format(tag, filename)) for filename in filenames]
TRAIN_DATA_LUT["img_abs_path"] = filename_to_abspath(filenames=TRAIN_DATA_LUT["[filename]"], tag="train")
VALID_DATA_LUT["img_abs_path"] = filename_to_abspath(filenames=VALID_DATA_LUT["[filename]"], tag="test")

# report status:
def report_status(data, tag):
    tp, tn = np.sum(data["Y"] == 1), np.sum(data["Y"] == 0)
    print("{}: +:{}, -:{}".format(tag, tp, tn))

report_status(data=TRAIN_DATA_LUT, tag="train")
report_status(data=VALID_DATA_LUT, tag="valid")

# %% USER DEFINE ----- ----- ----- ----- ----- -----
#######################
##### PREFERENCE ######
#######################
FEATURE_CONVERT_ALL_DATA_PRE_PROCESS = True # (Validation/Test) Only with differential augmentation for  RGB channels
FEATURE_DATA_PRE_PROCESS_V2 = True # (Training) Additional dataset with rotation and zoom augmentation, with differential augmentation for  RGB channels
TRAIN_NEW_IMG_SIZE = (320,320)
TEST_NEW_IMG_SIZE = TRAIN_NEW_IMG_SIZE # None for original size
FEATURE_POST_HOMOGRAPHY = True # for round two, fixes
FEATURE_AUGMENTATION = False 
TRAIN_TEST_SPLIT = 0.8 # None

# %% image conversion function: ----- ----- ----- ----- ----- -----
######################
##### FUNCTIONS ######
######################
import cv2
def img_batch_conversion(PATH_LUT, OUT_DIR, RANDOM_AUGMENTATION=False, size=None, POST_HOMOGRAPHY=False):
    jx_lib.create_folder(DIR=OUT_DIR)
    new_path_list = []
    counter = 0
    for img_path, file_name in zip(PATH_LUT["img_abs_path"], PATH_LUT["[filename]"]):
        counter += 1
        print("\r   >[{}/{}]".format(counter,len(PATH_LUT["img_abs_path"])),  end='')
        out_path = "{}/{}".format(OUT_DIR, file_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        if RANDOM_AUGMENTATION:
            out_path = "{}/aug_{}".format(OUT_DIR, file_name)

            # define operator:
            def random_rotation(img, angle):
                angle = int(random.uniform(-angle, angle))
                h, w = img.shape[:2]
                M = cv2.getRotationMatrix2D((int(w/2), int(h/2)), angle, 1)
                img = cv2.warpAffine(img, M, (w, h))
                return img
            def fill(img, h, w):
                img = cv2.resize(img, (h, w), cv2.INTER_CUBIC)
                return img
            def random_zoom_crop(img, value):
                if value > 1 or value < 0:
                    print('Value for zoom should be less than 1 and greater than 0')
                    return img
                value = random.uniform(value, 1)
                h, w = img.shape[:2]
                h_taken = int(value*h)
                w_taken = int(value*w)
                h_start = random.randint(0, h-h_taken)
                w_start = random.randint(0, w-w_taken)
                img = img[h_start:h_start+h_taken, w_start:w_start+w_taken, :]
                img = fill(img, h, w)
                return img
            
            img = random_rotation(img, 90)
            img = random_zoom_crop(img, 0.8)

            
        # basic morphological operator
        kernel = np.ones((5, 5), 'uint8')
        if not POST_HOMOGRAPHY:
            img1 = cv2.dilate(img, kernel, iterations=5)
            img2 = cv2.erode(img, kernel, iterations=5)
            img_new = np.dstack((img[:,:,0], img1[:,:,1], img2[:,:,2]))
        else:
            img_new = np.dstack((img[:,:,0], img[:,:,1], img[:,:,2]))

        if size is not None:
            # fit:
            w, h, c= img_new.shape
            if w <= h:
                nw = size[0]
                nh = int(size[0]/w * h)
            else:
                nh = size[0]
                nw = int(size[0] / h * w)
            img_new  = cv2.resize(img_new, (nw, nh))
            # center crop:
            w, h, c= img_new.shape
            a = int((w-size[0])/2)
            b = int((h-size[1])/2)
            img_new = img_new[a:a+size[0], b:b+size[1]]
        
        if POST_HOMOGRAPHY:
            img1 = cv2.dilate(img_new, kernel, iterations=1)
            img2 = cv2.erode(img_new, kernel, iterations=1)
            img_new = np.dstack((img_new[:,:,0], img1[:,:,1], img2[:,:,2]))
        # plt.imshow(img_new)
        # fig, axes = plt.subplots(figsize=(20, 10), ncols=3)
        # axes[0].imshow(img)
        # axes[1].imshow(img1)
        # axes[2].imshow(img2)
            
        # print(out_path)
        cv2.imwrite(out_path, img_new)
        # break
        new_path_list.append(out_path)
    
    return new_path_list

def output_text_file(OUT_DIR, tag, dataframe, augment=False):
    OUT_FILE_PATH = "{}/pre-processed-[{}].txt".format(OUT_DIR, tag)
    with open(OUT_FILE_PATH, "w") as file_out:
        # original:
        file_out.write("\n".join([" ".join(["{}".format(dataframe[lut][i]) for lut in LUT_HEADER]) for i in dataframe.index]))
        if augment:
            # augmented:
            file_out.write("\n".join([" ".join(["{}".format(
                dataframe[lut][i]) if lut != "[filename]" else "aug_{}".format(
                    dataframe[lut][i])  for lut in LUT_HEADER]) for i in dataframe.index]))
    print("\n >>> Descriptive file output @{}".format(OUT_FILE_PATH))

#%% MAIN
def main():
    # %% V1 conversion
    #######################
    ##### RGB DIFF ONLY ###
    #######################
    if FEATURE_CONVERT_ALL_DATA_PRE_PROCESS:
        N_TEST = 400
        PATH_LUT_COMP = {
            "[filename]": [ "{}.png".format(i+1) for i in range(N_TEST) ],
            "img_abs_path": [ abs_data_path("competition_test/{}.png".format(i+1)) for i in range(N_TEST) ],
        }
        OUT_DIR = abs_data_path("competition_test-custom")
        if FEATURE_POST_HOMOGRAPHY:
            OUT_DIR = abs_data_path("competition_test-custom-post")
        img_batch_conversion(PATH_LUT=PATH_LUT_COMP, OUT_DIR=OUT_DIR, size=TEST_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)

        # OUT_DIR = abs_data_path("train-custom")
        # img_batch_conversion(PATH_LUT=TRAIN_DATA_LUT, OUT_DIR=OUT_DIR)

        OUT_DIR = abs_data_path("valid-custom")
        if FEATURE_POST_HOMOGRAPHY:
            OUT_DIR = abs_data_path("valid-custom-post")
        img_batch_conversion(PATH_LUT=VALID_DATA_LUT, OUT_DIR=OUT_DIR, size=TEST_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)

    # %% V2 Conversion
    ################################################
    ##### RGB DIFF +  Rot  & Zoom Augmentation #####
    ################################################
    if FEATURE_DATA_PRE_PROCESS_V2:
        def dataframe_split(dataframe, tag):
            print("\n### {:10s} data source ========".format(tag))
            # split based on unique data source
            PD_DICT = {}
            N_pos, N_neg = 0, 0
            for source_name in TRAIN_DATA_LUT["[data source]"].unique():
                dataframe_ = dataframe[dataframe["[data source]"] == source_name]

                PD_DICT[source_name] = {
                    "+": dataframe_[dataframe_["Y"] == 1],
                    "-": dataframe_[dataframe_["Y"] == 0]
                }
                n_pos, n_neg = len(PD_DICT[source_name]["+"]), len(PD_DICT[source_name]["-"])
                print("> [{:10s}]: +:{:6d} | -:{:6d}".format(source_name, n_pos, n_neg))
                N_pos += n_pos
                N_neg += n_neg
            
            print("> [{:10s}]: +:{:6d} | -:{:6d}".format("Total", N_pos, N_neg))
            print("=================================== \n")

            return PD_DICT

        PD_DICT_TRAIN = dataframe_split(dataframe=TRAIN_DATA_LUT, tag="Training")
        PD_DICT_VALID = dataframe_split(dataframe=VALID_DATA_LUT, tag="Validation")

        # %% BALANCING: ----- ----- ----- ----- ----- -----
        """
        ### Training   data source ========
        > [cohen     ]: +:   270 | -:   297
        > [actmed    ]: +:    25 | -:   107
        > [fig1      ]: +:    24 | -:     0
        > [sirm      ]: +:   943 | -:     0
        > [ricord    ]: +:   896 | -:     0
        > [rsna      ]: +:     0 | -: 13389
        > [Total     ]: +:  2158 | -: 13793
        =================================== 
        ### Validation data source ========
        > [cohen     ]: +:     0 | -:     0
        > [actmed    ]: +:     0 | -:     0
        > [fig1      ]: +:     0 | -:     0
        > [sirm      ]: +:     0 | -:     0
        > [ricord    ]: +:   200 | -:     0
        > [rsna      ]: +:     0 | -:   200
        > [Total     ]: +:   200 | -:   200
        ===================================


        Hence, we can balance the dataset by:
        1. take all positive data                                                   (+: 2158 | -: 0)
        2. take negative data with cohen and actmed, and sample (2158-297-107) >>   (+: 2158 | -: 2158)
        3. augment dataset                                                          (+: 4316 | -: 4316)

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        >>> Latest (Nov, 2021) 
        ### Training   data source ========
        > [cohen     ]: +:   270 | -:   297
        > [actmed    ]: +:    25 | -:   107
        > [fig1      ]: +:    24 | -:     0
        > [sirm      ]: +:   943 | -:     0
        > [ricord    ]: +:   896 | -:     0
        > [rsna      ]: +:     0 | -: 13389
        > [stonybrook]: +: 14132 | -:     0
        > [bimcv     ]: +:   200 | -:     0
        > [rnsa      ]: +:     0 | -:   199
        > [Total     ]: +: 16490 | -: 13992
        ===================================

        # 10k vs 10k for training ...
        # 3.9k for testing?

        ### Validation data source ========
        > [cohen     ]: +:     0 | -:     0
        > [actmed    ]: +:     0 | -:     0
        > [fig1      ]: +:     0 | -:     0
        > [sirm      ]: +:     0 | -:     0
        > [ricord    ]: +:   200 | -:     0
        > [rsna      ]: +:     0 | -:   200
        > [stonybrook]: +:     0 | -:     0
        > [bimcv     ]: +:     0 | -:     0
        > [rnsa      ]: +:     0 | -:     0
        > [Total     ]: +:   200 | -:   200
        ===================================


        """
        # downsample:
        PD_DICT_TRAIN_NEW = {}
        # PD_DICT_TRAIN_NEW["+"] = pd.concat([ PD_DICT_TRAIN[source_name]["+"] for source_name in ["cohen", "actmed", "fig1", "sirm", "ricord"]])
        # PD_DICT_TRAIN_NEW["-"] = pd.concat([ PD_DICT_TRAIN[source_name]["-"] for source_name in ["cohen", "actmed"]])
        NEW_TABLE = ["cohen","actmed","fig1","sirm","ricord","rsna","bimcv","rnsa"]
        PD_DICT_TRAIN_NEW["+"] = pd.concat([ PD_DICT_TRAIN[source_name]["+"] for source_name in NEW_TABLE])
        PD_DICT_TRAIN_NEW["-"] = pd.concat([ PD_DICT_TRAIN[source_name]["-"] for source_name in NEW_TABLE])

        # - manually balance:
        N_DOWNSAMPLE = len(PD_DICT_TRAIN_NEW["-"]) - len(PD_DICT_TRAIN_NEW["+"])
        if N_DOWNSAMPLE > 0:
            PD_PD_DICT_TRAIN_RSNA_DOWN_SAMPLE = PD_DICT_TRAIN["stonybrook"]["+"].sample(n=N_DOWNSAMPLE, random_state=1)
            PD_DICT_TRAIN_NEW["+"] = pd.concat([PD_DICT_TRAIN_NEW["+"], PD_PD_DICT_TRAIN_RSNA_DOWN_SAMPLE])

        print((">> New Training Dataset >> -:{:6d} | +:{:6d} with {:4d} from stonybrook").format(
            len(PD_DICT_TRAIN_NEW["-"]), len(PD_DICT_TRAIN_NEW["+"]), N_DOWNSAMPLE
        ))

        PD_DICT_TRAIN_NEW_EVAL = {}
        if TRAIN_TEST_SPLIT is not None:
            #- shuffle:
            positive_entries = PD_DICT_TRAIN_NEW["+"].copy()
            negative_entries = PD_DICT_TRAIN_NEW["-"].copy()
            #- split:
            N_total = len(PD_DICT_TRAIN_NEW["+"])
            N_mid = TRAIN_TEST_SPLIT * N_total
            PD_DICT_TRAIN_NEW_EVAL["+"], PD_DICT_TRAIN_NEW["+"] = train_test_split(PD_DICT_TRAIN_NEW["+"], test_size=TRAIN_TEST_SPLIT)
            PD_DICT_TRAIN_NEW_EVAL["-"], PD_DICT_TRAIN_NEW["-"] = train_test_split(PD_DICT_TRAIN_NEW["-"], test_size=TRAIN_TEST_SPLIT)
            print((">> New Evaluation Dataset After Split >> -:{:6d} | +:{:6d} ").format(
                len(PD_DICT_TRAIN_NEW_EVAL["-"]), len(PD_DICT_TRAIN_NEW_EVAL["+"]), N_DOWNSAMPLE
            ))
            
            print((">> New Training Dataset After Split >> -:{:6d} | +:{:6d} ").format(
                len(PD_DICT_TRAIN_NEW["-"]), len(PD_DICT_TRAIN_NEW["+"]), N_DOWNSAMPLE
            ))
            OUT_DIR = abs_data_path("eval-custom")
            if FEATURE_POST_HOMOGRAPHY:
                OUT_DIR = abs_data_path("eval-custom-post")
            print("\n> Generate +ve evaluation dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW_EVAL["+"], OUT_DIR, RANDOM_AUGMENTATION=False, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)
            print("\n> Generate -ve evaluation  dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW_EVAL["-"], OUT_DIR, RANDOM_AUGMENTATION=False, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)

            EVAL_COMBINED = pd.concat([PD_DICT_TRAIN_NEW_EVAL["+"], PD_DICT_TRAIN_NEW_EVAL["-"]])
            EVAL_COMBINED = EVAL_COMBINED.sample(frac=1).reset_index(drop=True)
            output_text_file(OUT_DIR=abs_data_path(""), tag="eval", dataframe=EVAL_COMBINED)

        # %% UP-SAMPLING: ----- ----- ----- ----- ----- -----
        # generate pre-processed images + upsampling images by augmentation:
        if FEATURE_AUGMENTATION:
            OUT_DIR = abs_data_path("train-custom-with-aug")
            if FEATURE_POST_HOMOGRAPHY:
                OUT_DIR = abs_data_path("train-custom-with-aug-post")
        else:
            OUT_DIR = abs_data_path("train-custom")
            if FEATURE_POST_HOMOGRAPHY:
                OUT_DIR = abs_data_path("train-custom-post")
        
        if FEATURE_AUGMENTATION:
            # pre-process with augmentation + morpho logic operators
            print("> Augmenting +ve dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW["+"], OUT_DIR, RANDOM_AUGMENTATION=True, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)
            print("> Augmenting -ve dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW["-"], OUT_DIR, RANDOM_AUGMENTATION=True, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)
        else:
            # pre-process with morpho logic operators
            print("> Generate +ve dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW["+"], OUT_DIR, RANDOM_AUGMENTATION=False, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)
            print("> Generate -ve dataset:")
            img_batch_conversion(PD_DICT_TRAIN_NEW["-"], OUT_DIR, RANDOM_AUGMENTATION=False, size=TRAIN_NEW_IMG_SIZE, POST_HOMOGRAPHY=FEATURE_POST_HOMOGRAPHY)
            
        print("==> AUTO_GEN completed!")

        # %% output descriptive file
        NEW_TRAINING_DATA_AUGMENTED = pd.concat([PD_DICT_TRAIN_NEW["+"], PD_DICT_TRAIN_NEW["-"]])
        # NEW_TRAINING_DATA_AUGMENTED = NEW_TRAINING_DATA_AUGMENTED.sample(frac=1).reset_index(drop=True)
        output_text_file(OUT_DIR=abs_data_path(""), tag="train", dataframe=NEW_TRAINING_DATA_AUGMENTED)

if __name__ == "__main__":
    main()

# %%
