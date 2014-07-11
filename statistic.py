# -*- coding: utf-8 -*-
__author__ = 'bitcsdby'

from Rawdatastructure import Rawdatastructure
import urllib2
import json
import pickle


class Statistic:
    def __init__(self):
        self.dbitems = []
        self.dsitems = []
        self.tobrakes = 0  ## time of brakes
        self.tostepongas = 0  ## time of step on the gas
        self.tohighspeed = 0.  ## time of high speed working time
        self.toidling = 0.  ## time of idling
        self.mildistance = 0. ## total Malfunction Indicator Light trip distance
        self.clrdistance = 0. ## total Malfunction Indicator Clear trip distance
        self.oilconsumption = 0.  ## total energy consumption
        self.drivingscore = 0.  ## driving score
        self.averagespeed = 0.  ##  total 24 hour averge speed

    #def getdatafromweb(self, start, count, url, dspath, dbpath):
     def unpackdata(self):

        self.dbitems.reverse()

        for item in self.dbitems:
            #print int(item['VSS'])
            if int(item['VSS']) != 0x88:
                dsitem = Rawdatastructure(item)
                self.dsitems.append(dsitem)

            #else:
               #print 'invalid dbitem' logging
        self.dsitems.sort(key=lambda x: x.obdid);


    def getdatafromlocal(self, dspath, dbpath):
        with open(dspath, 'rb') as dsfile:
            self.dsitems = pickle.load(dsfile)
        with open(dbpath, 'rb') as dbfile:
            self.dbitems = pickle.load(dbfile)

        self.dsitems.sort(key=lambda x: x.obdid);
        self.dbitems.sort(key=lambda x: x['obds12_id'])

        #for x in self.dbitems:
        #    print '%8s'%(x['obds12_id']), '%8s'%x['MIL_DIST'], \
        #          '%8s'%x['CLR_DIST'],'%8s'%x['VSS'],'%8s'%x['MAF'], \
        #          '%8s'%x['LOAD_PCT'],'%8s'%x['RPM'],'%8s'%x['APP_R']




    def setscore(self):
        A = 100 - self.tostepongas * 7.5
        A = 60 if A < 60 else A

        B = 100 - self.tobrakes * 7.5
        B = 60 if B < 60 else B

        C = 100 - self.toidling
        C = 60 if C < 60 else C

        D = 100 - self.tohighspeed
        D = 60 if D < 60 else D
        #print A,B,C,D
        self.drivingscore = (A + B + C + D ) / 4

## 没有判定时间段，可以根据时间段，考虑不同段落的计算
## 考虑出现三分钟以上的非法数据  就认为是两段路程
## 两段路程的考虑
    def runstatistic(self):

        unpackdata();

        l = len(self.dsitems)
        maxspeed = 0.0      ## for maxspeed
        speedsum = 0.0      ## for average speed
        consumptionsum = 0.0        ## for averge oil consumption

        id_load_pct = 0;

        for i in range(l-1):
            self.dsitems[i].printvalues()
            # print self.dsitems[i].vss
            #print type(self.dsitems[i].load_pct)
            #print 'MAF', self.dsitems[i].maf

            ## load_pct
            if self.dsitems[i].load_pct > 50 and self.dsitems[i].vss < self.dsitems[i+1].vss:
                #print 'load_pct', self.dsitems[i].load_pct
                #print 'vss', self.dsitems[i].vss, self.dsitems[i+1].vss
                #print ''

                #self.dsitems[i].printvalues()
                #self.dsitems[i+1].printvalues()
                #print ''

                if id_load_pct != self.dsitems[i].obdid - 1:
                    self.tostepongas += 1
                #else:
                    #print 'remove it stepongas'
                id_load_pct = self.dsitems[i].obdid

            if self.dsitems[i].load_pct < 10 and self.dsitems[i].vss > self.dsitems[i+1].vss + 15:  ## 15 is a threshold
                #print 'load_pct', self.dsitems[i].load_pct , self.dsitems[i].vss, self.dsitems[i+1].vss
                #print 'vss', self.dsitems[i].vss, self.dsitems[i+1].vss
                #print ''

                #self.dsitems[i].printvalues()
                #self.dsitems[i+1].printvalues()
                #print ''

                if id_load_pct != self.dsitems[i].obdid - 1:
                    self.tobrakes += 1
                #else:
                    #print 'remove it brakes'
                id_load_pct = self.dsitems[i].obdid


            ## speed
            speedsum += self.dsitems[i].vss
            if self.dsitems[i].vss > maxspeed:
                maxspeed = self.dsitems[i].vss
            if self.dsitems[i].vss > 50:
                #print 'vss', self.dsitems[i].vss
                self.tohighspeed += 1

            ##idling
            #print 'rmp app_r', self.dsitems[i].rpm, self.dsitems[i].vss
            if self.dsitems[i].rpm != 0 and self.dsitems[i].vss == 0:
                #print self.dsitems[i].rpm, self.dsitems[i].app_r
                self.toidling += 1

            ##energy consumption
            #print 'MAF', self.dsitems[i].maf
            if self.dsitems[i].vss != 0:
                consumptionsum += self.dsitems[i].maf / self.dsitems[i].vss * 0.339

            # DIST
            if self.dsitems[i].mil_dist > self.mildistance:
                self.mildistance = self.dsitems[i].mil_dist
            if self.dsitems[i].clr_dist > self.clrdistance:
                self.clrdistance = self.dsitems[i].clr_dist
            #print 'MIL_DIST cLRDIST', self.dsitems[i].mil_dist, self.dsitems[i].clr_dist
        #print l
        #print 'speedsum', speedsum

        self.setscore()

        if l != 0:
            self.averagespeed = speedsum / l ;
            self.oilconsumption = consumptionsum / l ;

        print self.clrdistance,self.dsitems[0].clr_dist

        print '急刹车次数', self.tobrakes
        print '急踩油门次数', self.tostepongas
        print '高速巡航时间', self.tohighspeed / l * 100, '%'
        print '怠速时间', self.toidling / l * 100, '%'
        print '行驶里程',  '总里程', self.mildistance + self.clrdistance - \
                                    self.dsitems[0].mil_dist - self.dsitems[0].clr_dist, 'Km', '  '\
                          '故障', self.mildistance - self.dsitems[0].mil_dist, '正常', self.clrdistance - self.dsitems[0].clr_dist
        print '平均速度', self.averagespeed, 'Km/h'
        print '平均油耗', self.oilconsumption, 'L/ 100km'
        print '驾驶评分', self.drivingscore
        print ''
        #print '行驶里程', self
        ## statistic with dsitems
        # print self.dbitems

        # clean memory


if __name__ == '__main__':
    s = Statistic()
    url = 'http://www.ecloudan.com/api.php?p=vanet.obd.getdata.obd&access_token=f313e38dfb990557b49f475d42e89237ddda905a34a086fa48e7f26d9894242b&'
    dsfilepath = 'latest_dsdata.pickle'
    dbfilepath = 'latest_dbdata.pickle'

    #s.getdatafromweb(380, 251, url, dsfilepath, dbfilepath)
    s.getdatafromlocal(dsfilepath, dbfilepath)

    s.runstatistic()