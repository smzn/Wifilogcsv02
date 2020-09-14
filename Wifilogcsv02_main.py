'''
Created on Aug 10, 2020

@author: haruka
'''
#transitionsとdurationの集約
import wifilogcsv02.Wifilogcsv02_lib as mdl

name = "2014_09_24_2"

filepath = "./MPI/csv/"+name
tfilename = "transitions_all.csv"
dfilename = "duration_all.csv"
APfile = "./csv/APlocations.csv"



wlib = mdl.Wifilogcsv02_lib(filepath)

wlib.get_APlocations(APfile) #AP情報入れる
transitions_all = wlib.get_csv_tfile(tfilename) #transition足した
transitions_rate = wlib.get_rate_tfile(transitions_all) #transition rate
transitions_rate2 = wlib.get_rate_tfile2(transitions_rate) #transition rate  0の部分は省く

transitions_gall = wlib.get_csv_tfile_group(tfilename)#グループごとのrate
transitions_grate = wlib.get_rate_tfile_group(transitions_gall) #transition rate
transitions_grate2 = wlib.get_rate_tfile2_group(transitions_grate) #transition rate 0の部分は省く

duration_all = wlib.get_csv_dfile(dfilename) # duration足した
meantime = wlib.get_meantime() #平均系内時間計算
meantime = wlib.get_meantime2() #平均系内時間計算 3時間以上は除外


