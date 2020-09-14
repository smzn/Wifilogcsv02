'''
Created on Aug 10, 2020

@author: haruka
'''
import os
import csv
import time
import pprint
import pandas as pd
import numpy as np
import mysql.connector

class Wifilogcsv02_lib :

    def __init__(self, filepath):
        self.filepath = filepath
        self.csv_tfile = ""
        self.file_tlist = []
        self.csv_dfile = ""
        self.file_dlist = []
        self.duration_all = 0
        self.APlocations = []
        self.transition_all =[]
        self.transition_rate = []
        self.transitions_gall = []
        self.transition_grate = []
        # コネクションの作成
        #dbh = mysql.connector.connect(
        #    host='cloud02.mizunolab.info',
        ##    port='3306',
        #    db='mznwifilog',
        #    user='mznwifilog',
        #    password='kansoukikashiteyo',
        #    charset='utf8'
        #)
        #print(dbh.is_connected())
        #self.cur = dbh.cursor()

    def get_APlocations(self,csv_name):
        self.APlocations = pd.read_csv(csv_name, engine='python')

    def get_csv_tfile(self, csv_tfile):
        self.csv_tfile = csv_tfile
        self.file_tlist = []
        for file in os.listdir(self.filepath):
            is_tfile = 'transition' in file #transitionファイルか？
            not_csv_file = self.csv_tfile != file# リストCSVファイルでないか
            if is_tfile  and not_csv_file:
                self.file_tlist.append(file)
        #print(self.file_tlist)

        for i in range(len(self.file_tlist)):
            if i == 0:
                self.transition_all = pd.read_csv(self.filepath+'/'+self.file_tlist[i], engine='python', index_col=0)
            else:
                self.transition_all += pd.read_csv(self.filepath+'/'+self.file_tlist[i], engine='python', index_col=0)
        #print(self.transition_all)
        self.transition_all.to_csv(self.filepath+'/'+self.csv_tfile)
        return self.transition_all

    def get_rate_tfile(self, transition_all):
        self.transition_rate = transition_all
        tsum = transition_all.sum(axis=1) # 行ごとの合計を算出(文字データはむし)
        #print(tsum)
        for c in self.transition_rate.columns:
            self.transition_rate[c] = self.transition_rate[c]/tsum
        transition_rate = self.transition_rate.fillna(0)
        #print(transition_rate)
        transition_rate.to_csv(self.filepath+'/trate.csv')
        return transition_rate

    def get_rate_tfile2(self, transition_all):
        self.transition_rate = transition_all
        tsum = transition_all.sum(axis=1) # 行ごとの合計を算出(文字データはむし)
        dlist = list(tsum[tsum == 0].index)
        #print(dlist)
        self.transition_rate = self.transition_rate.drop(dlist)
        self.transition_rate = self.transition_rate.drop(self.transition_rate.columns[dlist], axis=1)
        #print(transition_rate)
        self.transition_rate.to_csv(self.filepath+'/markov_rate.csv')
        self.APlocations.drop(dlist).to_csv(self.filepath+'/markov_AP.csv')

        #for column_name, item in transition_rate.iteritems():
            #print(column_name)
            #for column_name2, item2 in item.iteritems():
                #print(column_name2, item2)
        return self.transition_rate

    def get_csv_tfile_group(self, csv_tfile):
        APid = self.APlocations['AP'].str.split('Bldg', expand=True)[1].str.split('AP', expand=True)[0].str.split('_', expand=True)[0]
        print(self.filepath+'/'+csv_tfile)
        with open(self.filepath+'/'+csv_tfile) as f:
            reader = csv.reader(f)
            l = [row for row in reader]
        tall = [[int(v) for v in row[1:]] for row in l[1:]]
        gtall = [[0] * 49 for i in range(49)]#外部もあるため+1
        #print(gtall)
        for i, iname in enumerate(APid):
            #print(i, iname)
            for j, jname in enumerate(APid):
                #print(j, jname)
                gtall[int(iname)-1][int(jname)-1] = gtall[int(iname)-1][int(jname)-1] + tall[i][j]
            gtall[int(iname)-1][48] = gtall[int(iname)-1][48] + tall[i][-1]#外部用
        for i, iname in enumerate(APid):
            #print(i, iname)
            gtall[48][int(iname)-1] = gtall[48][int(iname)-1] + tall[-1][i]
        gtall[48][48] = gtall[48][48] + tall[-1][-1]#外部用
        #print(gtall[48])
        self.transitions_gall = pd.DataFrame(gtall,index=[i for i in range(len(gtall))],columns=[i for i in range(len(gtall))])
        self.transitions_gall.to_csv(self.filepath+'/gtransitions_all.csv')

        return self.transitions_gall


    def get_rate_tfile_group(self, transition_gall):
        self.transition_grate = transition_gall
        tsum = transition_gall.sum(axis=1) # 行ごとの合計を算出(文字データはむし)
        #print(tsum)
        for c in self.transition_grate.columns:
            self.transition_grate[c] = self.transition_grate[c]/tsum
        transition_grate = self.transition_grate.fillna(0)
        #print(transition_grate)
        transition_grate.to_csv(self.filepath+'/gtrate.csv')
        return transition_grate

    def get_rate_tfile2_group(self, transition_gall):
        self.transition_grate = transition_gall
        tsum = transition_gall.sum(axis=1) # 行ごとの合計を算出(文字データはむし)
        dlist = list(tsum[tsum == 0].index)
        #print(dlist)
        self.transition_grate = self.transition_grate.drop(dlist)
        self.transition_grate = self.transition_grate.drop(self.transition_grate.columns[dlist], axis=1)
        #print(transition_grate)
        self.transition_grate.to_csv(self.filepath+'/markov_grate.csv')
        self.APlocations.drop(dlist).to_csv(self.filepath+'/markov_gAP.csv')
        return self.transition_grate

    def get_csv_dfile(self, csv_dfile):
        self.csv_dfile = csv_dfile
        self.file_dlist = []
        for file in os.listdir(self.filepath):
            is_tfile = 'duration' in file#transitionファイルか？
            not_csv_file = self.csv_dfile != file# リストCSVファイルでないか
            if is_tfile  and not_csv_file:
                self.file_dlist.append(file)
        #print(self.file_dlist)

        for i in range(len(self.file_dlist)):
            if i == 0:
                pd.read_csv(self.filepath+'/'+self.file_dlist[i], engine='python').to_csv(self.filepath+'/'+self.csv_dfile, columns=['duration','from','to'], index=False)
            else:
                pd.read_csv(self.filepath+'/'+self.file_dlist[i], engine='python').to_csv(self.filepath+'/'+self.csv_dfile, header=False, columns=['duration','from','to'], index=False, mode="a")

        self.duration_all = pd.read_csv(self.filepath+'/'+self.csv_dfile, engine='python')
        #print(self.duration_all)
        return self.duration_all

    def get_meantime(self):
        meantime = [-1 for i in range(len(self.APlocations))]
        for i in range(len(self.APlocations)):
            dlist = self.duration_all[(self.duration_all['from'] == i) & (self.duration_all['duration'] != -1)]
            if(dlist['duration'].count() > 0):
                meantime[i] = dlist['duration'].sum() / dlist['duration'].count()
        with open(self.filepath+'/meantime.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(meantime)
        return meantime


    def get_meantime2(self):
        meantime = [-1 for i in range(len(self.APlocations))]
        for i in range(len(self.APlocations)):
            dlist = self.duration_all[(self.duration_all['from'] == i) & (self.duration_all['duration'] != -1) & (self.duration_all['duration'] <= 3600*3)]
            if(dlist['duration'].count() > 0):
                meantime[i] = dlist['duration'].sum() / dlist['duration'].count()
        with open(self.filepath+'/meantime2.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(meantime)
        return meantime