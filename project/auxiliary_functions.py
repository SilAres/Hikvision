

def list_of_servers():
    """
    Получение списка ip адресов? ,без проверки на валидность из ../date/hikvision.txt

    """
    servers = []
    try:
        servers = []
        file1 = open("../date/hikvision.txt", "r")

        while True:
            line = file1.readline()
            if not line:
                break
            servers.append(line.strip())
            # print(line.strip()) # вывод серверов
    except :
            pass
    return servers
