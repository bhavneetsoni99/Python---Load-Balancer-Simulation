#!/usr/bin/env python
import random


# server_details =[[memory, weight], .... ]
def simulateRoundRobin(req_type, requests, percentage_load, servers, server_details, app):
    simulated_result = []
    for i in range(servers):
        max_server_connections = server_details[i][0] / load_factor(req_type)
        # previous_iteration_server_i tupple containing (%agebusy, waiting connections, dropped connections)
        if app.sim_run_counter < 2:
            previous_iteration_server_i = (0, 0, 0)
        else:
            previous_iteration_server_i = app.simulation_results[app.sim_run_counter - 2][i]

        dropped_connections = previous_iteration_server_i[2]
        current_connections_server_i = data_load(requests, req_type) * percentage_load * 0.01 / servers / \
                                           load_factor(req_type)
        total_connections = current_connections_server_i + previous_iteration_server_i[1]

        excess_connections = total_connections - max_server_connections

        if excess_connections < 0:
            excess_connections = 0
        elif excess_connections > max_server_connections * 5:
            dropped_connections = dropped_connections+ excess_connections - max_server_connections * 5
            excess_connections = max_server_connections * 5

        percentage_busy = current_connections_server_i * 100 / max_server_connections
        if percentage_busy > 100:
            percentage_busy = 100
        simulated_result.append((percentage_busy, excess_connections, dropped_connections))
    print(simulated_result)
    return simulated_result


def simulateWeightedRoundRobin(req_type, requests, percentage_load, servers, server_details, app):
    total_server_weights = reduce(lambda x, y: x[1] + y[1], server_details)

    simulated_result = []
    for i in range(servers):
        max_server_connections = server_details[i][0] / load_factor(req_type)
        # previous_iteration_server_i tupple containing (%agebusy, waiting connections, dropped connections)
        if app.sim_run_counter < 2:
            previous_iteration_server_i = simulateRoundRobin(req_type, requests, percentage_load, servers, server_details, app)[0]
        else:
            previous_iteration_server_i = app.simulation_results[app.sim_run_counter - 2][i]

        dropped_connections = previous_iteration_server_i[2]
        current_connections_server_i = data_load(requests,req_type) * percentage_load * 0.01 * server_details[i][1]/total_server_weights/ load_factor(req_type)

        total_connections = current_connections_server_i + previous_iteration_server_i[1]

        excess_connections = total_connections - max_server_connections

        if excess_connections < 0:
            excess_connections = 0
        elif excess_connections > max_server_connections * 5:
            dropped_connections = dropped_connections + excess_connections - max_server_connections * 5
            excess_connections = max_server_connections * 5

        percentage_busy = current_connections_server_i * 100 / max_server_connections
        if percentage_busy > 100:
            percentage_busy = 100
        simulated_result.append((percentage_busy, excess_connections, dropped_connections))
    print(simulated_result)
    return simulated_result


def simulateLeastConnection(req_type, requests, percentage_load, servers, server_details, app):
    if app.sim_run_counter < 2:
        return simulateRoundRobin(req_type, requests, percentage_load, servers, server_details, app)
    else:
        previous_iteration_servers = app.simulation_results[app.sim_run_counter - 2]

    total_data_load = data_load(requests, req_type) * percentage_load * 0.01

    incomming_connections = total_data_load/load_factor(req_type)
    total_waiting_connections = reduce(lambda x, y: x[1]+y[1], previous_iteration_servers)
    connections_to_each_server = (incomming_connections+total_waiting_connections)/servers

    this_iteration_servers = []
    for i in range(servers):
        server_max_connections = server_details[i][0] / load_factor(req_type)
        excess_connections = connections_to_each_server - server_max_connections
        dropped_connections = previous_iteration_servers[i][2]
        if excess_connections < 0:
            excess_connections = 0
        elif excess_connections > server_max_connections * 5:
            dropped_connections = dropped_connections + excess_connections - server_max_connections * 5
            excess_connections = server_max_connections * 5

        percentage_busy = connections_to_each_server * 100 / server_max_connections
        if percentage_busy > 100:
            percentage_busy = 100
        this_iteration_servers.append((percentage_busy, excess_connections, dropped_connections))
    print(this_iteration_servers)
    return this_iteration_servers

def simulateWeightedLeastConnection(req_type, requests, percentage_load, servers, server_details, app):
    if app.sim_run_counter < 2:
        return simulateWeightedRoundRobin(req_type, requests, percentage_load, servers, server_details, app)
    else:
        previous_iteration_servers = app.simulation_results[app.sim_run_counter - 2]

    total_data_load = data_load(requests, req_type) * percentage_load * 0.01

    incomming_connections = total_data_load/load_factor(req_type)
    total_waiting_connections = reduce(lambda x, y: x[1]+y[1], previous_iteration_servers)
    outstanding_connections = incomming_connections + total_waiting_connections
    total_server_weights = reduce(lambda x, y: x[1] + y[1], server_details)
    this_iteration_servers = []
    for i in range(servers):
        server_max_connections = server_details[i][0] / load_factor(req_type)
        allocated_connection = outstanding_connections*server_details[i][1] / total_server_weights
        excess_connections = allocated_connection - server_max_connections
        dropped_connections = previous_iteration_servers[i][2]
        if excess_connections < 0:
            excess_connections = 0
        elif excess_connections > server_max_connections * 5:
            dropped_connections = dropped_connections + excess_connections - server_max_connections * 5
            excess_connections = server_max_connections * 5

        percentage_busy = allocated_connection * 100 / server_max_connections
        if percentage_busy > 100:
            percentage_busy = 100
        this_iteration_servers.append((percentage_busy, excess_connections, dropped_connections))
    print(this_iteration_servers)
    return this_iteration_servers

def simulateCahinedFailover(req_type, requests, percentage_load, servers, server_details, app):
    if app.sim_run_counter < 2:
        previous_iteration_servers = [(0, 0, 0)]
    else:
        previous_iteration_servers = app.simulation_results[app.sim_run_counter - 2]

    total_data_load = data_load(requests, req_type) * percentage_load * 0.01

    incoming_connections = total_data_load/load_factor(req_type)
    this_iteration_servers = []
    for i in range(servers):
        if incoming_connections > 0:
            server_capacity = server_details[i][0] / load_factor(req_type)
            if app.sim_run_counter < 2:
                server_active_connections = 0
                server_dropped_connections = 0
            else:
                server_active_connections = previous_iteration_servers[i][1]
                server_dropped_connections = previous_iteration_servers[i][2]
            present_active_connections = server_active_connections + incoming_connections - server_capacity
            if present_active_connections > 0:
                percentage_load = 100
            else:
                percentage_load = (server_active_connections + incoming_connections) * 100 / server_capacity
            this_iteration_servers.append((percentage_load, 0, server_dropped_connections))
            incoming_connections = present_active_connections
        else:
            this_iteration_servers.append((0,0,0))

    if incoming_connections>0:
        per_server_load = incoming_connections / servers
        for i in range(servers):
            t = this_iteration_servers[i]
            lst = list(t)
            lst[1] = per_server_load
            t = tuple(lst)
            this_iteration_servers[i] = t
    print(this_iteration_servers)
    return this_iteration_servers

def data_load(requests, req_type):
    return requests * 100 * load_factor(req_type)


def load_factor(req_type):
    if req_type == "Text":
        return 0.2
    elif req_type == "Images":
        return 2
    elif req_type == "Audio":
        return 10
    elif req_type == "Video":
        return 50
    elif req_type == "Mixed":
        return 0.2 * random.randint(1, 50)
