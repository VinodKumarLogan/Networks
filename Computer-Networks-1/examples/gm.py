import socket , ssl , base64
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('smtp.gmail.com',587))
clientSocket.send('ehlo \r\n')
clientSocket.send('starttls \r\n')
ssl_clientSocket = ssl.wrap_socket(clientSocket,ca_certs="/etc/ssl/certs/ca.pem",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_clientSocket.send('auth login \r\n')
