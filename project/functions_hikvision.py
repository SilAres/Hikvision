from hikvisionapi import Client
import re
import pandas as pd


def reboot(serv, login, passw):
    """

    :param serv: ip регистратора
    :param login: логин
    :param passw: пароль
    :return: перезагрузка регистратора

    """
    cam = Client('http://'+serv, login, passw, timeout=30)
    cam.System.reboot(method='PUT')


def hikvision_modify_date_seting(serv, login, passw):
    """

    :param serv: ip регистратора
    :param login: логин
    :param passw: пароль
    :return: Изменения настроек даты и времени

    """
    cam = Client('http://'+serv, login, passw, timeout=30)
    url_cam = cam.ContentMgmt.InputProxy.channels(method='get')
    for i in range(len(url_cam.get("InputProxyChannelList").get("InputProxyChannel"))):
        try:
            url_dtd = cam.System.Video.inputs.channels[i+1].overlays.dateTime(method='get', present='text')
            date_style_pattern = "<dateStyle>.*</dateStyle>"
            date_style = "<dateStyle>DD-MM-YYYY</dateStyle>"
            url_dtd = re.sub(date_style_pattern, date_style, url_dtd)
            cam.System.Video.inputs.channels[i+1].overlays.dateTime(method='put', data=url_dtd)  # добавить проверку
        except:
            pass


def data_collection(serv, login, passw):
    """
    Заменить все сслыки на get("value", {})
    :param serv: ip регистратора
    :param login: логин
    :param passw: пароль
    :return: Датафрейм настроек регистратора
    """
    df = pd.DataFrame()
    user_hik1 = []
    try:
        cam = Client('http://' + serv, login, passw, timeout=30)
    except:
        print("Error checking the video recorder : " + serv)
        return []
        # continue при нескольких сервера, надо предусмотреть альтернативу при переходе на def
    url_ntp = cam.System.time.NTPservers(method='get')
    if url_ntp["NTPServerList"]["NTPServer"]["addressingFormatType"] == "hostname":
        ntp_server = url_ntp["NTPServerList"]["NTPServer"]["hostName"]
    else:
        ntp_server = url_ntp["NTPServerList"]["NTPServer"]["ipAddress"]
    url_ip = cam.System.Network.interfaces(method='get')
    url_info = cam.System.deviceInfo(method='get')
    url_cam = cam.ContentMgmt.InputProxy.channels(method='get')
    if len(url_ip["NetworkInterfaceList"]["NetworkInterface"]) > 1:
        ip_address_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["ipAddress"]
        subnet_mask_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["subnetMask"]
        addressing_type_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["addressingType"]
        mac_address_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["Link"]["MACAddress"]

        ip_address_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["ipAddress"]
        subnet_mask_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["subnetMask"]
        addressing_type_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["addressingType"]
        mac_address_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["Link"]["MACAddress"]
    else:
        ip_address_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["ipAddress"]
        subnet_mask_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["subnetMask"]
        addressing_type_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["addressingType"]
        mac_address_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["Link"]["MACAddress"]

        ip_address_2 = ""
        subnet_mask_2 = ""
        addressing_type_2 = ""
        mac_address_2 = ""

    device_name = url_info["DeviceInfo"]["deviceName"]
    devicemodel = url_info["DeviceInfo"]["model"]
    device_firmware_version = url_info["DeviceInfo"]["firmwareVersion"]
    device_firmware_released_date = url_info["DeviceInfo"]["firmwareReleasedDate"]

    try:
        urluser = cam.Security.users(method='get')
        for UserHik in urluser["UserList"]["User"]:
            temp = UserHik["userName"], UserHik["userLevel"]
            user_hik1.append(temp)
    except:
        pass

    # for i in range(1) :
    for i in range(len(url_cam["InputProxyChannelList"]["InputProxyChannel"])):
        k = int(url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["id"])
        # print("i=",i)
        video_codec_type_sub = ""
        video_resolution_width_sub = ""
        video_resolution_height_sub = ""
        video_quality_control_type_sub = ""
        vbr_upper_cap_sub = ""
        max_frame_rate_sub = ""
        video_codec_type_main = ""
        video_resolution_width_main = ""
        video_resolution_height_main = ""
        video_quality_control_type_main = ""
        smart_codec_main = ""
        vbr_upper_cap_main = ""
        max_frame_rate_main = ""
        motion_detection = ""
        date_time_overlay = ""
        enabled = ""
        enable_highlight = ""
        grid_map = ""
        daysrec = [[], [], [], [], [], [], []]
        try:
            # print("k=",k)
            url_main = cam.Streaming.channels[k * 100 + 1](method='get')
            # print("k=",k)
            video_codec_type_main = url_main["StreamingChannel"]["Video"]["videoCodecType"]
            video_resolution_width_main = url_main["StreamingChannel"]["Video"]["videoResolutionWidth"]
            video_resolution_height_main = url_main["StreamingChannel"]["Video"]["videoResolutionHeight"]
            video_quality_control_type_main = url_main["StreamingChannel"]["Video"]["videoQualityControlType"]
            smart_codec_main = url_main["StreamingChannel"]["Video"]["SmartCodec"]["enabled"]
            vbr_upper_cap_main = url_main["StreamingChannel"]["Video"]["vbrUpperCap"]
            max_frame_rate_main = url_main["StreamingChannel"]["Video"]["maxFrameRate"]

            url_md = cam.System.Video.inputs.channels[k].motionDetection(method='get')
            url_dtd = cam.System.Video.inputs.channels[k].overlays.dateTime(method='get')

            motion_detection = url_md["MotionDetection"]["MotionDetectionLayout"]["sensitivityLevel"]
            enabled = url_md["MotionDetection"]["enabled"]
            enable_highlight = url_md["MotionDetection"]["enabled"]
            grid_map = url_md["MotionDetection"]["MotionDetectionLayout"]["layout"]["gridMap"]

            date_time_overlay = url_dtd["DateTimeOverlay"]["dateStyle"]

            url_rec = cam.ContentMgmt.record.tracks[k * 100 + 1](method='get')
            # print(url_rec)
            daysrec = []
            for fragmentid in range(7):
                fragment = url_rec["Track"]["TrackSchedule"]["ScheduleBlockList"]["ScheduleBlock"]["ScheduleAction"][
                    fragmentid]
                rec = fragment["ScheduleActionStartTime"], fragment["ScheduleActionEndTime"], fragment["Actions"][
                    "Record"], fragment["Actions"]["ActionRecordingMode"]
                daysrec.append(rec)

            url_sub = cam.Streaming.channels[k * 100 + 2](method='get')
            video_codec_type_sub = url_sub["StreamingChannel"]["Video"]["videoCodecType"]
            video_resolution_width_sub = url_sub["StreamingChannel"]["Video"]["videoResolutionWidth"]
            video_resolution_height_sub = url_sub["StreamingChannel"]["Video"]["videoResolutionHeight"]
            video_quality_control_type_sub = url_sub["StreamingChannel"]["Video"]["videoQualityControlType"]
            vbr_upper_cap_sub = url_sub["StreamingChannel"]["Video"]["vbrUpperCap"]
            max_frame_rate_sub = url_sub["StreamingChannel"]["Video"]["maxFrameRate"]

        except:
            if video_codec_type_main == "":
                video_codec_type_sub = "не работает канал"
                video_resolution_width_sub = "не работает канал"
                video_resolution_height_sub = "не работает канал"
                video_quality_control_type_sub = "не работает канал"
                vbr_upper_cap_sub = "не работает канал"
                max_frame_rate_sub = "не работает канал"
                video_codec_type_main = "не работает канал"
                video_resolution_height_main = "не работает канал"
                video_quality_control_type_main = "не работает канал"
                smart_codec_main = "не работает канал"
                vbr_upper_cap_main = "не работает канал"
                max_frame_rate_main = "не работает канал"
                motion_detection = "не работает канал"
                date_time_overlay = "не работает канал"
                video_resolution_width_main = "не работает канал"

        cam_name = url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["name"]
        cam_ip_address = url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["sourceInputPortDescriptor"][
            "ipAddress"]

        datereg = [[serv, device_name, devicemodel, device_firmware_version, device_firmware_released_date,
                    ntp_server, k, cam_name, cam_ip_address, video_codec_type_main,
                    video_resolution_width_main, video_resolution_height_main, video_quality_control_type_main,
                    smart_codec_main, vbr_upper_cap_main, max_frame_rate_main, video_codec_type_sub,
                    video_resolution_width_sub, video_resolution_height_sub,
                    video_quality_control_type_sub, vbr_upper_cap_sub, max_frame_rate_sub, enabled,
                    enable_highlight, motion_detection, grid_map,
                    date_time_overlay, ip_address_1, subnet_mask_1, addressing_type_1, mac_address_1,
                    ip_address_2, subnet_mask_2, addressing_type_2, mac_address_2, user_hik1,
                    daysrec[0], daysrec[1], daysrec[2], daysrec[3], daysrec[4], daysrec[5], daysrec[6]
                    ]]
        df = df.append(pd.DataFrame(datereg), ignore_index=True)
    return df

def hikvision_motionDetection(serv, login, passw):
    """

    :param serv: ip регистратора
    :param login: логин
    :param passw: пароль
    :return: Изменения параметров маски и motionDetection
    - sensitivityLevel -100 максимальная чувсствительность
    """
    cam = Client('http://'+serv, login, passw , timeout=30)
    url_cam = cam.ContentMgmt.InputProxy.channels(method='get')
    for i in range(len(url_cam.get("InputProxyChannelList").get("InputProxyChannel"))) :
        try:
            k = int(url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["id"])
            url_md = cam.System.Video.inputs.channels[k].motionDetection(method='get', present='text')
            enabled = "<enabled>true</enabled>"
            enable_highlight = "<enableHighlight>true</enableHighlight>"
            sensitivity_level = "<sensitivityLevel>100</sensitivityLevel>"
            grid_map = "<gridMap>fffffcfffffcfffffcfffffcfffff" \
                       "cfffffcfffffcfffffcf" \
                       "ffffcfffffcfffffcfffffc" \
                       "fffffcfffffcfffffcfff" \
                       "ffcfffffcfffffc" \
                       "</gridMap>"
            sensitivity_level_pattern = "<sensitivityLevel>.*</sensitivityLevel>"
            grid_map_pattern = "<gridMap>.*</gridMap>"
            enabled_pattern = "<enabled>.*</enabled>"
            enable_highlight_pattern = "<enableHighlight>.*</enableHighlight>"
            url_md = re.sub(sensitivity_level_pattern, sensitivity_level, url_md)
            url_md = re.sub(grid_map_pattern, grid_map, url_md)
            url_md = re.sub(enabled_pattern, enabled, url_md)
            url_md = re.sub(enable_highlight_pattern, enable_highlight, url_md)
            cam.System.Video.inputs.channels[k].motionDetection(method='put', data=url_md)
        except:
            print(f'Во время изменения камеры произошла ошибка')

def cam_setting_main(serv, login, passw):
    """

    :param serv: ip регистратора
    :param login: логин
    :param passw: пароль
    :return: Изменения параметров основного потока камер на регистраторе
    - sensitivityLevel -100 максимальная чувсствительность

    video_codec_type = H.264
    video_scan_type = progressive
    video_resolution_width = 1920
    video_resolution_height = 1080
    video_quality_control_type = VBR
    fixed_quality = 90
    vbr_upper_cap = 2048
    vbr_lower_cap = 32
    max_frame_rate = 2000
    snap_shot_image_type = JPEG
    enabled = false

    """

    cam = Client('http://'+serv, login, passw, timeout=30)
    url_cam = cam.ContentMgmt.InputProxy.channels(method='get')
    for i in range(len(url_cam["InputProxyChannelList"]["InputProxyChannel"])):
        k = int(url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["id"])
        try:
            url_main = cam.Streaming.channels[k * 100 + 1](method='get', present='text')
        except:
            print("Error checking the video channels : " + str(k))
            continue

        video_codec_type_pattern = "\<videoCodecType\>.*\<\/videoCodecType\>"
        video_scan_type_pattern = "\<videoScanType\>.*\<\/videoScanType\>"
        video_resolution_width_pattern = "\<videoResolutionWidth\>.*\<\/videoResolutionWidth\>"
        video_resolution_height_pattern = "\<videoResolutionHeight\>.*\<\/videoResolutionHeight\>"
        video_quality_control_type_pattern = "\<videoQualityControlType\>.*\<\/videoQualityControlType\>"
        fixed_quality_pattern = "\<fixedQuality\>.*\<\/fixedQuality\>"
        vbr_upper_cap_pattern = "\<vbrUpperCap\>.*\<\/vbrUpperCap\>"
        vbr_lower_cap_pattern = "\<vbrLowerCap\>.*\<\/vbrLowerCap\>"
        max_frame_rate_pattern = "\<maxFrameRate\>.*\<\/maxFrameRate\>"
        snap_shot_image_type_pattern = "\<snapShotImageType\>.*\<\/snapShotImageType\>"
        enabled_pattern = "\<enabled\>.*\<\/enabled\>"

        video_codec_type = "<videoCodecType>H.264</videoCodecType>"
        video_scan_type = "<videoScanType>progressive</videoScanType>"
        video_resolution_width = "<videoResolutionWidth>1920</videoResolutionWidth>"
        video_resolution_height = "<videoResolutionHeight>1080</videoResolutionHeight>"
        video_quality_control_type = "<videoQualityControlType>VBR</videoQualityControlType>"
        fixed_quality = "<fixedQuality>90</fixedQuality>"
        vbr_upper_cap = "<vbrUpperCap>2048</vbrUpperCap>"
        vbr_lower_cap = "<vbrLowerCap>32</vbrLowerCap>"
        max_frame_rate = "<maxFrameRate>2000</maxFrameRate>"
        snap_shot_image_type = "<snapShotImageType>JPEG</snapShotImageType>"
        enabled = "<enabled>false</enabled>"

        url_main = re.sub(video_codec_type_pattern, video_codec_type, url_main)
        url_main = re.sub(video_scan_type_pattern, video_scan_type, url_main)
        url_main = re.sub(video_resolution_width_pattern, video_resolution_width, url_main)
        url_main = re.sub(video_resolution_height_pattern, video_resolution_height, url_main)
        url_main = re.sub(video_quality_control_type_pattern, video_quality_control_type, url_main)
        url_main = re.sub(fixed_quality_pattern, fixed_quality, url_main)
        url_main = re.sub(vbr_upper_cap_pattern, vbr_upper_cap, url_main)
        url_main = re.sub(vbr_lower_cap_pattern, vbr_lower_cap, url_main)
        url_main = re.sub(max_frame_rate_pattern, max_frame_rate, url_main)
        url_main = re.sub(snap_shot_image_type_pattern, snap_shot_image_type, url_main)
        url_main = re.sub(enabled_pattern, enabled, url_main)
        try:
            cam.Streaming.channels[k * 100 + 1](method='put', data=url_main)
        except:
            print("Error checking the video channels : " + str(k))
            continue
