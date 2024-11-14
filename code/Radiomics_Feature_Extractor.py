# Extract features from 3D nifti files as well as 2D PNG images (masks can include multiple labels)


import os
import SimpleITK as sitk
import numpy as np
import csv
from radiomics import featureextractor
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading


# Function to determine if a file is 2D (image) or 3D (NIfTI)
def is_2d_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension in ['.png', '.jpg', '.jpeg']

def load_png(file_path):
    image = sitk.ReadImage(file_path)
    return sitk.GetArrayFromImage(image)



def load_nii(file_path):
    image = sitk.ReadImage(file_path)
    return sitk.GetArrayFromImage(image)


def extract_features_3d(image_input, mask_input, feature_type='all'):
    # Initial setup
    extractor = featureextractor.RadiomicsFeatureExtractor()
    all_features = {}

    # Load the .nii files using SimpleITK
    if isinstance(image_input, str):
        image_input = sitk.ReadImage(image_input)
    if isinstance(mask_input, str):
        mask_input = sitk.ReadImage(mask_input)
    
    # Manually set the direction for the image
    desired_direction = (-1.0000000e+00, 0.0000000e+00, 0.0000000e+00,
                     0.0000000e+00, -1.0000000e+00, 0.0000000e+00,
                     0.0000000e+00, 0.0000000e+00, 1.0000000e+00)

    image_input.SetDirection(desired_direction)
    mask_input.SetDirection(desired_direction)
    
    mask_array = sitk.GetArrayFromImage(mask_input)

    # Extract features for each unique label in the mask
    for label in np.unique(mask_array):
        if label == 0:  # Skip the background
            continue

        new_mask_image = sitk.GetImageFromArray(np.full(mask_array.shape, label))
        new_mask_image.SetDirection(mask_input.GetDirection())
        new_mask_image.SetOrigin(mask_input.GetOrigin())
        new_mask_image.SetSpacing(mask_input.GetSpacing())
        binary_mask = sitk.Cast(sitk.Equal(mask_input, sitk.Cast(new_mask_image, mask_input.GetPixelID())), sitk.sitkUInt8)


        result_original = {}
        result_wavelet = {}

        if feature_type in ['all', 'original', 'shape', 'texture', 'first-order']:
            feature_classes = ['firstorder', 'shape', 'glcm', 'gldm', 'glrlm', 'glszm', 'ngtdm']

            for feature_class in feature_classes:
                extractor.enableFeatureClassByName(feature_class, False) # Disable all first

            if feature_type == 'all' or feature_type == 'original':
                for feature_class in feature_classes:
                    extractor.enableFeatureClassByName(feature_class, True)
            elif feature_type == 'shape':
                extractor.enableFeatureClassByName('shape', True)
            elif feature_type == 'texture':
                texture_features = ['glcm', 'gldm', 'glrlm', 'glszm', 'ngtdm']
                for feature_class in texture_features:
                    extractor.enableFeatureClassByName(feature_class, True)
            elif feature_type == 'first-order':
                extractor.enableFeatureClassByName('firstorder', True)

            result_original = extractor.execute(image_input, binary_mask)

        if feature_type in ['all', 'wavelet']:
            extractor.enableImageTypeByName('Wavelet', True)
            extractor.enableImageTypeByName('Original', False)

            extractor.enableFeatureClassByName('firstorder', True)
            extractor.enableFeatureClassByName('glcm', True)

            result_wavelet = extractor.execute(image_input, binary_mask)

        result = {**result_original, **result_wavelet}
        features_label = {k + f"_label_{label}": v for k, v in result.items() if not k.startswith(('general_', 'diagnostics_'))}
        all_features.update(features_label)

    return all_features

def extract_features_from_multiple_images_3d(images_folder, masks_folder, output_csv, feature_type='all'):
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.nii') or f.endswith(".nii.gz")]
    if not image_files:
        return False, "No image files found in the folder"

    csv_file = open(output_csv, 'w', newline='')
    csvwriter = csv.writer(csv_file)
    
    headers_written = False

    for image_name in image_files:
        image_path = os.path.join(images_folder, image_name)

        # Handle both .nii and .nii.gz correctly using os.path.splitext multiple times
        base_name, ext = os.path.splitext(image_name)
        if ext == ".gz":  # This indicates the file is a .nii.gz
            base_name, _ = os.path.splitext(base_name)  # Remove the .nii part as well
            ext = ".nii.gz"
        else:
            ext = ".nii"

        mask_name = f"{base_name}_mask{ext}"
        mask_path = os.path.join(masks_folder, mask_name)

        # Check if both image and mask files exist
        if not os.path.exists(image_path):
            print(f"Image file does not exist: {image_path}")
            continue

        if not os.path.exists(mask_path):
            print(f"Mask file does not exist: {mask_path}")
            continue

        try:
            slice_features = extract_features_3d(image_path, mask_path, feature_type)
            
            # Check if slice_features is empty or None
            if not slice_features:
                print(f"No features extracted for image: {image_name}")
                continue

            # Write to CSV
            if not headers_written:
                headers = ['Image_Name'] + list(slice_features.keys())
                csvwriter.writerow(headers)
                headers_written = True
            row = [image_name] + list(slice_features.values())
            csvwriter.writerow(row)
        except Exception as e:
            print(f"Error during feature extraction for image {image_name}: {e}")
    csv_file.close()
    return True, "Feature extraction completed"



def extract_features_2d(image_input, mask_input, feature_type='all'):
    extractor = featureextractor.RadiomicsFeatureExtractor()
    result_original = {}
    result_wavelet = {}

    if isinstance(image_input, np.ndarray):
        image_input = sitk.GetImageFromArray(image_input, isVector=False)
    if isinstance(mask_input, np.ndarray):
        mask_input = sitk.GetImageFromArray(mask_input, isVector=False)

    if feature_type in ['all', 'original', 'shape', 'texture', 'first-order']:
        extractor.enableImageTypeByName('Original', True)

        feature_classes = ['firstorder', 'shape2D', 'glcm', 'gldm', 'glrlm', 'glszm', 'ngtdm']
        if feature_type in ['all', 'original']:
            for feature_class in feature_classes:
                extractor.enableFeatureClassByName(feature_class, True)
        elif feature_type == 'shape':
            for feature_class in feature_classes:
                extractor.enableFeatureClassByName(feature_class, feature_class == 'shape2D')
        elif feature_type == 'texture':
            texture_features = ['glcm', 'gldm', 'glrlm', 'glszm', 'ngtdm']
            for feature_class in feature_classes:
                extractor.enableFeatureClassByName(feature_class, feature_class in texture_features)
        elif feature_type == 'first-order':
            # Disable all feature classes and enable only 'firstorder'
            for feature_class in feature_classes:
                extractor.enableFeatureClassByName(feature_class, feature_class == 'firstorder')
            
        extractor.settings['force2D'] = True
        result_original = extractor.execute(image_input, mask_input)

    if feature_type in ['all', 'wavelet']:
        extractor = featureextractor.RadiomicsFeatureExtractor()  # re-initializing to reset settings
        extractor.enableImageTypeByName('Wavelet', True)
        extractor.enableImageTypeByName('Original', False)
        

        # Specify which 'wavelet' features you want to enable. You can modify this according to your needs
        extractor.enableFeatureClassByName('firstorder', True)
        extractor.enableFeatureClassByName('glcm', True)
        
        result_wavelet = extractor.execute(image_input, mask_input)

    result = {**result_original, **result_wavelet}
    features = {k: v for k, v in result.items() if not k.startswith(('general_', 'diagnostics_'))}
    return features

def extract_features_from_multiple_images_2d(images_folder, masks_folder, output_csv, feature_type='all'):
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.png')]
    if not image_files:
        return False, "No image files found in the folder"

    csv_file = open(output_csv, 'w', newline='')
    csvwriter = csv.writer(csv_file)
    
    headers_written = False
    for image_name in image_files:
        image_path = os.path.join(images_folder, image_name)
        image_data = load_png(image_path)

        mask_name = os.path.splitext(image_name)[0] + '_mask.png'
        mask_path = os.path.join(masks_folder, mask_name)

        if os.path.exists(mask_path):
            mask_data_original = load_png(mask_path)

            # Check if the mask is 2D binary and convert it to 3D RGB if it is
            if len(mask_data_original.shape) == 2 or mask_data_original.shape[2] == 1:
                mask_data_original = np.stack((mask_data_original,) * 3, axis=-1)
                mask_data_original = (mask_data_original * np.array([255, 255, 255])).astype(np.uint8)


            # Identify unique colors in the mask, ignoring black [0, 0, 0]
            unique_colors = np.unique(mask_data_original.reshape(-1, mask_data_original.shape[2]), axis=0)
            unique_colors = unique_colors[~np.all(unique_colors == 0, axis=1)]

            for color in unique_colors:
                # Creating binary mask for the current color
                mask_data = np.all(mask_data_original == color, axis=-1).astype(int)

                if np.any(mask_data):
                    try:
                        slice_features = extract_features_2d(image_data, mask_data, feature_type)
                        if not headers_written:
                            headers = ['Image_Name', 'Mask_Color'] + list(slice_features.keys())
                            csvwriter.writerow(headers)
                            headers_written = True
                        row = [image_name, '_'.join(map(str, color))] + list(slice_features.values())
                        csvwriter.writerow(row)
                    except Exception as e:
                        print(f"Error during feature extraction: {e}")
    csv_file.close()
    return True, "Feature extraction completed"


def disable_buttons(state):
    btn_image_folder['state'] = state
    btn_mask_folder['state'] = state
    btn_output_folder['state'] = state
    for btn in feature_buttons_widgets:
        btn['state'] = state
    
def determine_image_type(folder_path):
    # Check for image file types in the selected folder
    files_in_directory = os.listdir(folder_path)

    # Check for PNG files
    png_files = [f for f in files_in_directory if f.endswith(".png")]
    
    # Check for JPEG files
    jpeg_files = [f for f in files_in_directory if f.endswith(".jpg") or f.endswith(".jpeg")]
    
    # Check for NII files
    nii_files = [f for f in files_in_directory if f.endswith(".nii") or f.endswith(".nii.gz")]

    # Return detected image type
    if png_files:
        return "2D Image"
    elif jpeg_files:
        return "2D Image"
    elif nii_files:
        return "3D Image"
    else:
        return "Unkown Image Dimension"

def select_image_folder():
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    if not folder_path:
        return

    entry_image_folder.delete(0, tk.END)
    entry_image_folder.insert(0, folder_path)
    
    # Display detected image type immediately
    image_type = determine_image_type(folder_path)
    bulb_label.config(text=image_type)

def select_mask_folder():
    folder_path = filedialog.askdirectory(title="Select Mask Folder")
    if not folder_path:
        return

    entry_mask_folder.delete(0, tk.END)
    entry_mask_folder.insert(0, folder_path)
    
    # Display detected image type immediately
    mask_type = determine_image_type(folder_path)
    bulb_label.config(text=mask_type)


def threaded_feature_extraction(feature_type):
    try:
        disable_buttons(tk.DISABLED)  # Disable all buttons
        
        # Initialize Progress Bar
        progress_bar.grid(row=1, column=0, columnspan=5, sticky="ew")
        progress_bar.start()
        
        run_feature_extraction(feature_type)
        
        progress_bar.stop()  # Stop the progress bar
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        progress_bar.grid_remove()  # Remove or hide the progress bar
        disable_buttons(tk.NORMAL)  # Enable all buttons


def select_output_folder():
    folder_selected = filedialog.askdirectory()
    entry_output_folder.delete(0, tk.END)
    entry_output_folder.insert(0, folder_selected)

    

def run_feature_extraction(feature_type=None):
    images_folder = entry_image_folder.get()
    mask_folder = entry_mask_folder.get()
    output_folder = entry_output_folder.get()

    if not images_folder or not mask_folder or not output_folder:
        messagebox.showwarning("Warning", "Please select all folders.")
        return

    # Determine image type for both folders and display it
    images_type = determine_image_type(images_folder)
    masks_type = determine_image_type(mask_folder)
    
    # Update the output panel with the detected image types
    output_panel.insert(tk.END, f"Image Folder Type: {images_type.split(' ')[-1]}\n")
    output_panel.insert(tk.END, f"Mask Folder Type: {masks_type.split(' ')[-1]}\n")
    output_panel.see(tk.END)

    masks_folders = mask_folder
    output_csv_path = os.path.normpath(os.path.join(output_folder, f'extracted_features_{feature_type}.csv'))

    if images_type == "2D Image" and masks_type == "2D Image":
        extraction_function = extract_features_from_multiple_images_2d
    elif images_type == "3D Image" and masks_type == "3D Image":
        extraction_function = extract_features_from_multiple_images_3d
    else:
        output_panel.insert(tk.END, f"Error: Mismatch between image and mask dimensions. Please ensure both are either 2D or 3D.\n")
        output_panel.see(tk.END)
        return

    try:
        success, message = extraction_function(images_folder, masks_folders, output_csv_path, feature_type)
        if success:
            output_panel.insert(tk.END, f"{message}\nOutput saved to {output_csv_path}\n")
        else:
            output_panel.insert(tk.END, f"Error: {message}\n")
    except Exception as e:
        output_panel.insert(tk.END, f"An error occurred: {str(e)}\n")
    output_panel.see(tk.END)



root = tk.Tk()
root.title("Radiomics Feature Extractor")

style = ttk.Style(root)
style.theme_use("clam")

frame_paths = ttk.Frame(root, padding=10)
frame_paths.pack(pady=5, padx=5, fill="x")

frame_actions = ttk.Frame(root, padding=10)
frame_actions.pack(pady=5, padx=5, fill="x")

frame_output = ttk.Frame(root, padding=10)
frame_output.pack(pady=5, padx=5, fill="both", expand=True)

label_image_folder = ttk.Label(frame_paths, text="Image Path:")
label_image_folder.grid(row=0, column=0, sticky="w", padx=5)

entry_image_folder = ttk.Entry(frame_paths, width=40)
entry_image_folder.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


btn_image_folder = ttk.Button(frame_paths, text="Browse", command=select_image_folder)
btn_image_folder.grid(row=0, column=2, padx=5)

label_mask_folder = ttk.Label(frame_paths, text="Mask Path:")
label_mask_folder.grid(row=1, column=0, sticky="w", padx=5)

entry_mask_folder = ttk.Entry(frame_paths, width=40)
entry_mask_folder.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn_mask_folder = ttk.Button(frame_paths, text="Browse", command=select_mask_folder)
btn_mask_folder.grid(row=1, column=2, padx=5)

label_output_folder = ttk.Label(frame_paths, text="Output Path:")
label_output_folder.grid(row=2, column=0, sticky="w", padx=5)

entry_output_folder = ttk.Entry(frame_paths, width=40)
entry_output_folder.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

btn_output_folder = ttk.Button(frame_paths, text="Browse", command=select_output_folder)
btn_output_folder.grid(row=2, column=2, padx=5)

image_type_label = ttk.Label(frame_paths, text="")
image_type_label.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

bulb_label = ttk.Label(frame_paths, text="No Image Path Selected")  # Initial state
bulb_label.grid(row=3, column=2, padx=5)

frame_paths.columnconfigure(1, weight=1)

# Adding Progress Bar
progress_bar = ttk.Progressbar(frame_actions, mode='indeterminate')

# Buttons in the "frame_actions" frame
feature_buttons = ["First-Order", "Texture", "Shape", "Wavelet", "ALL"]
feature_buttons_widgets = []  # Keep track of the button widgets
for i, feature_type in enumerate(feature_buttons):
    btn_feature = ttk.Button(frame_actions, text=f"Extract {feature_type} Features",
                             command=lambda ft=feature_type.lower(): threading.Thread(target=threaded_feature_extraction, args=(ft,), daemon=True).start())
    btn_feature.grid(row=0, column=i, padx=5, pady=5)
    feature_buttons_widgets.append(btn_feature)

label_output = ttk.Label(frame_output, text="Output Console:")
label_output.pack(anchor="w", padx=5, pady=5)

output_panel = scrolledtext.ScrolledText(frame_output, width=80, height=10, wrap=tk.WORD)
output_panel.pack(fill="both", expand=True, padx=5, pady=5)

root.mainloop()
