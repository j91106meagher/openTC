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
            
            
            