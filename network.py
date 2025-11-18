#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Network Module
Retrieves network information like current IP address.
"""
import socket


def get_local_ip_address():
    """
    Get the current local IP address of this device.
    Returns 'No connection' if not connected to a network.
    """
    try:
        # Create a socket to determine the IP address
        # We don't actually connect, just use this to find the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "No connection"
