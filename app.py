#!/usr/bin/env python

from simulationModels import *
from validations import *

import ttk
from Tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pandas import DataFrame

# plt.rcdefaults()

LARGE_FONT = ("Verdana", 12)


class LoadBalancer():
    def __init__(self):
        self.window = Tk()
        self.window.title("Load Balancer Simulator")
        self.keep_running_simulation = False
        self.sim_run_counter = 0
        self.vcmd = (self.window.register(validateNumerics), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.selected_algo_value = StringVar()
        self.no_of_requests_value = IntVar()
        self.no_of_servers_value = IntVar()
        self.type_of_load_value = StringVar()
        self.server_details = {}  # reference to all the server objects
        self.create_widgets()
        self.create_server_detail()
        self.simulation_results = []  # hold each results to be plotted [server(waiting connections, dropped connection)]

    def run_sim(self):
        self.sim_run_counter = self.sim_run_counter + 1
        if self.keep_running_simulation:
            algo = self.selected_algo_value.get()
            requests = self.no_of_requests_value.get()
            req_type = self.type_of_load_value.get()
            servers = self.no_of_servers_value.get()
            server_details = self.get_server_detail_values()
            percentage_load = self.request_percentage_scale.get()
            if validateEntries(algo, requests, servers):
                visualizer_text = 'Implementing  ' + str(algo) + ' on a load balancer with  ' + str(
                    servers) + ' handling ' + str(requests) + ' of ' + str(req_type) + ' type requests per second'
                # print(visualizer_text, servers, server_details, req_type, percentage_load)
                if algo == 'None':
                    tkMessageBox.showerror('Algorithm NOT selected', 'Please select an algorithm to proceed')
                if requests == 0 | servers == 0 | servers > 10:
                    tkMessageBox.showerror('Invalid Parameters',
                                           'Please select valid values to proceed')
                if algo == 'Round Robin':
                    self.simulation_results.append(
                        simulateRoundRobin(req_type, requests, percentage_load, servers, server_details, self))

                elif algo == 'Weighted Round Robin':
                    self.simulation_results.append(
                        simulateWeightedRoundRobin(req_type, requests, percentage_load, servers,
                                                   server_details, self))
                elif algo == 'Least Connection':
                    self.simulation_results.append(simulateLeastConnection(req_type, requests, percentage_load, servers,
                                                                           server_details, self))
                elif algo == 'Weighted Least Connection':
                    self.simulation_results.append(
                        simulateWeightedLeastConnection(req_type, requests, percentage_load, servers,
                                                        server_details, self))
                elif algo == 'Chained Failover':
                    self.simulation_results.append(
                        simulateCahinedFailover(req_type, requests, percentage_load, servers,
                                                server_details, self))

            self.plot_sim_results()
            self.window.after(1000, self.run_sim)

    def start_sim(self):
        self.keep_running_simulation = True
        self.window.after(0, self.run_sim)

    def stop_sim(self):
        self.keep_running_simulation = False
        self.sim_run_counter = 0
        self.simulation_results = []

    def plot_sim_results(self):
        data = self.simulation_results[-300:]
        server_waiting_data = {}
        server_dropped_connections = {}
        server_names = []
        usage = []
        for i in range(self.no_of_servers_value.get()):
            server_name = 'Server - ' + str(i + 1)
            server_names.append(server_name)
            usage.append(self.simulation_results[-1][i][0])
            server_waiting_data[server_name] = map(lambda d: d[i][1], data)
            server_dropped_connections[server_name] = map(lambda d: d[i][2], data)

        data_for_usage_data_frame = {'Servers': server_names,
                                     'Usage': usage, }

        dfUsage = DataFrame(data_for_usage_data_frame, columns=['Servers', 'Usage'])

        usage_bar = plt.Figure(figsize=(5, 4), dpi=100)
        usage_plot = usage_bar.add_subplot(111)
        chart_type = FigureCanvasTkAgg(usage_bar, self.visualizer_frame)
        chart_type.get_tk_widget().grid(row=1, column=1, sticky=W + N)
        dfUsage.plot(kind='bar', legend=True, ax=usage_plot)
        usage_plot.set_title('Percentage Usage')
        usage_plot.set_autoscaley_on(False)
        usage_plot.set_ylim([0, 120])
        usage_plot.set_xlabel('Servers')

        waiting_line = plt.Figure(figsize=(5, 4), dpi=100)
        waiting_plot = waiting_line.add_subplot(111)

        dfWaiting_s1 = DataFrame(server_waiting_data['Server - 1'], columns=['Server-1'])
        dfWaiting_s1.plot(kind='line', legend=True, ax=waiting_plot, color='b')
        dfWaiting_s2 = DataFrame(server_waiting_data['Server - 2'], columns=['Server-2'])
        dfWaiting_s2.plot(kind='line', legend=True, ax=waiting_plot, color='r')

        waiting_plot.set_title('Waiting Connections')
        waiting_plot.set_autoscalex_on(False)
        waiting_plot.set_xlim([0, 350])
        waiting_plot.set_xlabel('Time')
        waiting_plot.set_title('Waiting Connections')
        line_graph = FigureCanvasTkAgg(waiting_line, self.visualizer_frame)
        line_graph.get_tk_widget().grid(row=1, column=2, sticky=W + N)


    def create_server_detail(self):
        Label(self.choices_frame, text="Server Details").grid(row=9, column=1, sticky=W + N)
        Label(self.choices_frame, text="Memory (MB)").grid(row=9, column=2, sticky=W + N)
        Label(self.choices_frame, text="Weightage").grid(row=9, column=3, sticky=W + N)
        self.clear_server_details()
        for i in range(self.no_of_servers_value.get()):
            server_name_text = 'Server - ' + str(i + 1)
            self.server_details[server_name_text] = [IntVar(), IntVar()]
            self.server_details[server_name_text][0].set(1024)
            self.server_details[server_name_text][1].set(1)
            Label(self.choices_frame, text=server_name_text).grid(row=(10 + i), column=1, sticky=E, padx=5, pady=5)
            Entry(self.choices_frame, textvariable=self.server_details[server_name_text][0], validate='key',
                  validatecommand=self.vcmd).grid(row=(10 + i),
                                                  column=2, sticky=W, padx=5, pady=5)
            Entry(self.choices_frame, textvariable=self.server_details[server_name_text][1], validate='key',
                  validatecommand=self.vcmd).grid(row=(10 + i), column=3, sticky=W, padx=5, pady=5)

    def get_server_detail_values(self):
        server_details_values = []
        for i in range(self.no_of_servers_value.get()):
            server_name_text = 'Server - ' + str(i + 1)
            # server_detials [[mem, weight], ... ]
            server_details_values.append([self.server_details[server_name_text][0].get(),
                                          self.server_details[server_name_text][1].get()])
        return server_details_values

    def clear_server_details(self):
        self.simulation_results = []

    def create_widgets(self):
        self.window['padx'] = 5
        self.window['pady'] = 5

        config_frame = LabelFrame(self.window, text="Initial Configurations", relief=RIDGE)
        config_frame.grid(row=1, column=1, sticky=E + W + N + S)

        Label(config_frame, text="Max Requests/sec (X 100)").grid(sticky=E, padx=5, pady=10)
        requests_entry = Entry(config_frame, width=20, textvariable=self.no_of_requests_value, validate='key',
                               validatecommand=self.vcmd)
        requests_entry.grid(row=0, column=1, sticky=W, pady=10)

        Label(config_frame, text="No of Servers").grid(sticky=W, pady=10, padx=5)
        no_of_servers = Spinbox(config_frame, from_=2, to=10, width=5, justify=RIGHT,
                                textvariable=self.no_of_servers_value)
        no_of_servers.grid(row=1, column=1, sticky=W, pady=10)
        Button(config_frame, text="Set Servers", command=self.create_server_detail).grid(row=1, column=2)

        Label(config_frame, text="Load Percentage").grid(row=2, column=0, sticky=W)
        self.request_percentage_scale = Scale(config_frame, from_=50, to=200, orient=HORIZONTAL, length=200)
        self.request_percentage_scale.grid(row=2, column=1, sticky=W)
        self.request_percentage_scale.set(100)
        Label(config_frame, text="Type Of Load").grid(row=3, column=0, sticky=W)
        load_types = ["Text", "Images","Audio", "Video", "Mixed"]
        type_of_load = ttk.Combobox(config_frame, height=4, values=load_types, textvariable=self.type_of_load_value)
        type_of_load.grid(row=3, column=1, sticky=W)
        type_of_load.current(0)

        self.choices_frame = LabelFrame(self.window, text="Choices", relief=RIDGE)
        self.choices_frame.grid(row=1, column=2, sticky=E + W + N + S, padx=5)

        entry_label = Label(self.choices_frame, text="Loadbalancing Algorithm")
        entry_label.grid(row=4, rowspan=3, column=1, sticky=W + N)

        self.selected_algo_value = StringVar()
        self.selected_algo_value.set(None)
        algorithmSelection = Radiobutton(self.choices_frame, text='Round Robin', value='Round Robin',
                                         variable=self.selected_algo_value).grid(
            sticky=W,
            row=4,
            column=2,
            padx=5,
            pady=5)
        algorithmSelection = Radiobutton(self.choices_frame, text='Weighted Round Robin', value='Weighted Round Robin',
                                         variable=self.selected_algo_value).grid(
            sticky=W,
            row=5,
            column=2,
            padx=5,
            pady=5)
        algorithmSelection = Radiobutton(self.choices_frame, text='Least Connection', value='Least Connection',
                                         variable=self.selected_algo_value).grid(
            sticky=W,
            row=6,
            column=2,
            padx=5,
            pady=5)
        algorithmSelection = Radiobutton(self.choices_frame, text='Weighted Least Connection',
                                         value='Weighted Least Connection',
                                         variable=self.selected_algo_value).grid(sticky=W, row=7, column=2, padx=5,
                                                                                 pady=5)
        algorithmSelection = Radiobutton(self.choices_frame, text='Chained Failover',
                                         value='Chained Failover',
                                         variable=self.selected_algo_value).grid(sticky=W, row=8, column=2, padx=5,
                                                                                 pady=5)
        self.visualizer_frame = LabelFrame(self.window, text="Visualizer Window", relief=RIDGE, height=500)
        self.visualizer_frame.grid(row=2, rowspan=2, column=1, columnspan=3, sticky=E + W + N + S)
        # - - - - - - - - - - - - - - - - - - - - -
        # Quit button in the lower right corner
        self.start_button = Button(self.window, text="Start", command=self.start_sim).grid(row=1, column=3)
        stop_button = Button(self.window, text="Stop", command=self.stop_sim).grid(row=2, column=3)
        quit_button = Button(self.window, text="Quit", command=self.window.destroy).grid(row=3, column=3)


# Create the entire GUI program
program = LoadBalancer()
program.window.mainloop()
