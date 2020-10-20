import os

arg0 = 'C:\Konwerter_v3.1\Konwerter_v3.exe'
arg1 = 'C:\AutoHotKey\Do_prób\KonwertujTo'
arg2 = 'O-2018-09020.csv;O-2018-09030.csv;O-2018-09047.csv;O-2018-09054.csv;O-2018-09064.csv;O-2018-09079.csv;O-2018-09118.csv;O-2018-09130.csv;O-2018-09135.csv;O-2018-09136.csv;O-2018-09139.csv;O-2018-09145.csv;O-2018-09152.csv;O-2018-09154.csv;O-2018-09162.csv;O-2018-09181.csv'
arg3 = 'C:\AutoHotKey\Do_prób\próbny_drugi_dump.csv'

os.system(f'{arg0} {arg1} {arg2} {arg3}')