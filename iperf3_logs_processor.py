import parser
import json
import pandas as pd
import matplotlib.pyplot as plt

def process_json_files():
    list_of_files=parser.parse_folder_with_json_files()
    #lists contain a dictionary for each json file
    list_of_stats_tcp=[]
    list_of_stats_udp=[]
    for file in list_of_files:
        print(file)
        f = open(file)
        data = json.load(f)
        if data["start"]["test_start"]["protocol"]=="TCP":
            #tcp json file
            dict_tcp={}
            for interval in data["intervals"]:
                for key , value in interval["streams"][0].items():
                    #print( key , ": ", value )
                    if key not in dict_tcp: 
                        dict_tcp[key]=[]
                    dict_tcp[key].append(value)
            list_of_stats_tcp.append(dict_tcp)

        else:
            #udp json file
            dict_udp={}
            for interval in data["intervals"]:
                for key , value in interval["streams"][0].items():
                    #print( key , ": ", value )
                    if key not in dict_udp: 
                        dict_udp[key]=[]
                    dict_udp[key].append(value)
            list_of_stats_udp.append(dict_udp)
    create_plots(list_of_stats_tcp,list_of_stats_udp)


def create_plot_for_each_file(list_of_stats,protocol,exclude,destination, figure_to_start):
    i=figure_to_start
    for protocol_dict in list_of_stats:
        df = pd.DataFrame.from_dict(protocol_dict)
        for key, value in protocol_dict.items():
            if str(key) in exclude:
                continue
            fig = plt.figure(i)
            plt.plot( round(df['start'],3), round(df[str(key)],3),label=protocol)
            plt.xlabel("start")
            plt.ylabel(str(key))
            plt.legend()
            plt.savefig(destination+'/plot' +str(i)+".png")
            i+=1
    return i 
        


def plot_tcp_or_udp(list_of_stats,protocol,exclude,destination,last_figure_number):
    for protocol_dict in list_of_stats:
        i=last_figure_number
        df = pd.DataFrame.from_dict(protocol_dict)
        for key, value in protocol_dict.items():
            if str(key) in exclude:
                continue
            fig = plt.figure(i)
            plt.plot( round(df['start'],3), round(df[str(key)],3),label=protocol)
            plt.xlabel("start")
            plt.ylabel(str(key))
            plt.legend()
            plt.savefig(destination+'/plot' +str(i)+".png")
            i+=1
        #print(df)
    i= create_plot_for_each_file(list_of_stats,protocol,exclude,destination,i)
    return i


def create_plots(list_of_stats_tcp , list_of_stats_udp):
    f= open("app.conf.json")
    data=json.load(f)
    last_figure_numb=0
    last_figure_numb=plot_tcp_or_udp(list_of_stats_tcp,"TCP",data["excluded_metrics"],data["destination_folder"],last_figure_numb)
    plot_tcp_or_udp(list_of_stats_udp,"UDP",data["excluded_metrics"],data["destination_folder"],last_figure_numb)






process_json_files()