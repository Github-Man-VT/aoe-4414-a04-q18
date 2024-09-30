## Script Name: eci_to_ecef.py

## Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km

## Parameters:
# year: Value for year(s)
# month: Value for month(s)
# day: Value for day(s)
# hour: Value for hour(s)
# minute: Value for minute(s)
# second: Value for second(s)
# eci_x_km: X-Magnitude for ECI Vector
# eci_y_km: Y-Magnitude for ECI Vector
# eci_z_km: Z-Magnitude for ECI Vector

## Output: Converts ECI Vector into ECEF Vector

## Written by Carl Hayden

## Importing Libraries
import math
import sys # argv
import numpy

## Defining Constants
R_Earth = 6378.1363 # Radius of Earth in km
e_Earth = 0.081819221456 # Eccentricity of Earth

## Initialize Script Arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

## Parse Script Arguments
if len(sys.argv)==10:
    year = float(sys.argv[1])
    month = float(sys.argv[2])
    day = float(sys.argv[3])
    hour = float(sys.argv[4])
    minute = float(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])

else:
    print(\
        'Usage: '\
        'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
    )
    exit()

## Main Script
JD = day - 32075 + 1461 * (year+4800+(month-14)/12)/4+367*(month-2-(month-14)/12*12)/12 - 3*((year+4900+(month-14)/12)/100)/4
JD_midnight = JD - 0.5
D_fractional = (second + 60 *(month+60*hour))/86400
JD_fractional = JD_midnight + D_fractional
T_UT1 = (JD - 2451545.0)/36525.0
wVal = 7.292115 * 10**(-5)
Theta_GMST = 67310.54841 + ((876600*60*60 + 8640184.812866) * T_UT1) + (0.093104 * T_UT1**2) + (-6.2*10**(-6) * T_UT1**3)

Extra_Rad_GMST = math.fmod(Theta_GMST, 360)*wVal
Rad_GMST = math.fmod(Theta_GMST*(2*math.pi/86400), (2*math.pi))-Extra_Rad_GMST

ECI_Vect = numpy.array([[eci_x_km], [eci_y_km], [eci_z_km]])

Rotation1 = numpy.array([[math.cos(-Rad_GMST), -math.sin(-Rad_GMST), 0], 
             [math.sin(-Rad_GMST), math.cos(-Rad_GMST), 0], 
             [0, 0, 1]])

Calc1 = numpy.dot(Rotation1, ECI_Vect)

ecef_x_km = str(numpy.extract(1,Calc1[[0]]))
ecef_y_km = str(numpy.extract(1,-Calc1[[1]]))
ecef_z_km = str(numpy.extract(1,Calc1[[2]]))

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)