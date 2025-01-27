#!/bin/bash
import os
import socket

stat = os.statvfs('/')
total_blocks = stat.f_blocks
free_blocks = stat.f_bfree
block_size = stat.f_frsize

print(f"Storage: {total_blocks} blocks total, {free_blocks} blocks free (Block size: {block_size} bytes)")

print(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
