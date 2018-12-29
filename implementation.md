user input
    number of servers
        - Each servers mem rating
        - Each servers wight rating
    requests per sec
    type load of the requests
        - just output some thing - text
        - have lot of computing with in it
        
models
    servers with in the loadbalancer - computation power for each
    number of requests per sec and type of requests
    algorithm calculation models
    output models
     -  percentage memory usage consumption of each server vs time
     -  waiting connections for each server
     -  cumulative number of requests dropped due to over busy per server

visualization component
    using tkinter, panda and matlab plot library
    -   a bar graph of present memory consumption refreshed every second
    -   a scatter plot of waiting connections each sec

models will hold the logic and state of each of the factor to be graphed

536,870,912 max length of python array so can run the simulation for 536,870,912/5 sec 
@  1 every 200 ms

server matrix would be displayed would be the active server connections
and if they are above 5 times the memory we will put them as rejected connections
to accomodate for a 5 sec wait time any thing that is waiting for more then 5 secs is not 
useful
    - active connections
    - dropped connections
 both will be represented as numbers