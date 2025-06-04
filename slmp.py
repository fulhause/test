class SLMPMessage:
    """Very small placeholder implementation for SLMP messages."""

    def __init__(self, command: str, address: int, data: bytes):
        self.command = command
        self.address = address
        self.data = data

    def encode(self) -> bytes:
        # This is NOT a real SLMP implementation, just a placeholder for testing
        header = f"{self.command}:{self.address}:".encode()
        return header + self.data

    @classmethod
    def decode(cls, payload: bytes):
        # extremely naive decoding matching the encode above
        header, data = payload.split(b":", 2)[:2], payload.split(b":", 2)[2]
        command, address = header[0].decode(), int(header[1])
        return cls(command, address, data)
