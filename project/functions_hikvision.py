from hikvisionapi import Client


def reboot(serv, login, passw):
    cam = Client('http://'+serv, login, passw , timeout=30)
    cam.System.reboot(method='PUT')


