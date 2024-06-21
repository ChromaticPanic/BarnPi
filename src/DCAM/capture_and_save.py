from pickle import FALSE, TRUE
import sys

sys.path.append("./")

from API.Vzense_api_710 import *
import time
from datetime import datetime as dt

import os
import cv2
import dotenv
import socket


def validate_save_path(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def assert_required_folders(
    cache_dir: str,
    local_dir: str,
    data_dir: str,
    log_dir: str,
    rgb_dir: str,
    depth_dir: str,
    ir_dir: str,
):
    validate_save_path(cache_dir)
    validate_save_path(local_dir)
    validate_save_path(cache_dir + "/" + data_dir)
    validate_save_path(cache_dir + "/" + log_dir)
    validate_save_path(local_dir + "/" + data_dir)
    validate_save_path(local_dir + "/" + log_dir)
    validate_save_path(cache_dir + "/" + data_dir + "/" + rgb_dir)
    validate_save_path(cache_dir + "/" + data_dir + "/" + depth_dir)
    validate_save_path(cache_dir + "/" + data_dir + "/" + ir_dir)
    validate_save_path(local_dir + "/" + data_dir + "/" + rgb_dir)
    validate_save_path(local_dir + "/" + data_dir + "/" + depth_dir)
    validate_save_path(local_dir + "/" + data_dir + "/" + ir_dir)


def get_current_time():
    return round(
        # dt.now(datetime.UTC).timestamp() * 1000
        dt.now().timestamp()
        * 1000
    )  # get current time in milliseconds


class CaptureModel:
    def __init__(
        self,
        camera: VzenseTofCam,
        hostname: str,
        rgb_path: str,
        depth_path: str,
        ir_path: str,
        log_path: str,
        collect_rgb: bool,
        collect_depth: bool,
        collect_ir: bool,
        collect_point_cloud: bool,
        capture_delay: float,
        capture_count: int,
        rgb_format: str,
    ):
        self.hostname = hostname
        self.camera = camera
        self.rgb_path = rgb_path
        self.depth_path = depth_path
        self.ir_path = ir_path
        self.log_path = log_path
        self.collect_rgb = collect_rgb
        self.collect_depth = collect_depth
        self.collect_ir = collect_ir
        self.collect_point_cloud = collect_point_cloud
        self.capture_delay = capture_delay
        self.capture_count = capture_count
        self.rgb_format = rgb_format


def get_time_str():
    return dt.now().strftime("%Y%m%d_%H%M%S")


def get_prefix(hostname: str) -> str:
    return hostname + "_" + get_time_str() + "_"


def read_next_frame(camera: VzenseTofCam, retries: int = 10):
    ret, frameready = camera.Ps2_ReadNextFrame()
    if ret != 0:
        print("Ps2_ReadNextFrame failed:", ret)
        time.sleep(0.2)
        print("retries left: ", retries)
        retries -= 1
    return frameready


def save_frames(config: CaptureModel):
    loops = config.capture_count
    time_curr = get_current_time()  # get current time in milliseconds
    time_delay = int(config.capture_delay * 1000)  # convert seconds to milliseconds
    time_last = time_curr - time_delay - 1
    retries = 10
    rgb_filetype = config.rgb_format

    while loops != 0:
        if time_curr - time_last > time_delay:
            time_curr = get_current_time()
            print(f"{get_time_str()}: Collecting frames")
            frameready = read_next_frame(config.camera, retries)

            if config.collect_rgb:
                _retries = 10
                while not frameready.rgb and _retries > 0:
                    print("retrying to get rgb frame")
                    frameready = read_next_frame(config.camera, retries)
                    _retries -= 1
                    time.sleep(0.05)
                prefix = get_prefix(config.hostname)
                time_last = time_curr

                print("getting rgb frame")
                ret, rgbframe = config.camera.Ps2_GetFrame(PsFrameType.PsRGBFrame)

                # filename = config.rgb_path + f"/{prefix}rgb.bin"
                # file = open(filename, "wb+")
                # for i in range(rgbframe.dataLen):
                #     file.write(c_uint8(rgbframe.pFrameData[i]))

                # file.close()
                frametmp = numpy.ctypeslib.as_array(
                    rgbframe.pFrameData, (1, rgbframe.width * rgbframe.height * 3)
                )
                frametmp.dtype = numpy.uint8
                frametmp.shape = (rgbframe.height, rgbframe.width, 3)
                cv2.imwrite(config.rgb_path + f"/{prefix}rgb.{rgb_filetype}", frametmp)

                print("rgb save ok")

            if config.collect_ir:
                _retries = 10
                while not frameready.ir and _retries > 0:
                    print("retrying to get ir frame")
                    frameready = read_next_frame(config.camera, retries)
                    _retries -= 1
                    time.sleep(0.05)
                prefix = get_prefix(config.hostname)
                time_last = time_curr

                print("getting ir frame")
                ret, irframe = config.camera.Ps2_GetFrame(PsFrameType.PsIRFrame)

                filename = config.ir_path + f"/{prefix}ir.bin"
                file = open(filename, "wb+")
                for i in range(irframe.dataLen):
                    file.write(c_uint8(irframe.pFrameData[i]))

                file.close()

                print("ir save ok")

            if config.collect_depth:
                _retries = 10
                while not frameready.depth and _retries > 0:
                    print("retrying to get depth frame")
                    frameready = read_next_frame(config.camera, retries)
                    _retries -= 1
                    time.sleep(0.05)
                prefix = get_prefix(config.hostname)
                time_last = time_curr

                print("getting depth frame")
                ret, depthframe = config.camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)

                filename = config.depth_path + f"/{prefix}depth.bin"
                file = open(filename, "wb+")
                for i in range(depthframe.dataLen):
                    file.write(c_uint8(depthframe.pFrameData[i]))

                file.close()
                print("depth save ok")
                if config.collect_point_cloud:
                    ret, pointlist = config.camera.Ps2_ConvertDepthFrameToWorldVector(
                        depthframe
                    )
                    if ret == 0:

                        filename = config.depth_path + f"/{prefix}point_cloud.txt"
                        file = open(filename, "w")

                        for i in range(depthframe.width * depthframe.height):
                            if pointlist[i].z != 0 and pointlist[i].z != 65535:
                                file.write(
                                    "{0},{1},{2}\n".format(
                                        pointlist[i].x, pointlist[i].y, pointlist[i].z
                                    )
                                )

                        file.close()
                        print("point cloud save ok")
                    else:
                        print("Ps2_ConvertDepthFrameToWorldVector failed:", ret)

            loops -= 1
        time_curr = get_current_time()


def camera_init(camera: str) -> VzenseTofCam:
    camera_count = camera.Ps2_GetDeviceCount()
    retry_count = 5
    while camera_count == 0 and retry_count > 0:
        retry_count = retry_count - 1
        camera_count = camera.Ps2_GetDeviceCount()
        time.sleep(1)
        print("scaning......   ", retry_count)

    device_info = PsDeviceInfo()

    if camera_count > 1:
        ret, device_infolist = camera.Ps2_GetDeviceListInfo(camera_count)
        if ret == 0:
            device_info = device_infolist[0]
            for info in device_infolist:
                print("cam uri:  " + str(info.uri))
        else:
            print(" failed:" + ret)
            exit()
    elif camera_count == 1:
        ret, device_info = camera.Ps2_GetDeviceInfo()
        if ret == 0:
            print("cam uri:" + str(device_info.uri))
        else:
            print(" failed:" + ret)
            exit()
    else:
        print("there are no camera found")
        exit()

    if PsConnectStatus.Connected.value != device_info.status:
        print("connect statu:", device_info.status)
        print(
            "Call Ps2_OpenDevice with connect status :", PsConnectStatus.Connected.value
        )
        exit()
    else:
        print("uri: " + str(device_info.uri))
        print("alias: " + str(device_info.alias))
        print("connectStatus: " + str(device_info.status))

    ret = camera.Ps2_OpenDevice(device_info.uri)
    if  ret != 0:  
        print("Ps2_OpenDevice failed: " + str(ret))
        exit()

    ret = camera.Ps2_StartStream()
    if  ret != 0:  
        print("Ps2_StartStream failed:", ret)
        exit()

    ret = camera.Ps2_SetDataMode(PsDataMode.PsDepthAndIR_15_RGB_30)
    if  ret != 0:  
        print("Ps2_SetDataMode failed:",ret)
        exit()
        
    ret = camera.Ps2_SetRGBResolution(PsResolution.PsRGB_Resolution_640_480)
    if  ret != 0:  
        print("Ps2_SetRGBResolution failed:",ret)
        exit()

    return camera


def camera_close(camera: str) -> bool:
    ret = camera.Ps2_StopStream()
    if  ret != 0:  
        print("Ps2_StopStream failed: " + str(ret))

    ret = camera.Ps2_CloseDevice()
    if  ret != 0:  
        print("Ps2_CloseDevice failed: " + str(ret))


def main():
    dotenv.load_dotenv("./capture_config.ini")
    cache_dir = os.getenv("CACHE_DIR")
    local_dir = os.getenv("LOCAL_DIR")
    data_dir = os.getenv("DATA_DIR")
    log_dir = os.getenv("LOG_DIR")
    rgb_dir = os.getenv("RGB_DIR")
    depth_dir = os.getenv("DEPTH_DIR")
    ir_dir = os.getenv("IR_DIR")
    assert_required_folders(
        cache_dir, local_dir, data_dir, log_dir, rgb_dir, depth_dir, ir_dir
    )
    rgb_path = cache_dir + "/" + data_dir + "/" + rgb_dir
    depth_path = cache_dir + "/" + data_dir + "/" + depth_dir
    ir_path = cache_dir + "/" + data_dir + "/" + ir_dir
    log_path = cache_dir + "/" + log_dir
    capture_delay = float(os.getenv("CAPTURE_DELAY_SECONDS"))
    collect_rgb = bool(os.getenv("COLLECT_RGB"))
    collect_depth = bool(os.getenv("COLLECT_DEPTH"))
    collect_ir = bool(os.getenv("COLLECT_IR"))
    collect_point_cloud = bool(os.getenv("COLLECT_POINT_CLOUD"))
    capture_count = int(os.getenv("CAPTURE_COUNT"))
    rgb_format = os.getenv("RGB_FILE_FORMAT")
    hostname = socket.gethostname()

    camera = camera_init(VzenseTofCam())
    if isinstance(camera, VzenseTofCam):
        save_frames(
            CaptureModel(
                **{
                    "camera": camera,
                    "hostname": hostname,
                    "rgb_path": rgb_path,
                    "depth_path": depth_path,
                    "ir_path": ir_path,
                    "log_path": log_path,
                    "collect_rgb": collect_rgb,
                    "collect_depth": collect_depth,
                    "collect_ir": collect_ir,
                    "collect_point_cloud": collect_point_cloud,
                    "capture_delay": capture_delay,
                    "capture_count": capture_count,
                    "rgb_format": rgb_format,
                }
            )
        )
        camera_close(camera)
    else:
        print("Camera initialization failed")

    print("Capture completed without errors")


if __name__ == "__main__":
    main()
