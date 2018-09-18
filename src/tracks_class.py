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
        
        
     
     
        
        