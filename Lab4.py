import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 11005

s.bind(("localhost",port))
s.listen(5)

print("Socket is listening")

while True:
    client, address = s.accept()
    elements = {}
    enders = []
    req = client.recv(4096)
    print(req)
    tempreq = req
    # print(req)
    req = req.decode().split('\n')
    temp_counter = 0
    for i in req:
        if temp_counter == 0:
            elements['first_line'] = i
            temp_counter+=1
            continue
        tmp = i.split(': ')
        if len(tmp) < 2:
            enders.append(i)
            continue
        elements[tmp[0]] = tmp[1]
    # print(f"elements are \n{elements}\nthe enders are:\n{enders}")
    try:
        web_server = elements['Host'].split('\r')[0]
    except:
        continue
    if ':' in web_server:
        portNo = int(web_server.split(':')[1])
        web_server = web_server.split(':')[0]
    # elif ':' in elements['first_line']:
    #     portNo = elements['first_line'].split(':')[1]
    else:
        if elements['first_line'].split(' ')[1].startswith('https'):
            portNo = 443
        else:
            portNo = 80

    # if 'Connection' in elements:
    #     elements['Connection'] = 'close'
    # if 'Proxy-Connection' in elements:
    #     elements['Proxy-Connection'] = 'close'

    tmp = elements['first_line'].split(' ')
    tmp[2] = 'HTTP/1.0'
    elements['first_line'] = " ".join(tmp)

    # print(f'\n\n\n Port no is : {portNo}\n')

    # print(f"\nWeb Server is {web_server} and port no is {portNo}\n")
    request = ''
    tmp_flag = 0
    for key in elements:
        if tmp_flag == 0:
            tmp_flag = 1
            request += elements['first_line']+'\r\n'
            continue
        request += key+': '+elements[key]+'\n'
    request += '\r\n'

    # print(f"Modified request is: \n {request.encode()}")
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((web_server,portNo))
    # s2.sendall(request.encode())
    s2.sendall(request.encode())
    # print("here")
    print(f"\n{request.encode()}\n")
        
    while True:
        data = s2.recv(4096)
        if len(data)>0:
            client.send(data)
        else:
            break
    s2.close()

    









