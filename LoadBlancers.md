A web server's job is basically to accept requests from clients and send responses to those requests. A web server gets a URL, translates it to a filename (for static requests), and sends that file back over the internet from the local disk, or it translates it to a program name (for dynamic requests), executes it, and then sends the output of that program back over the internet to the requesting party. If for any reason, the web server was not able to process and complete the request, it instead returns an error message. The word, web server, can refer to the machine (computer/hardware) itself, or the software that receives requests and sends out responses.

Servers worb by using various protocols through different ports, and include: hypertext transfer protocol (HTTP), typically through port 80, simple mail transfer protocol (SMTP), typically through port 25, domain name service (DNS) for mapping domain names to their corresponding IP addresses, genearlly through port 53, and file transfer protocol (FTP) for uploading and downloading files, usually through port 21.
Types of Load balancing Softwares

But one server can host many websites, not just one - though, to the outside world, they seem separate from one another. To achieve this, every one of those websites has to be assigned a different name, even if those all map eventually to the same machine. This is accomplished by using what is known as virtual hosts.

Since IP addresses are difficult to remember, we, as visitors to specific sites, usually type in their respective domain names into the URL address box on our browsers. The browser then connects to a DNS server, which translates the domain names to their IP addresses. The browser then takes the returned IP address and connects to it. The browser also sends a Host header with the request so that, if the server is hosting multiple sites, it will know which one to serve back.

For example, typing in www.google.com into your browser's address field might send the following request to the server at that IP address:

The client (usually but not necessarily a web browser) makes a request, the server sends back a response, and communication stops. The server doesn't look forward for more communication as is the case with other protocols that stay at a waiting state after the request is over.

1. Round Robin - Requests are routed in a rotation for all the servers

2. Weighted Round Robin - Same as Round Robin but servers are given points and higher traffic is diverted to servers with higher points 

3. Least Connection - Takes in to accoint the current server load and requests are routed to the server with the least number of active sessions at the current time.

4. Weighted Least Connection - Like in the Weighted Round Robin method each server is given a numerical value. The load balancer uses this when allocating requests to servers. If two servers have the same number of active connections then the server with the higher weighting will be allocated the new request.

5. Agent Based Adaptive Load Balancing
Each server in the pool has an agent that reports on its current load to the load balancer. This real time information is used when deciding which server is best placed to handle a request. This is used in conjunction with other techniques such as Weighted Round Robin and Weighted Least Connection.

6. Chained Failover (Fixed Weighted)
In this method a predetermined order of servers is configured in a chain. All requests are sent to the first server in the chain. If it can’t accept any more requests the next server in the chain is sent all requests, then the third server. And so on.

7. Weighted Response Time
This method uses the response information from a server health check to determine the server that is responding fastest at a particular time. The next server access request is then sent to that server. This ensures that any servers that are under heavy load, and which will respond more slowly, are not sent new requests. This allows the load to even out on the available server pool over time.

8. Source IP Hash
Source IP Hash load balancing uses an algorithm that takes the source and destination IP address of the client and server and combines them to generate a unique hash key. This key is used to allocate the client to a particular server. As the key can be regenerated if the session is broken this method of load balancing can ensure that the client request is directed to the same server that it was using previously. This is useful if it’s important that a client should connect to a session that is still active after a disconnection. For example, to retain items in a shopping cart between sessions.

9. Software Defined Networking (SDN) Adaptive
SDN Adaptive combines knowledge of upper networking layers, with information about the state of the network at lower layers. Information about data from Layers 4 & 7 of the network, and information about the network from layers 2 & 3 is combined when deciding how to allocate requests. This allows information about the status of the servers, the status of the applications running on them, the health of the network infrastructure, and the level of congestion on the network to all play a part in the load balancing decision making.