from pickle import FALSE, TRUE
import sys

sys.path.append("./")

from API.Vzense_api_710 import *
import time
import datetime
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
        datetime.datetime.now(datetime.UTC).timestamp() * 1000
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
        capture_delay: float,
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
        self.capture_delay = capture_delay


def save_frames(config: CaptureModel):
    run_once = TRUE
    time_curr = get_current_time()  # get current time in milliseconds
    time_delay = int(config.capture_delay * 1000)  # convert seconds to milliseconds
    time_last = time_curr + time_delay + 1
    retries = 10
    rgb_saved = FALSE
    depth_saved = FALSE
    ir_saved = FALSE

    while time_curr - time_last < time_delay and retries > 0:
        time_curr = get_current_time()
        prefix = config.hostname + "_" + str(time_curr)

        ret, frameready = config.camera.Ps2_ReadNextFrame()
        if ret != 0:
            print("Ps2_ReadNextFrame failed:", ret)
            time.sleep(1)
            print("retries left: ", retries)
            retries -= 1
            continue

        if config.collect_rgb or config.collect_depth or config.collect_ir:
            time_last = time_curr

        if config.collect_rgb and (not rgb_saved) and frameready.rgb:
            ret, rgbframe = config.camera.Ps2_GetFrame(PsFrameType.PsRGBFrame)

            filename = config.rgb_path + "/rgb.bin"
            file = open(filename, "wb+")
            for i in range(rgbframe.dataLen):
                file.write(c_uint8(rgbframe.pFrameData[i]))

            file.close()
            frametmp = numpy.ctypeslib.as_array(
                rgbframe.pFrameData, (1, rgbframe.width * rgbframe.height * 3)
            )
            frametmp.dtype = numpy.uint8
            frametmp.shape = (rgbframe.height, rgbframe.width, 3)
            cv2.imwrite(config.rgb_path + "/rgb.png", frametmp)
            cv2.imwrite(config.rgb_path + "/rgb.jpg", frametmp)
            rgb_saved = TRUE

            print("rgb save ok")

        if config.collect_depth and (not depth_saved) and frameready.depth:
            ret, depthframe = config.camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)

            filename = config.depth_path + "/depth.bin"
            file = open(filename, "wb+")
            for i in range(depthframe.dataLen):
                file.write(c_uint8(depthframe.pFrameData[i]))

            file.close()
            # ret, pointlist = config.camera.Ps2_ConvertDepthFrameToWorldVector(depthframe)
            # if  ret == 0:

            #     filename = config.depth_path + "/point.txt"
            #     file = open(filename,"w")

            #     for i in range(depthframe.width*depthframe.height):
            #         if pointlist[i].z!=0 and pointlist[i].z!=65535:
            #             file.write("{0},{1},{2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

            #     file.close()
            #     print("point cloud save ok")
            # else:
            #     print("Ps2_ConvertDepthFrameToWorldVector failed:",ret)
            depth_saved = TRUE

            print("depth save ok")

        if config.collect_ir and (not ir_saved) and frameready.ir:
            ret, irframe = config.camera.Ps2_GetFrame(PsFrameType.PsIRFrame)

            filename = config.ir_path + "/ir.bin"
            file = open(filename, "wb+")
            for i in range(irframe.dataLen):
                file.write(c_uint8(irframe.pFrameData[i]))

            file.close()
            ir_saved = TRUE

            print("ir save ok")

        if config.collect_rgb == rgb_saved and config.collect_depth == depth_saved and config.collect_ir == ir_saved:
            rgb_saved = FALSE
            depth_saved = FALSE
            ir_saved = FALSE

            if run_once:
                break
            


def camera_init(camera: str) -> VzenseTofCam:
    camera_count = camera.Ps2_GetDeviceCount()
    retry_count = 20
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
    if ret == 0:
        print("open device successful")
    else:
        print("Ps2_OpenDevice failed: " + str(ret))
        exit()

    ret = camera.Ps2_StartStream()
    if ret == 0:
        print("start stream successful")
    else:
        print("Ps2_StartStream failed:", ret)
        exit()

    return camera


def camera_close(camera: str) -> bool:
    ret = camera.Ps2_StopStream()
    if ret == 0:
        print("stop stream successful")
    else:
        print("Ps2_StopStream failed: " + str(ret))

    ret = camera.Ps2_CloseDevice()
    if ret == 0:
        print("close device successful")
    else:
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
    hostname = socket.gethostname()

    camera = camera_init(VzenseTofCam())
    if isinstance(camera, VzenseTofCam):
        save_frames(CaptureModel(**{
            'camera': camera,
            'hostname': hostname,
            'rgb_path': rgb_path,
            'depth_path': depth_path,
            'ir_path': ir_path,
            'log_path': log_path,
            'collect_rgb': collect_rgb,
            'collect_depth': collect_depth,
            'collect_ir': collect_ir,
            'capture_delay': capture_delay,
        }))
        camera_close(camera)
    else:
        print("Camera initialization failed")


if __name__ == "__main__":
    main()
