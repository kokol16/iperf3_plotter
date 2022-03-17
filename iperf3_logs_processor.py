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


def create_plots(list_of_stats_tcp , list_of_stats_udp):
    f= open("app.conf.json")
    data=json.load(f)
    #print(len ( list_of_stats_udp ) )
    for udp_dict in list_of_stats_udp:
        i =0
        df = pd.DataFrame.from_dict(udp_dict)
        for key, value in udp_dict.items():
            fig = plt.figure(i)
            if str(key) in data["excluded_metrics"]:
                continue

            #print(str(key))
            plt.plot( df['start'], df[str(key)])
            plt.xlabel("start")
            plt.ylabel(str(key))
            i+=1

        print(df)
        #if i ==1:
            #print("xaxa")
            #ax= df.plot(ax=ax,kind = 'bar' , x ='start', y='bytes' )
        #else:
            #ax= df.plot(kind = 'bar' , x ='start', y='bytes')
        #i=1
        
    #plt.xlim(0,18000)
    #plt.ylim(0,30)
    plt.show()



    



    #df2 = pd.DataFrame.from_dict(list_of_stats_udp[1])

    #print(df)
    #ax= df.plot(x ='start', y='bits_per_second', kind = 'line')
    #df2.plot(ax=ax , x ='start', y='bits_per_second')
    #plt.show()


    


process_json_files()