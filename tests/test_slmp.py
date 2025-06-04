from slmp import SLMPMessage


def test_slmp_encode_decode_roundtrip():
    msg = SLMPMessage(command="RD", address=0x100, data=b"abc")
    encoded = msg.encode()
    decoded = SLMPMessage.decode(encoded)

    assert decoded.command == msg.command
    assert decoded.address == msg.address
    assert decoded.data == msg.data
