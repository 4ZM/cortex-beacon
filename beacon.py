"""
Copyright (C) 2013 Anders Sundman <anders@4zm.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from emokit import emotiv
import gevent
import socket
import sys
import select

sensorNames = { 'X', 'Y', 'F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4', 'Unknown' }

def emotiv_setup():
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    return headset

def emotiv_read(headset):
    packet = headset.dequeue()
    sensors = packet.sensors
    dataStr = ",".join(str(sensors[x]['value']) for x in sensorNames)
    return dataStr
    
if __name__ == "__main__":

    headset = emotiv_setup()

    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(('', 1337))
    srv_sock.listen(5)
    srv_sock.settimeout(1)
        
    try:
        while True: # Server loop
            try:
                print "Waiting for a client. Press enter to quit..."
                client_sock = None
                
                try:
                    (client_sock, address) = srv_sock.accept()
                except socket.timeout:
                    if select.select([sys.stdin], [], [], 0)[0]:
                        break
                    else:
                        continue
                        
                print "Received connection. Will now stream data."

                while True:
                    dataStr = emotiv_read(headset)
                    client_sock.send(dataStr + "\n")
                    gevent.sleep(0)

            except socket.error:
                print "Socket Error. Possibly because client disconnected."
            except KeyboardInterrupt:
                print "Got keybord interrupt, disconnecting client"
            finally:
                if client_sock is not None:
                    client_sock.close()
                                
    except KeyboardInterrupt:
        print "Shutting down..."
    finally:
        headset.close()
