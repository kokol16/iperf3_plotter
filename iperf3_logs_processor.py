import parser
import json
import pandas as pd
import matplotlib.pyplot as plt


def get_relative_path(absolute_path):
    filename=""
    for c in reversed(absolute_path):
        if c=="/":
            return filename[::-1]
        else:
            filename=filename+ c

     


def process_json_files():
    list_of_files=parser.parse_folder_with_json_files()
    #lists contain a dictionary for each json file
    list_of_stats_tcp=[]
    list_of_stats_udp=[]
    for file in list_of_files:
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
                if "filename" not in dict_tcp:
                    dict_tcp["filename"]=[]
                tmp_file_name= file
                tmp_file_name= str(tmp_file_name)
                dict_tcp["filename"].append(get_relative_path(str(file)))

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
                if "filename" not in dict_udp:
                    dict_udp["filename"]=[]
                dict_udp["filename"].append(get_relative_path(str(file)))
            list_of_stats_udp.append(dict_udp)
    create_plots(list_of_stats_tcp,list_of_stats_udp)

count=0
def create_plot_for_each_file(list_of_stats,protocol,exclude,destination, figure_to_start):
    i=figure_to_start
    global count
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
            plt.savefig(destination+'/plot_' +protocol+"_"+str(key)+str(count)+".png")
            count+=1
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
            #print(df["filename"][0])
            if 'client_' in df["filename"][0] or '_C.json' in df['filename'][0]:
                plt.plot( round(df['start'] + 60,3), round(df[str(key)],3),label=df["filename"][0])
            else:
                plt.plot( round(df['start'],3), round(df[str(key)],3),label=df["filename"][0])
            plt.xlabel("start")
            plt.ylabel(str(key))
            plt.legend()
            plt.savefig(destination+'/plot_' +protocol+"_combined_"+str(key)+".png")
            i+=1
        #print(df)
    #i= create_plot_for_each_file(list_of_stats,protocol,exclude,destination,i)
    return i


def create_plots(list_of_stats_tcp , list_of_stats_udp):
    f= open("app.conf.json")
    data=json.load(f)
    last_figure_numb=0
    last_figure_numb=plot_tcp_or_udp(list_of_stats_tcp,"TCP",data["excluded_metrics"],data["destination_folder"],last_figure_numb)
    plot_tcp_or_udp(list_of_stats_udp,"UDP",data["excluded_metrics"],data["destination_folder"],last_figure_numb)






process_json_files()