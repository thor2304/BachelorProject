from RobotControl import send_command, get_interpreter_socket, send_user_command
from socket import socket as Socket


def test():
    socket: Socket = get_interpreter_socket()

    # Thread move kill
    # commands = [
    #     'thread myThread(): movej([0,1,0,0,0,0], a=0.1, v=0.1) return False end',
    #     'thrd = run myThread()',
    #     'sleep(1)'
    #     # 'kill thrd'
    # ]

    # Thread exception
    # commands = [
    #     'thread myThread(): a=[0,0] b=a[2] return False end',
    #     'thrd = run myThread()'
    # ]

    # Secondary program
    commands = [
        'sec secondaryProgram(): set_digital_out(1,True) end',
        'secp = run secondaryProgram()',
        'movej([0,0,0,0,0,0], a=0.1, v=0.1)'
    ]

    for command in commands:
        send_command(command, socket)

if __name__ == '__main__':
    test()