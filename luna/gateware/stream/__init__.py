#
# This file is part of LUNA.
#
""" Core stream definitions. """

from nmigen         import Elaboratable, Signal, Module
from nmigen.hdl.rec import Record, DIR_FANIN, DIR_FANOUT


class StreamInterface(Record):
    """ Simple record implementing a unidirectional data stream.

    This class is similar to LiteX's streams; but instances may be optimized for
    interaction with USB PHYs. Accordingly, some uses may add restrictions; this
    is typically indicated by subclassing this interface.

    In the following signals list, 'T' indicates a signal driven by the sender;
    and 'R' indicates a signal driven by the receiver.

    Signals:
        T: valid      -- Indicates that an active transaction is underway
        T: first      -- Indicates that the payload byte is the first byte of a new packet.
        T: last       -- Indicates that the payload byte is the last byte of the current packet.
        T: payload[]  -- The data payload to be transmitted.

        R: ready      -- Indicates that the receiver will accept the payload byte at the next active
                         clock edge. Can be de-asserted to slew the transmitter.
    """


    def __init__(self, payload_width=8):
        """
        Parameter:
            payload_width -- The width of the payload packets.
        """
        super().__init__([
            ('valid',    1),
            ('ready',    1),

            ('first',    1),
            ('last',     1),

            ('payload',  payload_width),
        ])


    def attach(self, interface):
        return [
            interface.valid    .eq(self.valid),
            interface.first    .eq(self.first),
            interface.last     .eq(self.last),
            interface.payload  .eq(self.payload),

            self.ready         .eq(interface.ready)
        ]


    def connect(self, interface):
        return interface.attach(self)
