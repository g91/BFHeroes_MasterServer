Battlefield Heroes Master Server Emulator
=================================================

![Battlefield Heroes Cover](https://vignette.wikia.nocookie.net/battlefield/images/0/0e/Battlefield_Heroes_Cover.jpg/revision/latest?cb=20150817034842 "Battlefield Heroes Cover")


Game Info
---------

Type         | Value
------------:|:-----------
Developer(s) | EA DICE and Easy Studios
Publisher(s) | Electronic Arts
Series       | Battlefield
Engine       | Refractor 2 Engine
Platform(s)  | Microsoft Windows
Genre(s)     | Third-person shooter
Mode(s)      | Multiplayer


Legal notes
-----------

- The project aren't containing *any* of the original code from the game!!! 
- It is an emulated program!
- That are imitating original server
- It is completely legal to use this code!
 

Requirements
------------

- Original copy of Battlefield Heroes (preffered version: v1.42)

Module           | Version | Download
----------------:|:-------:|:------------
Python           | 2.7     | [Python Download](https://www.python.org/)
colorama         | latest  | pip install colorama
passlib          | latest  | pip install passlib
Twisted          | 16.3.0  | pip install Twisted==16.3.0
pyOpenSSL        | 0.15.1  | pip install pyOpenSSL==0.15.1
cffi             | 1.3.0   | pip install cffi==1.3.0
cryptography     | 0.7.2   | pip install cryptography==0.7.2
service_identity | 1.0.0   | pip install service_identity==1.0.0

*...or just install everything via `pip install -r requirements.txt`*

Also you have to open these ports:

Port   | Type
------:|:-------
18270  | TCP
18275  | TCP/UDP
18051  | TCP
18056  | TCP/UDP
80     | TCP
443    | TCP


Setting up the emulator
-----------------------

- Make sure that all required ports (see above) are open
- Write the IP of the PC where the emulator will be hosted in the config.ini to the key 'emulator_ip' (overwrite "REPLACE_ME") and save it
- Run `Init.py`


Credits
-------

- B1naryKill3r (Main Programmer/Developer)

Special thanks to:
- DICE (for making the game)
