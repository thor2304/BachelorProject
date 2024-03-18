import asyncio

from RtdeConnection import start_rtde_loop, start_RTDE_websocket
from WebsocketProxy import open_robot_server, start_webserver


async def main():
    print("Starting WebsocketProxy.py")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(open_robot_server())
        t2 = tg.create_task(start_webserver())
        t3 = tg.create_task(start_rtde_loop())
        t4 = tg.create_task(start_RTDE_websocket())
    pass


if __name__ == '__main__':
    asyncio.run(main())
