# openTC
The open Tropical Cyclone project purpose is to develop and share code for tropical cyclone Nat Cat modelling

## Wind field modeling
Currently, for NatCat modeling of tropical cyclones, their wind-fields are generally described by parametric radial wind profiles, such as Holland 2010, Wood 2013 etc. The basis is to assume that the tangential winds can be approximated as a vortex. This provides a numerically straightforward algorithm for the calculation of large numbers of simulated storms. 


The parametric wind-field models take historical or simulated storms tracks as their inputs. Utilizating parameters such as Rmax, Vmax, Pc. The parametric models operate in a moving local frame with the radial distance calculated from the storm center. Hence, the tracks parameters which are in a stationary Earth frame using a latitude and longitude coordinate system need to projected into local storm frame. Track parameters are commonly reported in six hour time-steps, so they need to be also interpolated to produce smooth peak wind speed maps (footprints).
1. calculate great circle distance between interpolated track points. Calcualte storm speed from distance and interpolated time-step, along with storm bearing.
2. Calculate local catesian distance from each wind grid point to the storm center to give radial distance and angle.
3. Subtract storm translatonal speed from Vmax
4. Apply parameteric wind equations based on radial distance and adjusted track parameters*5 calculate angle between sorm bearing and radial wind vector
6. vs + vn * cos(wm2rad) add projected storm translational velocity to pure radial windspeed

A number of extra steps are required to deal with wrap around of longitude at -180 to 180, mulitples of 2pi in local frame angle calcualtions, expotential attenuation of windspeeds in the far field based on radius of last closed barometric contour (storm extent) 
    [notebook](notebooks/example_ebtrk.ipynb)


## Simulated track sets
Synethic tropical cyclone track-sets are used to fill out the historical record in terms of intensity and location of storms. Conditional random walk based on the statistics calculated on historical track sets. 
Hall & Jewson Tellus 2007, Yonekura and Hall JAMC 2011
- Cyclogensis
- Conditional randon walk for track and storm progation
- Lysis (storm termination)
- Inland filling
- Extra tropical transistion
