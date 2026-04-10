import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.measure import label
import socket

host = "84.237.21.36"
port = 5152

def recvall(sock, nbytes):
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def distance(image):
    x1, y1 = ndimage.center_of_mass(image==1)
    x2, y2 = ndimage.center_of_mass(image==2)
    dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return round(dist, 1)

plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    print(sock.recv(10))

    for _ in range(10):
        sock.send(b"get")
        bts = recvall(sock, 40002)
        im1 = np.frombuffer(bts[2:40002], dtype="uint8")
        im1 = im1.reshape(bts[0], bts[1])
        objs = label(im1 > 160)

        sock.send(str(distance(objs)).encode())
        print(sock.recv(10), "Distance =", str(distance(objs)))

        sock.send(b"beat")
        beat = sock.recv(10)

        plt.clf()
        plt.imshow(objs)
        plt.show()