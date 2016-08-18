import socket
"""
Bare bones controller for AR Drone 2
Based of code by Micah Sheer
https://security.cs.georgetown.edu/courses/cosc235-fall2014/hws/ad-controller.py
"""


class ArDrone:
    """
    ArDrone class implements control functions for AR Drone 2
    """

    def __init__(self):
        self._seqno = 1
        self._address = ('192.168.1.1', 5556)

        # Create socket to talk to ardrone on control port 5556
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(self._address)

    def _send_command(self, cmd):
        print('INFO: Sending: {}'.format(cmd.strip()))
        self.s.sendto(cmd, self._address)
        self._seqno += 1

    def _set_bits(lst):
        res = 0
        for b in lst + [18, 20, 22, 24, 28]:
            res |= (1 << b)
        return res

    def reset(self):
        self._seqno = 1
        self._send_command("AT*FTRIM=%d\r" % self._seqno)

    def takeoff(self):
        self._send_command("AT*FTRIM=%d\r" % self._seqno)
        takeoff_cmd = self._set_bits([9])
        for i in xrange(1, 25):
            self._send_command("AT*REF=%d,%d\r" % (self._seqno, takeoff_cmd))

    def land(self):
        land_cmd = self._set_bits([])
        for i in xrange(1, 25):
            self._send_command("AT*REF=%d,%d\r" % (self._seqno, land_cmd))

    def emergency(self):
        shutdown_cmd = self._set_bits([8])
        self._send_command("AT*REF=%d,%d\r" % (self._seqno, shutdown_cmd))
