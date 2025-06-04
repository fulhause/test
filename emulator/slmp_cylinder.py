"""SLMP communication routines and cylinder data structures."""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from typing import List, Tuple


# Constants for SLMP
SLMP_SUBHEADER = 0x5000
DEFAULT_NETWORK = 0x00
DEFAULT_PC = 0xFF
DEFAULT_IO = 0x03FF
DEFAULT_STATION = 0x00
DEFAULT_TIMEOUT = 5.0


@dataclass
class SLMPFrame:
    """Represents a minimal SLMP frame."""

    command: int
    subcommand: int = 0x0000
    data: bytes = b""

    def encode(self) -> bytes:
        data_len = 2 + 2 + len(self.data)
        header = SLMP_SUBHEADER.to_bytes(2, "little")
        header += bytes(
            [
                DEFAULT_NETWORK,
                DEFAULT_PC,
                DEFAULT_IO & 0xFF,
                (DEFAULT_IO >> 8) & 0xFF,
                DEFAULT_STATION,
            ]
        )
        header += data_len.to_bytes(2, "little")
        header += (1000).to_bytes(2, "little")
        header += self.command.to_bytes(2, "little")
        header += self.subcommand.to_bytes(2, "little")
        return header + self.data


class SLMPClient:
    """Simple SLMP TCP client."""

    def __init__(self, host: str, port: int = 5000, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock: socket.socket | None = None

    def connect(self) -> None:
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def close(self) -> None:
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_frame(self, frame: SLMPFrame) -> bytes:
        if not self.sock:
            raise RuntimeError("Not connected")
        self.sock.sendall(frame.encode())
        return self.sock.recv(4096)


@dataclass
class Cylinder:
    """Base class for cylinders."""

    stroke_length: float
    speed: float
    position: float = 0.0

    def step(self, delta: float) -> None:
        raise NotImplementedError

    @property
    def two_position_signal(self) -> Tuple[bool, bool]:
        raise NotImplementedError


@dataclass
class TwoPositionCylinder(Cylinder):
    """Simple two-position cylinder."""

    extended: bool = False

    def step(self, delta: float) -> None:
        target = self.stroke_length if self.extended else 0.0
        if self.position < target:
            self.position = min(self.position + self.speed * delta, target)
        else:
            self.position = max(self.position - self.speed * delta, target)

    @property
    def two_position_signal(self) -> Tuple[bool, bool]:
        return (self.position <= 0.0, self.position >= self.stroke_length)


@dataclass
class ThreePositionCylinder(Cylinder):
    """Cylinder with a middle position."""

    middle_position: float = field(default=0.0)
    state: int = 0  # 0=retracted,1=middle,2=extended

    def step(self, delta: float) -> None:
        targets = [0.0, self.middle_position, self.stroke_length]
        target = targets[self.state]
        if self.position < target:
            self.position = min(self.position + self.speed * delta, target)
        else:
            self.position = max(self.position - self.speed * delta, target)

    @property
    def two_position_signal(self) -> Tuple[bool, bool]:
        return (self.position <= 0.0, self.position >= self.stroke_length)


class CylinderEmulator:
    """Emulates multiple cylinders and provides SLMP communication."""

    def __init__(self, cylinders: List[Cylinder]) -> None:
        self.cylinders = cylinders
        self.client: SLMPClient | None = None

    def connect(self, host: str, port: int = 5000) -> None:
        self.client = SLMPClient(host, port)
        self.client.connect()

    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            self.client = None

    def step_all(self, delta: float) -> None:
        for cyl in self.cylinders:
            cyl.step(delta)

    def read_signals(self) -> List[Tuple[bool, bool]]:
        return [cyl.two_position_signal for cyl in self.cylinders]

    def send_signals(self) -> None:
        if not self.client:
            return
        signals = b"".join(
            b"\x01" if s else b"\x00" for pair in self.read_signals() for s in pair
        )
        frame = SLMPFrame(command=0x1401, data=signals)
        self.client.send_frame(frame)
