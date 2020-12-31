# hackthon assigment- clinte&server
This project is about server and client connection on UDP and TCP protocols

Servers broadcast their announcements with destination port 13117 using UDP.
There isone packet format used for all UDP communications.

○ Magic cookie

○ Message type 

○ Server port 

connect to over TCP (the IP address of the server is the same for the UDP and
TCP connections, so it doesn't need to be sent).

The data over TCP has no packet format. After connecting, the client sends the
predefined team name to the server, followed by a line break.
After that, the client simply prints anything it gets from the server onscreen,
and sends anything it gets from
the keyboard to the server
