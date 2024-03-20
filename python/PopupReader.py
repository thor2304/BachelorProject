import asyncio
import struct

from RobotControl import get_socket, POLYSCOPE_IP

PRIMARY_PORT = 30001

packageHeaderFmt = '!iB'


async def start_primary_reader():
    primary_socket = get_socket(POLYSCOPE_IP, PRIMARY_PORT)
    print(f"Connected to primary socket: {primary_socket}")
    print(f"Starting primary reader")

    while True:
        data = primary_socket.recv(4096*4)
        if data:
            i = 0

            # extract packet length, timestamp and packet type from start of packet and print to screen
            (length, type_) = struct.unpack(packageHeaderFmt, data[i:i + 5])
            assert i + length <= len(data), '{}+{}<={}'.format(i, length, len(data))
            print(f"Received from primary socket with length {length} and type {type_}")

            if type_ == 16:
                print(f"Received Robot State Package with length {length}")
            elif type_ == 20:
                print(f"Received Robot Message with length {length}")
                timestamp = (struct.unpack('!Q', data[5:13]))[0]
                source = (struct.unpack('!b', data[13:14]))[0]
                robotMessageType = (struct.unpack('!b', data[14:15]))[0]
                print(f"Timestamp: {timestamp}, Source: {source}, RobotMessageType: {robotMessageType}")

            # print(f"Received data: {my_data}")
            # print(f"Lenght: {length}, Type: {type_}, Data: {my_data}")

        # if data:
        #     # Print title to screen
        #     print('*******')
        #     print('UR Controller Primary Client Interface Reader')
        #     print('*******')
        #     # extract packet length, timestamp and packet type from start of packet and print to screen
        #     (packlen, packtype) = struct.unpack(packageHeaderFmt, data[i:i + 5])
        #     timestamp = (struct.unpack('!Q', data[10:18]))[0]
        #     print('packet length: ' + str(packlen))
        #     print('timestamp: ' + str(timestamp))
        #     print('packet type: ' + str(packtype))
        #     print('*******')
        #
        #     if packtype == 16:
        #         # if packet type is Robot State, loop until reached end of packet
        #         while i + 5 < packlen:
        #
        #             # extract length and type of message and print if desired
        #             msglen = (struct.unpack('!i', data[5 + i:9 + i]))[0]
        #             msgtype = (struct.unpack('!b', data[9 + i]))[0]
        #
        #             print('packet length: ' + str(msglen))
        #             print('message type: ' + str(msgtype))
        #             print('*******')
        #
        #             if msgtype == 1:
        #                 # if message is joint data, create a list to store angles
        #                 angle = [0] * 6
        #                 j = 0
        #                 while j < 6:
        #                     # cycle through joints and extract only current joint angle (double precision)  then print to screen
        #                     # bytes 10 to 18 contain the j0 angle, each joint's data is 41 bytes long (so we skip j*41 each time)
        #                     angle[j] = (struct.unpack('!d', data[10 + i + (j * 41):18 + i + (j * 41)]))[0]
        #                     print('Joint ' + str(j) + ' angle : ' + str(angle[j]))
        #                     j = j + 1
        #
        #                 print('*******')




        await asyncio.sleep(1)



