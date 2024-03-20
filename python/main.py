import asyncio

from RtdeConnection import start_rtde_loop, start_RTDE_websocket
from WebsocketProxy import open_robot_server, start_webserver
from PopupReader import start_primary_reader


async def main():
    print("Starting WebsocketProxy.py")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(open_robot_server())
        t2 = tg.create_task(start_webserver())
        t3 = tg.create_task(start_rtde_loop())
        t4 = tg.create_task(start_RTDE_websocket())
        t5 = tg.create_task(start_primary_reader())
    pass


if __name__ == '__main__':
    asyncio.run(main())
