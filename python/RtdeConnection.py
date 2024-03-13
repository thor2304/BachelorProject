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

from rtde import rtde_config, rtde
from rtde.serialize import DataObject
from websockets.server import serve

from SocketMessages import RobotState

sys.path.append("..")

from RobotControl import POLYSCOPE_IP, get_socket

ROBOT_HOST = POLYSCOPE_IP
ROBOT_PORT = 30004
config_filename = "rtde_configuration.xml"

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe("state")

RTDE_WEBSOCKET_HOST = "0.0.0.0"
RTDE_WEBSOCKET_PORT = 8001

TRANSMIT_FREQUENCY_IN_HERTZ = 60
SLEEP_TIME = 1 / TRANSMIT_FREQUENCY_IN_HERTZ


async def start_rtde_server():
    print("Starting RTDE Websocket")
    async with serve(get_handler(), RTDE_WEBSOCKET_HOST, RTDE_WEBSOCKET_PORT):
        await asyncio.Future()  # run forever


def states_are_equal(obj1: DataObject, obj2: DataObject):
    return obj1.__dict__ == obj2.__dict__


def get_handler() -> callable:
    async def handler(websocket, path):
        # Connecting to RTDE interface
        con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        con.connect()
        # get controller version
        con.get_controller_version()
        # setup recipes
        con.send_output_setup(state_names, state_types)
        # start data synchronization
        if not con.send_start():
            sys.exit()

        # Set initial state
        initial_state = con.receive()
        old_robot_state = initial_state
        await websocket.send(str(RobotState(initial_state)))

        while True:
            await asyncio.sleep(SLEEP_TIME)
            state = con.receive()

            if states_are_equal(state, old_robot_state):
                continue

            old_robot_state = state
            robot_state = RobotState(state)
            await websocket.send(str(robot_state))

    return handler
