import os
import subprocess
import sys

if len(sys.argv) < 3:
    print(f'Przekazano za mało argumentów ({len(sys.argv) - 1}). Powinny być dwa.\nWychodzę.')
    exit()
if len(sys.argv) > 3:
    print(f'Przekazano za dużo argumentów ({len(sys.argv) - 1}). Powinny być dwa.\nKlęska urodzaju. Wychodzę.')
    exit()
#if len(sys.argv) == 3:
lookup_dir = sys.argv[1]
final_dir = sys.argv[2]


print(len(sys.argv))
print(lookup_dir)
print(final_dir)

newfilename = 'WynikZPytona.txt'
with open(newfilename, 'w+') as f:
    f.write(f'Przekazane prawidłowo parametry ze skryptu {sys.argv[0]} to:\n'
            f'lookup_dir={lookup_dir}\nfinal_dir={final_dir}\n'
            f'Liczba przekazanych argumentów: {len(sys.argv)}')
try:
    os.system(f'notepad.exe {newfilename}')

except FileExistsError:
    print(f'Plik {newfilename} nie istnieje!')

print('działa')
