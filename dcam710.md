DCAM 710 dependencies and setup

Require Vzense SDK and the Python wrapper
Manual: vzense/Vzense-DCAM710-Manual-20210906.pdf

Pi 4 model B USB current limit : 1200mA total so stick to Range 0 mode which has peak 769mA power draw



IR 640x480 30fps in pixel sync with TOF Depth image RAW12 format

RGB all 30fps 1920x1080 1280x720 640x480 640x360 H264

PsFrameType
Description：
Specific image frame type.
PS: the number of enumeration values corresponding to different models of products
may be different. Please refer to the definition under the specific model folder in include.
Enumerator：
PsDepthFrame: depth image frame
PsIRFrame: IR gray image frame.
PsRGBFrame: RGB image frame.
PsMappedRGBFrame: RGB image which is mapped to Depth space.
PsMappedDepthFrame: Depth image which is mapped to RGB space.
PsMappedIRFrame: IR image whichi is mapped to RGB space.
PsWDRDepthFrame: WDR depth frame with 16bits per pixel in mm, only take effect when data mode set to PsWDR_Depth