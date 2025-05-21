# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ====================================================================================================
# Changed to work without Lerobot dependencies and to only control the Koch robot

import abc
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class MotorsBusConfig(abc.ABC):
    pass
    # @property
    # def type(self) -> str:
    #     return self.get_choice_name(self.__class__)


@dataclass
class DynamixelMotorsBusConfig(MotorsBusConfig):
    port: str
    motors: dict[str, tuple[int, str]]
    mock: bool = False

    @property
    def type(self) -> str:
        return "dynamixel"


@dataclass
class RobotConfig( abc.ABC):
    @property
    def type(self) -> str:
        return ""


# TODO(rcadene, aliberts): remove ManipulatorRobotConfig abstraction
@dataclass
class ManipulatorRobotConfig(RobotConfig):
    leader_arms: dict[str, MotorsBusConfig] = field(default_factory=lambda: {})
    follower_arms: dict[str, MotorsBusConfig] = field(default_factory=lambda: {})
    cameras: dict = field(default_factory=lambda: {})

    # Optionally limit the magnitude of the relative positional target vector for safety purposes.
    # Set this to a positive scalar to have the same value for all motors, or a list that is the same length
    # as the number of motors in your follower arms (assumes all follower arms have the same number of
    # motors).
    max_relative_target: list[float] | float | None = None

    # Optionally set the leader arm in torque mode with the gripper motor set to this angle. This makes it
    # possible to squeeze the gripper and have it spring back to an open position on its own. If None, the
    # gripper is not put in torque mode.
    gripper_open_degree: float | None = None

    mock: bool = False

    def __post_init__(self):
        if self.mock:
            for arm in self.leader_arms.values():
                if not arm.mock:
                    arm.mock = True
            for arm in self.follower_arms.values():
                if not arm.mock:
                    arm.mock = True
            for cam in self.cameras.values():
                if not cam.mock:
                    cam.mock = True

        if self.max_relative_target is not None and isinstance(self.max_relative_target, Sequence):
            for name in self.follower_arms:
                if len(self.follower_arms[name].motors) != len(self.max_relative_target):
                    raise ValueError(
                        f"len(max_relative_target)={len(self.max_relative_target)} but the follower arm with name {name} has "
                        f"{len(self.follower_arms[name].motors)} motors. Please make sure that the "
                        f"`max_relative_target` list has as many parameters as there are motors per arm. "
                        "Note: This feature does not yet work with robots where different follower arms have "
                        "different numbers of motors."
                    )





# @RobotConfig.register_subclass("koch")
@dataclass
class KochRobotConfig(ManipulatorRobotConfig):
    calibration_dir: str = ".cache/calibration/koch"
    # `max_relative_target` limits the magnitude of the relative positional target vector for safety purposes.
    # Set this to a positive scalar to have the same value for all motors, or a list that is the same length as
    # the number of motors in your follower arms.
    max_relative_target: int | None = None

    leader_arms: dict[str, MotorsBusConfig] = field(
        default_factory=lambda: {
            "main": DynamixelMotorsBusConfig(
                port="/dev/tty.usbmodem585A0085511",
                motors={
                    # name: (index, model)
                    "shoulder_pan": [1, "xl330-m077"],
                    "shoulder_lift": [2, "xl330-m077"],
                    "elbow_flex": [3, "xl330-m077"],
                    "wrist_flex": [4, "xl330-m077"],
                    "wrist_roll": [5, "xl330-m077"],
                    "gripper": [6, "xl330-m077"],
                },
            ),
        }
    )

    follower_arms: dict[str, MotorsBusConfig] = field(
        default_factory=lambda: {
            "main": DynamixelMotorsBusConfig(
                port="COM3",
                motors={
                    # name: (index, model)
                    "shoulder_pan": [1, "xl430-w250"],
                    "shoulder_lift": [2, "xl430-w250"],
                    "elbow_flex": [3, "xl330-m288"],
                    "wrist_flex": [4, "xl330-m288"],
                    "wrist_roll": [5, "xl330-m288"],
                    "gripper": [6, "xl330-m288"],
                },
            ),
        }
    )


    # ~ Koch specific settings ~
    # Sets the leader arm in torque mode with the gripper motor set to this angle. This makes it possible
    # to squeeze the gripper and have it spring back to an open position on its own.
    gripper_open_degree: float = 35.156

    mock: bool = False

    @property
    def type(self) -> str:
        return "koch"


# @RobotConfig.register_subclass("koch_bimanual")
# @dataclass
# class KochBimanualRobotConfig(ManipulatorRobotConfig):
#     calibration_dir: str = ".cache/calibration/koch_bimanual"
#     # `max_relative_target` limits the magnitude of the relative positional target vector for safety purposes.
#     # Set this to a positive scalar to have the same value for all motors, or a list that is the same length as
#     # the number of motors in your follower arms.
#     max_relative_target: int | None = None

#     leader_arms: dict[str, MotorsBusConfig] = field(
#         default_factory=lambda: {
#             "left": DynamixelMotorsBusConfig(
#                 port="/dev/tty.usbmodem585A0085511",
#                 motors={
#                     # name: (index, model)
#                     "shoulder_pan": [1, "xl330-m077"],
#                     "shoulder_lift": [2, "xl330-m077"],
#                     "elbow_flex": [3, "xl330-m077"],
#                     "wrist_flex": [4, "xl330-m077"],
#                     "wrist_roll": [5, "xl330-m077"],
#                     "gripper": [6, "xl330-m077"],
#                 },
#             ),
#             "right": DynamixelMotorsBusConfig(
#                 port="/dev/tty.usbmodem575E0031751",
#                 motors={
#                     # name: (index, model)
#                     "shoulder_pan": [1, "xl330-m077"],
#                     "shoulder_lift": [2, "xl330-m077"],
#                     "elbow_flex": [3, "xl330-m077"],
#                     "wrist_flex": [4, "xl330-m077"],
#                     "wrist_roll": [5, "xl330-m077"],
#                     "gripper": [6, "xl330-m077"],
#                 },
#             ),
#         }
#     )

#     follower_arms: dict[str, MotorsBusConfig] = field(
#         default_factory=lambda: {
#             "left": DynamixelMotorsBusConfig(
#                 port="/dev/tty.usbmodem585A0076891",
#                 motors={
#                     # name: (index, model)
#                     "shoulder_pan": [1, "xl430-w250"],
#                     "shoulder_lift": [2, "xl430-w250"],
#                     "elbow_flex": [3, "xl330-m288"],
#                     "wrist_flex": [4, "xl330-m288"],
#                     "wrist_roll": [5, "xl330-m288"],
#                     "gripper": [6, "xl330-m288"],
#                 },
#             ),
#             "right": DynamixelMotorsBusConfig(
#                 port="/dev/tty.usbmodem575E0032081",
#                 motors={
#                     # name: (index, model)
#                     "shoulder_pan": [1, "xl430-w250"],
#                     "shoulder_lift": [2, "xl430-w250"],
#                     "elbow_flex": [3, "xl330-m288"],
#                     "wrist_flex": [4, "xl330-m288"],
#                     "wrist_roll": [5, "xl330-m288"],
#                     "gripper": [6, "xl330-m288"],
#                 },
#             ),
#         }
#     )

#     # ~ Koch specific settings ~
#     # Sets the leader arm in torque mode with the gripper motor set to this angle. This makes it possible
#     # to squeeze the gripper and have it spring back to an open position on its own.
#     gripper_open_degree: float = 35.156

#     mock: bool = False


