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

def create_plot_for_each_file(list_of_stats_tcp , list_of_stats_udp,figure_to_start):
    f= open("app.conf.json")
    data=json.load(f)
    i =figure_to_start
    for tcp_dict in list_of_stats_tcp:
        df = pd.DataFrame.from_dict(tcp_dict)
        for key, value in tcp_dict.items():
            if str(key) in data["excluded_metrics"]:
                continue
            fig = plt.figure(i)
            plt.plot( df['start'], df[str(key)],label="tcp")
            plt.xlabel("start")
            plt.ylabel(str(key))
            plt.legend()
            plt.savefig(data["destination_folder"]+'/plot' +str(i)+".png")



            i+=1
    # TODO add UDP
        


def create_plots(list_of_stats_tcp , list_of_stats_udp):
    f= open("app.conf.json")
    data=json.load(f)
    #print(len ( list_of_stats_udp ) )
    for udp_dict in list_of_stats_udp:
        i =0
        df = pd.DataFrame.from_dict(udp_dict)
        for key, value in udp_dict.items():
            if str(key) in data["excluded_metrics"]:
                continue
            fig = plt.figure(i)
            #print(str(key))
            plt.plot( df['start'], df[str(key)],label="udp")
            plt.xlabel("start")
            plt.ylabel(str(key))
            plt.legend()
            plt.savefig(data["destination_folder"]+'/plot' +str(i)+".png")

            i+=1
        print(df)
    #TODO add tcp
    create_plot_for_each_file(list_of_stats_tcp, list_of_stats_udp,i+1)
    



    



    #df2 = pd.DataFrame.from_dict(list_of_stats_udp[1])

    #print(df)
    #ax= df.plot(x ='start', y='bits_per_second', kind = 'line')
    #df2.plot(ax=ax , x ='start', y='bits_per_second')
    #plt.show()


    


process_json_files()