import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
import socket

host = "84.237.21.36"
port = 5151

def recvall(sock, nbytes):
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    print(sock.recv(10))

    sock.send(b'get')
    bts = recvall(sock, 80004)
    print(len(bts))
    beat = b'nope'

    while beat != b'yep':

        iml = np.frombuffer(bts[2:40002], dtype = "uint8")
        iml = iml.reshape(bts[0], bts[1])
        im2 = np.frombuffer(bts[40004:], dtype = "uint8")
        im2 = im2.reshape(bts[40002], bts[40003])

        pos1 = np.unravel_index(np.argmax(iml), iml.shape)
        pos2 = np.unravel_index(np.argmax(im2), im2.shape)
        result = np.abs(np.array(pos1) - np.array(pos2))
        sock.send(f'{result[0]} {result[1]}'.encode())
        print("res:", sock.recv(10))

        plt.clf()
        plt.subplot(121)
        plt.imshow(iml)
        plt.subplot(122)
        plt.imshow(im2)
        plt.pause(4)

        sock.send(b'beat')
        beat = sock.recv(10)




# plt.subplot(121)
# plt.imshow(image)
# plt.show()