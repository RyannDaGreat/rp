#OSC stands for Open Sound Control. It works with software synths like Reactor. This is a test file for it.
Đ_OSC_ip='192.168.1.104'
Đ_OSC_port=12345
#
_OSC_client=None  # This is a singleton
_OSC_values={}
def OSC_output(address,value):
    address=str(address)
    if not address[0] == '/':
        address='/' + address
    global Đ_OSC_ip
    global _OSC_client
    if not _OSC_client:
        _OSC_client=SimpleUDPClient(address=Đ_OSC_ip,port=Đ_OSC_port)
    _OSC_client.send_message(address=address,value=value)
    _OSC_values[address]=value  # Attempt to keep track of them (though it might sometimes drift out of sync etc idk i haven't tested it as of writing this)
def OSC_jiggle(address):
    address=str(address)
    if address in _OSC_values:
        original_value=_OSC_values[address]
    from time import sleep
    OSC_output(address,1)
    sleep(.1)
    OSC_output(address,0)
    sleep(.1)
    if address in _OSC_values:
        # noinspection PyUnboundLocalVariable
        OSC_output(address,original_value)
# Less abstract things lie below...
# Less abstract things lie below...
# Less abstract things lie below...
# Less abstract things lie below...
# Less abstract things lie below...
"""Client to send OSC datagrams to an OSC server via UDP."""
from collections import Iterable
import socket

"""Build OSC messages for client applications."""

"""Functions to get OSC types from datagrams and vice versa"""

import decimal
import struct

"""Parsing and conversion of NTP dates contained in datagrams."""

import datetime
import struct
import time
"""Representation of an OSC message in a pythonesque way."""

import logging

class ParseError(Exception):
    """Base exception raised when a datagram parsing error occurs."""

class OscMessage(object):
    """Representation of a parsed datagram representing an OSC message.

    An OSC message consists of an OSC Address Pattern followed by an OSC
    Type Tag String followed by zero or more OSC Arguments.
    """

    def __init__(self,dgram):
        self._dgram=dgram
        self._parameters=[]
        self._parse_datagram()

    def _parse_datagram(self):
        try:
            self._address_regexp,index=get_string(self._dgram,0)
            if not self._dgram[index:]:
                # No params is legit, just return now.
                return

            # Get the parameters types.
            type_tag,index=get_string(self._dgram,index)
            if type_tag.startswith(','):
                type_tag=type_tag[1:]

            # Parse each parameter given its type.
            for param in type_tag:
                if param == "i":  # Integer.
                    val,index=get_int(self._dgram,index)
                elif param == "f":  # Float.
                    val,index=get_float(self._dgram,index)
                elif param == "s":  # String.
                    val,index=get_string(self._dgram,index)
                elif param == "b":  # Blob.
                    val,index=get_blob(self._dgram,index)
                elif param == "r":  # RGBA.
                    val,index=get_rgba(self._dgram,index)
                elif param == "T":  # True.
                    val=True
                elif param == "F":  # False.
                    val=False
                # TODO: Support more exotic types as described in the specification.
                else:
                    logging.warning('Unhandled parameter type: {0}'.format(param))
                    continue
                self._parameters.append(val)
        except ParseError as pe:
            raise ParseError('Found incorrect datagram, ignoring it',pe)

    @property
    def address(self):
        """Returns the OSC address regular expression."""
        return self._address_regexp

    @staticmethod
    def dgram_is_message(dgram):
        """Returns whether this datagram starts as an OSC message."""
        return dgram.startswith(b'/')

    @property
    def size(self):
        """Returns the length of the datagram for this message."""
        return len(self._dgram)

    @property
    def dgram(self):
        """Returns the datagram from which this message was built."""
        return self._dgram

    @property
    def params(self):
        """Convenience method for list(self) to get the list of parameters."""
        return list(self)

    def __iter__(self):
        """Returns an iterator over the parameters of this message."""
        return iter(self._parameters)

# conversion factor for fractional seconds (maximum value of fractional part)
FRACTIONAL_CONVERSION=2 ** 32

# 63 zero bits followed by a one in the least signifigant bit is a special
# case meaning "immediately."
IMMEDIATELY=struct.pack('>q',1)

# From NTP lib.
_SYSTEM_EPOCH=datetime.date(*time.gmtime(0)[0:3])
_NTP_EPOCH=datetime.date(1900,1,1)
# _NTP_DELTA is 2208988800
_NTP_DELTA=(_SYSTEM_EPOCH - _NTP_EPOCH).days * 24 * 3600

class NtpError(Exception):
    """Base class for ntp module errors."""

def ntp_to_system_time(date):
    """Convert a NTP time to system time.

    System time is reprensented by seconds since the epoch in UTC.
    """
    return date - _NTP_DELTA

def system_time_to_ntp(date):
    """Convert a system time to NTP time.

    System time is reprensented by seconds since the epoch in UTC.
    """
    try:
        num_secs=int(date)
    except ValueError as e:
        raise NtpError(e)

    num_secs_ntp=num_secs + _NTP_DELTA

    sec_frac=float(date - num_secs)

    picos=int(sec_frac * FRACTIONAL_CONVERSION)

    return struct.pack('>I',int(num_secs_ntp)) + struct.pack('>I',picos)

class ParseError(Exception):
    """Base exception for when a datagram parsing error occurs."""

class BuildError(Exception):
    """Base exception for when a datagram building error occurs."""

# Constant for special ntp datagram sequences that represent an immediate time.
IMMEDIATELY=0

# Datagram length in bytes for types that have a fixed size.
_INT_DGRAM_LEN=4
_FLOAT_DGRAM_LEN=4
_DATE_DGRAM_LEN=_INT_DGRAM_LEN * 2
# Strings and blob dgram length is always a multiple of 4 bytes.
_STRING_DGRAM_PAD=4
_BLOB_DGRAM_PAD=4

def write_string(val):
    """Returns the OSC string equivalent of the given python string.

    Raises:
      - BuildError if the string could not be encoded.
    """
    try:
        dgram=val.encode('utf-8')  # Default, but better be explicit.
    except (UnicodeEncodeError,AttributeError) as e:
        raise BuildError('Incorrect string, could not encode {}'.format(e))
    diff=_STRING_DGRAM_PAD - (len(dgram) % _STRING_DGRAM_PAD)
    dgram+=(b'\x00' * diff)
    return dgram

def get_string(dgram,start_index):
    """Get a python string from the datagram, starting at pos start_index.

    According to the specifications, a string is:
    "A sequence of non-null ASCII characters followed by a null,
    followed by 0-3 additional null characters to make the total number
    of bits a multiple of 32".

    Args:
      dgram: A datagram packet.
      start_index: An index where the string starts in the datagram.

    Returns:
      A tuple containing the string and the new end index.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    offset=0
    try:
        while dgram[start_index + offset] != 0:
            offset+=1
        if offset == 0:
            raise ParseError(
                'OSC string cannot begin with a null byte: %s' % dgram[start_index:])
        # Align to a byte word.
        if (offset) % _STRING_DGRAM_PAD == 0:
            offset+=_STRING_DGRAM_PAD
        else:
            offset+=(-offset % _STRING_DGRAM_PAD)
        # Python slices do not raise an IndexError past the last index,
        # do it ourselves.
        if offset > len(dgram[start_index:]):
            raise ParseError('Datagram is too short')
        data_str=dgram[start_index:start_index + offset]
        return data_str.replace(b'\x00',b'').decode('utf-8'),start_index + offset
    except IndexError as ie:
        raise ParseError('Could not parse datagram %s' % ie)
    except TypeError as te:
        raise ParseError('Could not parse datagram %s' % te)

def write_int(val):
    """Returns the datagram for the given integer parameter value

    Raises:
      - BuildError if the int could not be converted.
    """
    try:
        return struct.pack('>i',val)
    except struct.error as e:
        raise BuildError('Wrong argument value passed: {}'.format(e))

def get_int(dgram,start_index):
    """Get a 32-bit big-endian two's complement integer from the datagram.

    Args:
      dgram: A datagram packet.
      start_index: An index where the integer starts in the datagram.

    Returns:
      A tuple containing the integer and the new end index.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    try:
        if len(dgram[start_index:]) < _INT_DGRAM_LEN:
            raise ParseError('Datagram is too short')
        return (
            struct.unpack('>i',
                          dgram[start_index:start_index + _INT_DGRAM_LEN])[0],
            start_index + _INT_DGRAM_LEN)
    except (struct.error,TypeError) as e:
        raise ParseError('Could not parse datagram %s' % e)

def write_float(val):
    """Returns the datagram for the given float parameter value

    Raises:
      - BuildError if the float could not be converted.
    """
    try:
        return struct.pack('>f',val)
    except struct.error as e:
        raise BuildError('Wrong argument value passed: {}'.format(e))

def get_float(dgram,start_index):
    """Get a 32-bit big-endian IEEE 754 floating point number from the datagram.

    Args:
      dgram: A datagram packet.
      start_index: An index where the float starts in the datagram.

    Returns:
      A tuple containing the float and the new end index.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    try:
        if len(dgram[start_index:]) < _FLOAT_DGRAM_LEN:
            # Noticed that Reaktor doesn't send the last bunch of \x00 needed to make
            # the float representation complete in some cases, thus we pad here to
            # account for that.
            dgram=dgram + b'\x00' * (_FLOAT_DGRAM_LEN - len(dgram[start_index:]))
        return (
            struct.unpack('>f',
                          dgram[start_index:start_index + _FLOAT_DGRAM_LEN])[0],
            start_index + _FLOAT_DGRAM_LEN)
    except (struct.error,TypeError) as e:
        raise ParseError('Could not parse datagram %s' % e)

def get_blob(dgram,start_index):
    """ Get a blob from the datagram.

    According to the specifications, a blob is made of
    "an int32 size count, followed by that many 8-bit bytes of arbitrary
    binary data, followed by 0-3 additional zero bytes to make the total
    number of bits a multiple of 32".

    Args:
      dgram: A datagram packet.
      start_index: An index where the float starts in the datagram.

    Returns:
      A tuple containing the blob and the new end index.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    size,int_offset=get_int(dgram,start_index)
    # Make the size a multiple of 32 bits.
    total_size=size + (-size % _BLOB_DGRAM_PAD)
    end_index=int_offset + size
    if end_index - start_index > len(dgram[start_index:]):
        raise ParseError('Datagram is too short.')
    return dgram[int_offset:int_offset + size],int_offset + total_size

def write_blob(val):
    """Returns the datagram for the given blob parameter value.

    Raises:
      - BuildError if the value was empty or if its size didn't fit an OSC int.
    """
    if not val:
        raise BuildError('Blob value cannot be empty')
    dgram=write_int(len(val))
    dgram+=val
    while len(dgram) % _BLOB_DGRAM_PAD != 0:
        dgram+=b'\x00'
    return dgram

def get_date(dgram,start_index):
    """Get a 64-bit big-endian fixed-point time tag as a date from the datagram.

    According to the specifications, a date is represented as is:
    "the first 32 bits specify the number of seconds since midnight on
    January 1, 1900, and the last 32 bits specify fractional parts of a second
    to a precision of about 200 picoseconds".

    Args:
      dgram: A datagram packet.
      start_index: An index where the date starts in the datagram.

    Returns:
      A tuple containing the system date and the new end index.
      returns osc_immediately (0) if the corresponding OSC sequence was found.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    # Check for the special case first.
    if dgram[start_index:start_index + _DATE_DGRAM_LEN] == IMMEDIATELY:
        return IMMEDIATELY,start_index + _DATE_DGRAM_LEN
    if len(dgram[start_index:]) < _DATE_DGRAM_LEN:
        raise ParseError('Datagram is too short')
    num_secs,start_index=get_int(dgram,start_index)
    fraction,start_index=get_int(dgram,start_index)
    # Sum seconds and fraction of second:
    system_time=num_secs + (fraction / FRACTIONAL_CONVERSION)
    return ntp_to_system_time(system_time),start_index

def write_date(system_time):
    if system_time == IMMEDIATELY:
        return IMMEDIATELY

    try:
        return system_time_to_ntp(system_time)
    except NtpError as ntpe:
        raise BuildError(ntpe)

def write_rgba(val):
    """Returns the datagram for the given rgba32 parameter value

    Raises:
      - BuildError if the int could not be converted.
    """
    try:
        return struct.pack('>I',val)
    except struct.error as e:
        raise BuildError('Wrong argument value passed: {}'.format(e))

def get_rgba(dgram,start_index):
    """Get an rgba32 integer from the datagram.

    Args:
      dgram: A datagram packet.
      start_index: An index where the integer starts in the datagram.

    Returns:
      A tuple containing the integer and the new end index.

    Raises:
      ParseError if the datagram could not be parsed.
    """
    try:
        if len(dgram[start_index:]) < _INT_DGRAM_LEN:
            raise ParseError('Datagram is too short')
        return (
            struct.unpack('>I',
                          dgram[start_index:start_index + _INT_DGRAM_LEN])[0],
            start_index + _INT_DGRAM_LEN)
    except (struct.error,TypeError) as e:
        raise ParseError('Could not parse datagram %s' % e)

class BuildError(Exception):
    """Error raised when an incomplete message is trying to be built."""

class OscMessageBuilder(object):
    """Builds arbitrary OscMessage instances."""

    ARG_TYPE_FLOAT="f"
    ARG_TYPE_INT="i"
    ARG_TYPE_STRING="s"
    ARG_TYPE_BLOB="b"
    ARG_TYPE_RGBA="r"
    ARG_TYPE_TRUE="T"
    ARG_TYPE_FALSE="F"

    _SUPPORTED_ARG_TYPES=(
        ARG_TYPE_FLOAT,ARG_TYPE_INT,ARG_TYPE_BLOB,ARG_TYPE_STRING,ARG_TYPE_RGBA,ARG_TYPE_TRUE,ARG_TYPE_FALSE)

    def __init__(self,address=None):
        """Initialize a new builder for a message.

        Args:
          - address: The osc address to send this message to.
        """
        self._address=address
        self._args=[]

    @property
    def address(self):
        """Returns the OSC address this message will be sent to."""
        return self._address

    @address.setter
    def address(self,value):
        """Sets the OSC address this message will be sent to."""
        self._address=value

    @property
    def args(self):
        """Returns the (type, value) arguments list of this message."""
        return self._args

    def add_arg(self,arg_value,arg_type=None):
        """Add a typed argument to this message.

        Args:
          - arg_value: The corresponding value for the argument.
          - arg_type: A value in ARG_TYPE_* defined in this class,
                      if none then the type will be guessed.
        Raises:
          - ValueError: if the type is not supported.
        """
        if arg_type and arg_type not in self._SUPPORTED_ARG_TYPES:
            raise ValueError(
                'arg_type must be one of {}'.format(self._SUPPORTED_ARG_TYPES))
        if not arg_type:
            if isinstance(arg_value,str):
                arg_type=self.ARG_TYPE_STRING
            elif isinstance(arg_value,bytes):
                arg_type=self.ARG_TYPE_BLOB
            elif isinstance(arg_value,int):
                arg_type=self.ARG_TYPE_INT
            elif isinstance(arg_value,float):
                arg_type=self.ARG_TYPE_FLOAT
            elif arg_value == True:
                arg_type=self.ARG_TYPE_TRUE
            elif arg_value == False:
                arg_type=self.ARG_TYPE_FALSE
            else:
                raise ValueError('Infered arg_value type is not supported')
        self._args.append((arg_type,arg_value))

    def build(self):
        """Builds an OscMessage from the current state of this builder.

        Raises:
          - BuildError: if the message could not be build or if the address
                        was empty.

        Returns:
          - an OscMessage instance.
        """
        if not self._address:
            raise BuildError('OSC addresses cannot be empty')
        dgram=b''
        try:
            # Write the address.
            dgram+=write_string(self._address)
            if not self._args:
                dgram+=write_string(',')
                return OscMessage(dgram)

            # Write the parameters.
            arg_types="".join([arg[0] for arg in self._args])
            dgram+=write_string(',' + arg_types)
            for arg_type,value in self._args:
                if arg_type == self.ARG_TYPE_STRING:
                    dgram+=write_string(value)
                elif arg_type == self.ARG_TYPE_INT:
                    dgram+=write_int(value)
                elif arg_type == self.ARG_TYPE_FLOAT:
                    dgram+=write_float(value)
                elif arg_type == self.ARG_TYPE_BLOB:
                    dgram+=write_blob(value)
                elif arg_type == self.ARG_TYPE_RGBA:
                    dgram+=write_rgba(value)
                elif arg_type == self.ARG_TYPE_TRUE or arg_type == self.ARG_TYPE_FALSE:
                    continue
                else:
                    raise BuildError('Incorrect parameter type found {}'.format(
                        arg_type))

            return OscMessage(dgram)
        except BuildError as be:
            raise BuildError('Could not build the message: {}'.format(be))

class UDPClient(object):
    """OSC client to send OscMessages or OscBundles via UDP."""

    def __init__(self,address,port):
        """Initialize the client.

        As this is UDP it will not actually make any attempt to connect to the
        given server at ip:port until the send() method is called.
        """
        self._sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self._sock.setblocking(0)
        self._address=address
        self._port=port

    def send(self,content):
        """Sends an OscBundle or OscMessage to the server."""
        self._sock.sendto(content.dgram,(self._address,self._port))

class SimpleUDPClient(UDPClient):
    """Simple OSC client with a `send_message` method."""

    def send_message(self,address,value):
        """Compose an OSC message and send it."""
        builder=OscMessageBuilder(address=address)
        if not isinstance(value,Iterable) or isinstance(value,(str,bytes)):
            values=[value]
        else:
            values=value
        for val in values:
            builder.add_arg(val)
        msg=builder.build()
        self.send(msg)
