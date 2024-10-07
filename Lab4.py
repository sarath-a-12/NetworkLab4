import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 11001

s.bind(("localhost",port))
s.listen(5)

print("Socket is listening")

while True:
    client, address = s.accept()
    elements = {}
    enders = []
    req = client.recv(1024).decode().split('\n')
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
        elements[tmp[0].lower()] = tmp[1]
    # print(f"elements are \n{elements}\nthe enders are:\n{enders}")
    try:
        web_server = elements['host'].split('\r')[0]
    except:
        continue
    if ':' in web_server:
        portNo = web_server.split(':')[1]
    elif ':' in elements['first_line']:
        portNo = elements['first_line'].split(':')[1]
    else:
        if elements['first_line'].split(' ')[1].startswith('https'):
            portNo = 443
        else:
            portNo = 80

    if 'connection' in elements:
        elements['connection'] = 'close'
    if 'proxy-connection' in elements:
        elements['proxy-connection'] = 'close'

    tmp = elements['first_line'].split(' ')
    tmp[2] = 'HTTP/1.0'
    elements['first_line'] = " ".join(tmp)

    print(f'\n\n\n Port no is : {portNo}\n')
    for key in elements:
        print(f'{key} : {elements[key]}')

        

    

