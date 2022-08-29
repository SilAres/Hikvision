from hikvisionapi import Client


def reboot(serv, login, passw):
    cam = Client('http://'+serv, login, passw , timeout=30)
    cam.System.reboot(method='PUT')


def data_collection(serv, login, passw):

    UserHik1 = []
    try:
        cam = Client('http://' + serv, login, passw, timeout=30)
    except:
        print("Error checking the video recorder : " + serv)
        continue
    url_NTP = cam.System.time.NTPservers(method='get')
    if url_NTP["NTPServerList"]["NTPServer"]["addressingFormatType"] == "hostname":
        NTPServer = url_NTP["NTPServerList"]["NTPServer"]["hostName"]
    else:
        NTPServer = url_NTP["NTPServerList"]["NTPServer"]["ipAddress"]

    url_ip = cam.System.Network.interfaces(method='get')

    url_info = cam.System.deviceInfo(method='get')

    url_cam = cam.ContentMgmt.InputProxy.channels(method='get')

    if len(url_ip["NetworkInterfaceList"]["NetworkInterface"]) > 1:
        ipAddress_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["ipAddress"]
        subnetMask_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["subnetMask"]
        addressingType_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["IPAddress"]["addressingType"]
        MACAddress_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"][0]["Link"]["MACAddress"]

        ipAddress_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["ipAddress"]
        subnetMask_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["subnetMask"]
        addressingType_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["IPAddress"]["addressingType"]
        MACAddress_2 = url_ip["NetworkInterfaceList"]["NetworkInterface"][1]["Link"]["MACAddress"]
    else:
        ipAddress_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["ipAddress"]
        subnetMask_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["subnetMask"]
        addressingType_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["IPAddress"]["addressingType"]
        MACAddress_1 = url_ip["NetworkInterfaceList"]["NetworkInterface"]["Link"]["MACAddress"]

        ipAddress_2 = ""
        subnetMask_2 = ""
        addressingType_2 = ""
        MACAddress_2 = ""

    deviceName = url_info["DeviceInfo"]["deviceName"]
    devicemodel = url_info["DeviceInfo"]["model"]
    device_firmwareVersion = url_info["DeviceInfo"]["firmwareVersion"]
    device_firmwareReleasedDate = url_info["DeviceInfo"]["firmwareReleasedDate"]

    try:
        urluser = cam.Security.users(method='get')
        for UserHik in urluser["UserList"]["User"]:
            temp = UserHik["userName"], UserHik["userLevel"]
            UserHik1.append(temp)
    except:
        pass

    # for i in range(1) :
    for i in range(len(url_cam["InputProxyChannelList"]["InputProxyChannel"])):
        k = int(url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["id"])
        # print("i=",i)
        videoCodecType_sub = ""
        videoResolutionWidth_sub = ""
        videoResolutionHeight_sub = ""
        videoQualityControlType_sub = ""
        vbrUpperCap_sub = ""
        maxFrameRate_sub = ""
        videoCodecType_main = ""
        videoResolutionWidth = ""
        videoResolutionHeight_main = ""
        videoQualityControlType_main = ""
        SmartCodec_main = ""
        vbrUpperCap_main = ""
        maxFrameRate_main = ""
        MotionDetection = ""
        DateTimeOverlay = ""
        enabled = ""
        enableHighlight = ""
        gridMap = ""
        try:
            # print("k=",k)
            url_main = cam.Streaming.channels[(k) * 100 + 1](method='get')
            # print("k=",k)
            videoCodecType_main = url_main["StreamingChannel"]["Video"]["videoCodecType"]
            videoResolutionWidth_main = url_main["StreamingChannel"]["Video"]["videoResolutionWidth"]
            videoResolutionHeight_main = url_main["StreamingChannel"]["Video"]["videoResolutionHeight"]
            videoQualityControlType_main = url_main["StreamingChannel"]["Video"]["videoQualityControlType"]
            SmartCodec_main = url_main["StreamingChannel"]["Video"]["SmartCodec"]["enabled"]
            vbrUpperCap_main = url_main["StreamingChannel"]["Video"]["vbrUpperCap"]
            maxFrameRate_main = url_main["StreamingChannel"]["Video"]["maxFrameRate"]

            url_md = cam.System.Video.inputs.channels[k].motionDetection(method='get')
            url_dtd = cam.System.Video.inputs.channels[k].overlays.dateTime(method='get')

            MotionDetection = url_md["MotionDetection"]["MotionDetectionLayout"]["sensitivityLevel"]
            enabled = url_md["MotionDetection"]["enabled"]
            enableHighlight = url_md["MotionDetection"]["enabled"]
            gridMap = url_md["MotionDetection"]["MotionDetectionLayout"]["layout"]["gridMap"]

            DateTimeOverlay = url_dtd["DateTimeOverlay"]["dateStyle"]

            url_rec = cam.ContentMgmt.record.tracks[(k) * 100 + 1](method='get')
            # print(url_rec)
            daysrec = []
            for fragmentid in range(7):
                fragment = url_rec["Track"]["TrackSchedule"]["ScheduleBlockList"]["ScheduleBlock"]["ScheduleAction"][
                    fragmentid]
                rec = fragment["ScheduleActionStartTime"], fragment["ScheduleActionEndTime"], fragment["Actions"][
                    "Record"], fragment["Actions"]["ActionRecordingMode"]
                daysrec.append(rec)

            url_sub = cam.Streaming.channels[(k) * 100 + 2](method='get')
            videoCodecType_sub = url_sub["StreamingChannel"]["Video"]["videoCodecType"]
            videoResolutionWidth_sub = url_sub["StreamingChannel"]["Video"]["videoResolutionWidth"]
            videoResolutionHeight_sub = url_sub["StreamingChannel"]["Video"]["videoResolutionHeight"]
            videoQualityControlType_sub = url_sub["StreamingChannel"]["Video"]["videoQualityControlType"]
            vbrUpperCap_sub = url_sub["StreamingChannel"]["Video"]["vbrUpperCap"]
            maxFrameRate_sub = url_sub["StreamingChannel"]["Video"]["maxFrameRate"]

        except:
            if videoCodecType_main == "":
                videoCodecType_sub = "не работает канал"
                videoResolutionWidth_sub = "не работает канал"
                videoResolutionHeight_sub = "не работает канал"
                videoQualityControlType_sub = "не работает канал"
                vbrUpperCap_sub = "не работает канал"
                maxFrameRate_sub = "не работает канал"
                videoCodecType_main = "не работает канал"
                videoResolutionWidth = "не работает канал"
                videoResolutionHeight_main = "не работает канал"
                videoQualityControlType_main = "не работает канал"
                SmartCodec_main = "не работает канал"
                vbrUpperCap_main = "не работает канал"
                maxFrameRate_main = "не работает канал"
                MotionDetection = "не работает канал"
                DateTimeOverlay = "не работает канал"
                videoResolutionWidth_main = "не работает канал"

        cam_name = url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["name"]
        cam_ipAddress = url_cam["InputProxyChannelList"]["InputProxyChannel"][i]["sourceInputPortDescriptor"][
            "ipAddress"]

        datereg = [[serv, deviceName, devicemodel, device_firmwareVersion, device_firmwareReleasedDate,
                    NTPServer, k, cam_name, cam_ipAddress, videoCodecType_main,
                    videoResolutionWidth_main, videoResolutionHeight_main, videoQualityControlType_main,
                    SmartCodec_main, vbrUpperCap_main, maxFrameRate_main, videoCodecType_sub, videoResolutionWidth_sub,
                    videoResolutionHeight_sub, videoQualityControlType_sub, vbrUpperCap_sub, maxFrameRate_sub, enabled,
                    enableHighlight, MotionDetection, gridMap,
                    DateTimeOverlay, ipAddress_1, subnetMask_1, addressingType_1, MACAddress_1,
                    ipAddress_2, subnetMask_2, addressingType_2, MACAddress_2, UserHik1,
                    daysrec[0], daysrec[1], daysrec[2], daysrec[3], daysrec[4], daysrec[5], daysrec[6]
                    ]]
    return datereg