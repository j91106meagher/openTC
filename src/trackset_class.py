import numpy as np
from tracks_class import tracks


class track_set:   

    def __init__(self):
        self.tracks = []
        self.num_tracks = []
        self.fn = []
        self.fn_path = []
        self.year = []
        self.ID = []
        
    def read_track_set_ebtrk(self,fn,fn_path):
        self.fn = fn
        self.fn_path = fn_path
        
        self.lat = np.zeros((0))
        self.lon = np.zeros((0))
        self.Vmax_knots = np.zeros((0))
        self.Vmax_ms = np.zeros((0))
        self.Pc = np.zeros((0))
        self.Rmax = np.zeros((0))
        self.RADP = np.zeros((0))
        self.RAP_m = np.zeros((0))
        
        #i = 0
        lastID = ''
        
        f = open(self.fn_path + self.fn,'r')
        trk = tracks()
        firstpass = True
        i = 0
        
        for l in f:
            
            #l = f.readline()
            l2 = l[17:]
            s = l2.split()
            s2 = l[0:17].split()
            #print s
            if ((lastID == s2[0]) or (firstpass)):
                #print 'parse1','lastID',lastID,'firstpass',firstpass
                trk.parse_line_ebtrk(s,s2)
                firstpass = False
                lastID = s2[0]
            else:
                #new storm track
                
                #print 'new storm'
                trk.trackset_type = 'EBTRK'
                trk.track = i
                trk.year = int(s[1])
                self.tracks.append(trk)
                trk = tracks()
                #print 'new trk object'
                i = i + 1
                trk.parse_line_ebtrk(s,s2)
                lastID = s2[0]
                #raw_input('Enter to continue')
                
           
        trk.trackset_type = 'EBTRK'  
        trk.track = i
        trk.year = int(s[1])              
        self.tracks.append(trk)
                        
        f.close()     
        
    def proc_tracks_ebtrk(self,dt,wg,out_path,trk_i,debug):
        
        if trk_i > 0:
            wg.vst.fill(0.0)
            wg.vst_max.fill(0.0)
            wg.vs.fill(0.0)
            self.tracks[trk_i].ebtrk_rmax()
            self.tracks[trk_i].interp_track(dt)
            self.tracks[trk_i].calc_vmi()
            self.tracks[trk_i].windfield_hs(wg,debug)
            fn_out = self.tracks[trk_i].ID[0]+'_'+str(self.tracks[trk_i].year)
            wg.save_vst_max(out_path,fn_out)
            
        else:
            for trk_i in range(len(self.tracks)):
                wg.vst.fill(0.0)
                wg.vst_max.fill(0.0)
                wg.vs.fill(0.0)
                self.tracks[trk_i].ebtrk_rmax()
                self.tracks[trk_i].interp_track(dt)
                self.tracks[trk_i].calc_vmi()
                self.tracks[trk_i].windfield_hs(wg,debug)
                fn_out = self.tracks[trk_i].ID[0]+'_'+str(self.tracks[trk_i].year)
                wg.save_vst_max(out_path,fn_out)
            
            
           
    def read_hurdat_set(self,fn,fn_path,debug):
        self.fn = fn
        self.fn_path = fn_path
        i = 0
        
        f = open(self.fn_path + self.fn,'r')
        while (True):
            try:
                trk = tracks()
                l = f.readline()
                i += 1
                if l == '': break
                s = l.split(',')
                print(i,s)
                numlines = int(s[2])
                trk.num_lines.append(numlines)
                trk.ID.append(s[0].strip())
                self.ID.append(s[0].strip())
                trk.year.append(int(s[0].strip()[-4:]))
                self.year.append(int(s[0].strip()[-4:]))
                if debug:
                    print(s,trk.year[-1])
                try:
                    trk.Name.append(s[1].strip())
                except:
                    trk.Name.append('')
                    
                #print('trk.num_lines',trk.num_lines)
                trk.read_hurdat_track(f,numlines,debug)
                self.tracks.append(trk)
                
        
            except:
                print('read_hurdat_set error')
                break
            
        f.close()
        
    def prep_tracks(self,debug):
        
        for i in range(len(self.tracks)):
            self.tracks[i].calc_deltalatlon()
            if debug:
                print('i',i,len(self.tracks[i].dlat),len(self.tracks[i].lat))
                
                
    def genesis_kernel(self,wg,year1,year2,L,debug): 
        #L = 210*1000 #length scale in meters
        #from geopy.distance import great_circle
        
        print('starting genesis_kernel','ny',wg.ny,'nx',wg.nx,'ntracks',len(self.tracks))
        
        from pyproj import Geod

        wgs84_geod = Geod(ellps='WGS84') #Distance will be measured on this ellipsoid - more accurate than a spherical method

        lat0 = np.zeros((wg.ny,wg.nx))
        lon0 = np.zeros((wg.ny,wg.nx))
        
        for i in range(len(self.tracks)):
            if ((self.year[i] >= year1)and(self.year[i] <= year2)):
                wlon = np.squeeze(wg.lonv[:,:])
                wlat = np.squeeze(wg.latv[:,:])
                
                lat0[:] = self.tracks[i].lat[0]
                lon0[:] = self.tracks[i].lon[0]
               
                az12,az21,dist = wgs84_geod.inv(wlon,wlat,lon0,lat0)
                pdist = np.exp(-1.0*dist*dist/(2.0*L*L))
                wg.track_start_prob[:,:] += pdist
                
            print(i,'of ',len(self.tracks))
        wg.track_start_prob =  wg.track_start_prob / wg.track_start_prob.sum()
        
        if debug:
            import matplotlib.pyplot as plt 
            #plt.subplot(221)
            plt.pcolormesh(wg.lonv,wg.latv,wg.track_start_prob)
            plt.title('genesis prob')
            plt.colorbar()
            plt.show()
            
            
                