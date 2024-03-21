#!/usr/bin/env python
# Copyright (c) 2016-2022, Universal Robots A/S,
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Universal Robots A/S nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UNIVERSAL ROBOTS A/S BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import asyncio
import sys
from typing import Callable, Coroutine

from rtde import rtde_config, rtde
from rtde.serialize import DataObject
from websockets.server import serve, WebSocketServerProtocol

from RobotControl import POLYSCOPE_IP
from SocketMessages import RobotState
from undo.History import History
from undo.HistorySupport import create_state_from_rtde_state

ROBOT_HOST = POLYSCOPE_IP
ROBOT_PORT = 30004
config_filename = "rtde_configuration.xml"

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe("state")

RTDE_WEBSOCKET_HOST = "0.0.0.0"
RTDE_WEBSOCKET_PORT = 8001

TRANSMIT_FREQUENCY_IN_HERTZ = 60
SLEEP_TIME = 1 / TRANSMIT_FREQUENCY_IN_HERTZ

_ROBOT_STATE: DataObject | None = None

type ListenerFunction = Callable[[DataObject], Coroutine[None, None, None]]
listeners: list[ListenerFunction] = []


async def start_rtde_loop():
    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()
    # get controller version
    con.get_controller_version()
    # setup recipes
    con.send_output_setup(state_names, state_types)
    # start data synchronization
    if not con.send_start():
        sys.exit()

    global _ROBOT_STATE

    while True:
        await asyncio.sleep(SLEEP_TIME)
        try:
            _ROBOT_STATE = con.receive()
        except rtde.RTDEException as e:
            print(f"Error in recieve_rtde_data: {e}")


def states_are_equal(obj1: DataObject, obj2: DataObject):
    return obj1.__dict__ == obj2.__dict__


def get_handler() -> callable:
    async def handler(websocket: WebSocketServerProtocol):
        # Connecting to RTDE interface
        local_robot_state: DataObject | None = None

        async def send_state_through_websocket(state: DataObject):
            if state is None:
                return
            await websocket.send(str(RobotState(state)))

        register_listener(send_state_through_websocket)

        while True:
            await asyncio.sleep(SLEEP_TIME)

            if local_robot_state is None and _ROBOT_STATE is not None:
                local_robot_state = _ROBOT_STATE
                await call_listeners(_ROBOT_STATE)
                continue

            if local_robot_state is None and _ROBOT_STATE is None:
                continue

            if states_are_equal(local_robot_state, _ROBOT_STATE):
                continue

            local_robot_state = _ROBOT_STATE
            await call_listeners(_ROBOT_STATE)

    return handler


def register_listener(listener: ListenerFunction):
    listeners.append(listener)


async def log_state(state: DataObject):
    history = History.get_history()
    history.append_state(create_state_from_rtde_state(state))


register_listener(log_state)


async def call_listeners(with_state: DataObject):
    for listener in listeners:
        await listener(with_state)


async def start_RTDE_websocket():
    print("Starting RTDE Websocket")
    async with serve(get_handler(), RTDE_WEBSOCKET_HOST, RTDE_WEBSOCKET_PORT):
        await asyncio.Future()  # run forever
