import numpy as np
import pydicom

def adjust_hounsfield_units(dicom_file, new_slope=1, new_intercept=0):
    # Load the DICOM file
    ds = pydicom.dcmread(dicom_file)
    
    # Decompress the pixel data using GDCM
    ds.decompress()
    
    # Convert the original pixel data to Hounsfield Units (HU)
    original_hu = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
    
    clipped_hu = np.clip(original_hu, 0, 400)
    
    # Convert the clipped HU values back to pixel values
    adjusted_pixel_values = (clipped_hu - new_intercept) / new_slope
    ds.PixelData = adjusted_pixel_values.astype(np.int16).tobytes()
    ds.RescaleSlope = new_slope
    ds.RescaleIntercept = new_intercept
    
    return ds