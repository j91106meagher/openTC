import numpy as np
from datetime import datetime


class tracks:
    def __init__(self):
        self.fn = []
        self.track = []
        self.ID = []
        self.Name = []
        self.num_lines = []
        self.trackset_type = []
        self.year = []
        
        self.rho = 1.15 #kgm-3 from Holland 80 Eq 4
        self.kts2ms = 0.51444 # knots to m/s
        self.nm2m = 1852
        self.Pns = 1005 
        self.earth_radius_m = 6371 * 1000
        self.vnfac  = 0.9
        self.max_vm = 25.0 #m/s
        
        self.grade = []
        self.lat = []
        self.lon = []
        self.Pc = []
        self.Vmax_knots = []
        self.Vmax_ms = []
        self.Rmax = []
        self.DLR50 = []
        self.RS50 = []
        self.RL50 = []
        self.DLR30 = []
        self.RL30 = []
        self.RS30 = []
        self.dto = []
        self.RS50_m = []
        self.RL50_m = []
        self.RL30_m = []
        self.RS30_m = []
        self.TY = []
        
        self.RAP_m = []
        self.RADP = []
        
        self.dismi = []
        self.thetai = []
        self.vmi = []
        self.dt = []
        self.dtoi = []
        self.dtmi = []
        self.dtm = []
        self.lati = []
        self.loni = []
        self.Pci = []
        self.Vmaxi_ms = []
        self.DLR50i = []
        self.RS50i = []
        self.RL50i = []
        self.DLR30i = []
        self.RL30i = []
        self.RS30i = []
        self.Rmaxi = []
        
    def parse_line_ebtrk(self,s,s2):
                  
        self.ID.append(s2[0])
        self.Name.append(s2[1])
        mmddhh = s[0]
        yyyy = s[1]
        
        self.dto.append(datetime.strptime(yyyy+mmddhh,'%Y%m%d%H'))
        self.lat = np.append(self.lat,float(s[2]))
        self.lon = np.append(self.lon,-1.0 * float(s[3]))
        self.Vmax_knots = np.append(self.Vmax_knots,float(s[4]))
        self.Vmax_ms = np.append(self.Vmax_ms,float(s[4])*self.kts2ms)
        self.Pc = np.append(self.Pc,float(s[5]))
        self.Rmax = np.append(self.Rmax,float(s[6])*self.nm2m)
        
        try:
            self.RADP = np.append(self.RADP,float(s[8])) #pressure of outer isobar
        except:
            self.RADP = np.append(self.RADP,0.0) #pressure of outer isobar
        self.RAP_m = np.append(self.RAP_m,float(s[9])*self.nm2m)
        
    def ebtrk_rmax(self):
        for i in range(len(self.Pc)):
            if (self.Rmax[i] <= 0.0):                
                self.Rmax[i] = 1000.0*46.4*np.exp(-0.0155*self.Vmax_ms[i] + 0.0169*self.lat[i])
            
    def interp_track(self,dt):
        from datetime import timedelta
        
        self.dt = dt
        start_datetime = self.dto[0]
        self.dtm = np.zeros((len(self.dto)))
        
        
        for i in range(len(self.dto)):
            deltadt = self.dto[i]- start_datetime
            self.dtm[i] = deltadt.total_seconds()/60.0
            
            
        self.dtmi = np.arange(self.dtm[0],self.dtm[-1]+dt,dt)
        for i in range(len(self.dtmi)):
            self.dtoi.append(start_datetime + timedelta(seconds=self.dtmi[i]*60.0))
        
        self.Pci = np.interp(self.dtmi,self.dtm,self.Pc)
        self.lati = np.interp(self.dtmi,self.dtm,self.lat)
        
        tlon = self.lon
        for i in range(len(self.lon)-1):
            if ((np.sign(self.lon[i]) ==1) and (np.sign(self.lon[i+1])== -1) and (self.lon[i]>90.0)):
                tlon[i+1] = tlon[i+1]+ 360.0
    
                
            if ((np.sign(self.lon[i]) ==-1) and (np.sign(self.lon[i+1])== 1) and (self.lon[i]<-90.0)):
                tlon[i+1] = tlon[i+1]- 360.0
        
                
        self.loni = np.interp(self.dtmi,self.dtm,tlon)
        
        ii = np.where(self.loni>180.0)
        self.loni[ii] = self.loni[ii] -360.0
        
        ii = np.where(self.loni<-180.0)
        self.loni[ii] = self.loni[ii] +360.0
        
            
        self.Vmaxi_ms = np.interp(self.dtmi,self.dtm,self.Vmax_ms)
        try:
            self.DLR50i = np.interp(self.dtmi,self.dtm,self.DLR50)
            self.RS50i = np.interp(self.dtmi,self.dtm,self.RS50_m)
            self.RL50i = np.interp(self.dtmi,self.dtm,self.RL50_m)
            self.DLR30i = np.interp(self.dtmi,self.dtm,self.DLR30)
            self.RL30i = np.interp(self.dtmi,self.dtm,self.RL30_m)
            self.RS30i = np.interp(self.dtmi,self.dtm,self.RS30_m)
        except:
            pass
        
        try:
            self.RAP_mi = np.interp(self.dtmi,self.dtm,self.RAP_m)
            self.RADPi = np.interp(self.dtmi,self.dtm,self.RADP)
            self.Rmaxi = np.interp(self.dtmi,self.dtm,self.Rmax)
        except:
            pass 
        
        print('len dtm',len(self.dtm),'len dtmi',len(self.dtmi))
        print('start_datetime',start_datetime,'ID',self.ID)
        
    def calc_vmi(self):
        #calc wind in moving frame from interpolation track
        from pyproj import Geod
        g = Geod(ellps='clrk66') # Use Clarke 1966 ellipsoid.
        
        self.vmi = np.zeros((len(self.lati)))
        self.thetai = np.zeros((len(self.lati)))
        self.dismi = np.zeros((len(self.lati)))
        
        for i in range(1,len(self.lati)):
            az12,az21,dis = g.inv(self.loni[i],self.lati[i],self.loni[i-1],self.lati[i-1])
            self.dismi[i] = dis
            self.vmi[i] = np.minimum(self.max_vm,dis/(self.dt * 60.0)) #m/s # dt is in min
            dlon = self.loni[i] - self.loni[i-1]
            a1 = np.sin(np.deg2rad(dlon))* np.cos(np.deg2rad(self.lati[i]))
            a2 = np.cos(np.deg2rad(self.lati[i-1]))*np.sin(np.deg2rad(self.lati[i])) - np.sin(np.deg2rad(self.lati[i-1]))*np.cos(np.deg2rad(self.lati[i])) * np.cos(np.deg2rad(dlon))
            self.thetai[i] = (np.pi/2.0) - np.arctan2(a1,a2) 
            #print('i',1,az12,az21,self.thetai[i])
        self.vmi[0] = self.vmi[1] 
        self.thetai[0] = self.thetai[1]
        
    def windfield_hs(self,wg,debug):
        import matplotlib.pyplot as plt
        
        for i in range(len(self.lati)):
            lati = self.lati[i]
            loni = self.loni[i]
            
            if ((lati>=wg.latll)and(loni>=wg.lonll)and(lati<=wg.latur)and(loni<=wg.lonur)and(self.Vmaxi_ms[i]>0.0)):
            
                latirad = np.deg2rad(lati)
                lonirad = np.deg2rad(loni) 
            
                #Havesine distance
                #wm2rad = wm2rad % (2*np.pi)
                dlon = wg.lonvrad - lonirad
                ii = np.where(dlon > np.pi)
                dlon[ii] = dlon[ii] - (2.0*np.pi)
                ii = np.where(dlon < -1*np.pi)
                dlon[ii] = dlon[ii] + (2.0*np.pi)
                
                dlat = wg.latvrad - latirad
                a = np.sin(dlat / 2) ** 2 + np.cos(latirad) * np.cos(wg.latvrad) * np.sin(dlon / 2) ** 2
                c = 2 * np.arcsin(np.sqrt(a))
                r = 6371*1000  # Radius of earth in m
                dism =  c*r
                
                wg.vs.fill(0.0)
                wg.vst.fill(0.0)
            
                p = np.argwhere(dism<(2.0*self.RAP_mi[i]))                
                count_p = p.shape[0]
                for ii in range(count_p):
                    wi = p[ii][0]
                    wj = p[ii][1]
                    if ((self.RAP_mi[i] > self.Rmaxi[i])and(self.RADPi[i] > self.Pci[i])):      
                        self.wind_H10_NOAA(wg,i,wi,wj,dism[wi,wj])
                
                
                wg.vst_max = np.maximum(wg.vst,wg.vst_max) 
                
                if True:
                #t 'vst','max',wg.vst.max(),'min',wg.vst.min(),'mean',wg.vst.mean()
                    #print('vst_max','max',wg.vst_max.max(),'min',wg.vst_max.min(),'mean',wg.vst_max.mean())
                    print('Vmaxi_ms[%d] %f vst.max %f vst.min %f max Vmaxi %f len(trk) %d'%(i,self.Vmaxi_ms[i],wg.vst.max(),wg.vst.min(),max(self.Vmaxi_ms),len(self.lati)))
                    #print('i',i,'Vmaxi_ms[i]',self.Vmaxi_ms[i],'max Vmaxi',max(self.Vmaxi_ms),self.Vmaxi_ms[i])#,'ID',self.ID[0],self.dto[0]  
                
                if (debug and wg.vst_max.max() > 0):
                    #import matplotlib.pyplot as plt 
                    plt.subplot(221)
                    plt.pcolormesh(wg.lonv,wg.latv,wg.vs)
                    plt.title('vs i %d of %d'%(i,len(self.lati)))
                    plt.colorbar()
                    #plt.show(block='False')
                    
                    plt.subplot(222)                    
                    plt.pcolormesh(wg.lonv,wg.latv,wg.vst_max)
                    #plt.title('track %d, vst_max i %d'%(self.track,i))
                    plt.colorbar()
                    
                    plt.subplot(223)                    
                    plt.pcolormesh(wg.lonv,wg.latv,wg.vst)
                    plt.title('vst')
                    plt.colorbar()
                    plt.ion()
                    plt.show()
                    plt.pause(5)
                    #time.sleep(8)
                    #plt.close()
                    #input('Enter to continue2')
                    plt.close()
                #nter to continue')
        
        if True:
                #t 'vst','max',wg.vst.max(),'min',wg.vst.min(),'mean',wg.vst.mean()
                print('vst_max','max',wg.vst_max.max(),'min',wg.vst_max.min(),'mean',wg.vst_max.mean())
                print('max Vmaxi',max(self.Vmaxi_ms))#,'ID',self.ID[0],self.dto[0]        
        if False: 
            plt.subplot(221)
            plt.pcolormesh(wg.lonv,wg.latv,wg.vs)
            plt.title('vs step %d'%(i))
            plt.colorbar()
            #plt.show(block='False')
                    
            plt.subplot(222)                    
            plt.pcolormesh(wg.lonv,wg.latv,wg.vst_max)
            #plt.title('i %d'%(i))
            if (self.trackset_type == 'JTWC'or self.trackset_type == 'EBTRK'):
                plt.title('vst_max trk %d y %d'%(self.track,self.year)) 
            elif (self.trackset_type == 'HURDAT'):
                plt.title('vst_max %s'%self.dto[0])
            else:
                plt.title('vst_max ID %d'%(self.ID[0])) 
            plt.colorbar()
            #plt.show(block='False')
            
            plt.subplot(223)                    
            plt.pcolormesh(wg.lonv,wg.latv,wg.vst)
            plt.title('vst')
            plt.colorbar()
            
            plt.ion()
            plt.show()
            plt.pause(5)
            #time.sleep(2)
            #raw_input('Enter to continue')
            plt.close()
            
    def wind_H10_NOAA(self,wg,i,wi,wj,r):
        #r in meters
        
        if ((r<=0.0)or(self.Rmaxi[i]<= 0.0)or (self.Vmaxi_ms[i] <=0.0)or (self.Pci[i]<=0.0)or (self.RADPi[i]<=0.0)or (self.RAP_mi[i]<=0.0)):
            return()
        
        
        
        trklati = self.lati[i]
        trkloni = self.loni[i]
                
        trklatirad = np.deg2rad(trklati)
        #trklonirad = np.deg2rad(trkloni)
        dlon = wg.lonv[wi,wj] - trkloni
        if dlon > 180.0:
            dlon = (dlon - 360.0)
        if dlon < -180.0:
            dlon = dlon + 360 
            
        xp = self.earth_radius_m * (dlon) * np.cos(np.mean([trklatirad,np.deg2rad(wg.latv[wi,wj])]))
        yp = self.earth_radius_m * (wg.latv[wi,wj] - trklati)
        theta = np.arctan2(yp,xp) # in radians -pi to pi

        vn = self.vnfac * self.vmi[i]
        vmax_mf = max (4.0, self.Vmaxi_ms[i] - vn)
        #if ((self.RADPi[i] - self.Pci[i])< -4.0):
        if (self.RADPi[i]< 950.0):
            RADP = 1005.0
        else:
            RADP = self.RADPi[i]
            
        if (RADP <= (self.Pci[i]+5.0)):  
            Pc = RADP - 5.0
        else:
            Pc = self.Pci[i]
        bs = (np.power(vmax_mf,2.0)*self.rho*np.e)/(100.0*(RADP - Pc)) #eq 7 H10
        betasn = np.power((self.Rmaxi[i]/self.RAP_mi[i]),bs)
        xn = (np.log(vn) - np.log(self.Vmaxi_ms[i]))/np.log(betasn*np.exp(1.0-betasn))
        
        if (r <= self.Rmaxi[i]):
            x = 0.5 #eq 10 H10
        else:
            x = 0.5 + (r - self.Rmaxi[i])*((xn - 0.5)/(self.RAP_mi[i] -self.Rmaxi[i])) #Holland10 eq 10
            
        betas = np.power((self.Rmaxi[i]/r),bs)
        vfac = min(1.0,np.power((betas*np.exp(1.0 - betas)),x))
       
        vs = vmax_mf * vfac
        wg.vs[wi,wj] = vs
        
        if (self.lati[i]<0.0):
            thetatang = (theta - (np.pi/2.0))%(2.0*np.pi)
        else:
            thetatang = (theta + (np.pi/2.0))%(2.0*np.pi)
     
        wm2rad = np.abs(self.thetai[i] - thetatang) # angle between storm bearing and radial wind vector
        wm2rad = wm2rad % (2*np.pi)
        
        vst = np.maximum(0.0,vs + vn * np.cos(wm2rad))
        #wind_x_mft = vst * -1.0 * np.sin(theta)
        #wind_y_mft = vst * np.cos(theta)
        rapflag = False
        if (r >= self.RAP_mi[i]):
            rapflag = True
            vst = vst * np.exp((-4.0 * r /self.RAP_mi[i]) + 4)
        
        if (np.isnan(vst)):
            wg.vst[wi,wj] = 0.0
        else:
            wg.vst[wi,wj] = vst
        
        if ((vst > 200.0)or(np.isnan(vst))):   
            print('i',i,'wi',wi,'wj',wj,'rapflag',rapflag)
            print('vs',vs,'vst',vst,'vmi',self.vmi[i],'wm2rad',wm2rad,'cos',np.cos(wm2rad),self.vmi[i] * np.cos(wm2rad),vs + self.vmi[i] * np.cos(wm2rad))
            print('RAP_mi',self.RAP_mi[i],'r',r,'Vmax',self.Vmaxi_ms[i],'Rmax',self.Rmaxi[i])
            print('x',x,'betas',betas,'bs',bs,'vmax_mf',vmax_mf,'rho',self.rho,'e',np.e,'RADP',self.RADPi[i],'Pc',Pc,'Pci',self.Pci[i])
            print('xn',xn,'betasn',betasn,'RAP_mi',self.RAP_mi[i],'vn',vn)
            #raw_input('Enter to continue')
            #if (vst > 200.0):
            #    raw_input('Enter to continue')
            #if (np.isnan(vst)):
            #    raw_input('Enter to continue')
        
        #if ((rapflag == False) and(r<2.0*self.Rmaxi[i])):
        #    print 'vs',vs,'vst',vst,'vmi',self.vmi[i],'wm2rad',wm2rad,'cos',np.cos(wm2rad),self.vmi[i] * np.cos(wm2rad),vs + self.vmi[i] * np.cos(wm2rad),'i',i,'wi',wi,'wj',wj,rapflag
        #    print 'RAP_mi',self.RAP_mi[i],'r',r,'Vmax',self.Vmaxi_ms[i],'Rmax',self.Rmaxi[i]
        #print 'r',r,'theta',theta,'thetatang',thetatang,'wg lat',wg.latv[wi,wj],'wg lon',wg.lonv[wi,wj],'x',xp,'y',yp
        #print 'thetai',self.thetai[i],'wm2rad',wm2rad,'vs',vs,'vmi',self.vmi[i],'vst',vst,'cos wm2rad',np.cos(wm2rad)
        
        #print 'wlat',wg.latv[wi,wj],'wlon',wg.lonv[wi,wj],'theta',theta,'theta2',theta2,'thetatang',thetatang,'thetai',self.thetai[i],'lati',self.lati[i],'loni',self.loni[i],'x',xp,'y',yp
        #raw_input('Enter to continue')
            
        
        
        
        
     
     
        
        