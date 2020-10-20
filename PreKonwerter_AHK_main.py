#!/usr/bin/python
import configparser
import errno
import os
import re
from _datetime import datetime
import sys
from os import makedirs
from os.path import basename, splitext, exists, dirname
from pathlib import Path

from chardet import UniversalDetector
from my_functions import CreateIniFile

wersja = '2.0'
# 0. parametry pliku .ini
inicontent = '[Info]\n### plik konfiguracyjny narzędzia ' + basename(__file__) + ' ###\n' \
                '# Autor: Piotr Wielecki\n# Wersja: ' + wersja + ', październik 2020 r.\n' \
                    '# Wyłączność użytkowania: REDDO Translations\n\n' \
                        '[Dirs]\n# domyślne ścieżki:\n' \
                        'lookup_dir=-->Tu należy wpisać przeszukiwaną ścieżkę<--\n' \
                        'final_dir=-->Tu należy podać ścieżkę docelową<--\n\n' \
                        'konwerter_dir=C:\Konwerter_v3.1\Konwerter_v3.exe' \
                        '[Odrobaczanie]\n' \
                        '# może mieć wartość Boole’a albo liczbową; wówczas jest to liczba sekund wyświetlania odrobaczających okien informacyjnych.\n\n' \
                        'debug=False\n;msgboxtime=0\n\n' \
                        '[Misc]\n' \
                        'langs_with_codes=Afrikaans|AF,Akan|AK,Albanian|SQ,Amharic|AM,Arabic|AR,Aragonese|AN,Aranese|OC,Armenian|HY,Assamese|AS,Azeri|' \
                        'AZ,Basque|EU,Belarussian|BE,Bengali|BN,Bislama|BI,Bosnian|BS,Breton|BR,Bulgarian|BG,Burmese|MY,Catalan|CA,Chinese|ZH,Croatian|' \
                        'HR,Czech|CS,Danish|DA,Dutch|NL,English|EN,Esperanto|EO,Estonian|ET,Farsi|FA,Fijian|FJ,Finnish|FI,Flemish|VLS,French|FR,Frisian|' \
                        'FY,Fulah|FF,Gaelic|GD,Galician|GL,Georgian|KA,German|DE,Greek|EL,Greenlandic|KL,Guaraní|GN,Gujarati|GU,Haitian Creole|HT,Hausa|HA,Hebrew|' \
                        'HE,Hindi|HI,Hungarian|HU,Icelandic|IS,Igbo|IG,Indonesian|ID,Irish|GA,Italian|IT,Japanese|JA,Javanese|JV,Kannada|KN,Kashmiri|KS,Kazakh|' \
                        'KK,Khmer|KM,Kiribati|GIL,Korean|KO,Kurdish|KU,Kyrgyz|KY,Lao|LO,Latin|LA,Latvian|LV,Lingala|LN,Lithuanian|LT,Luxembourgish|LB,Macedonian|' \
                        'MK,Malagasy|MG,Malay|MS,Malayalam|ML,Maltese|MT,Maori|MI,Marathi|MR,Marshallese|MH,Moldavian|MO,Mongolian|MN,Montenegrin|CG,Nauruan|' \
                        'NA,Navajo|NV,Nepali|NE,Norwegian|NO,Occitan|OC,Oriya|OR,Oromo|OM,Pashto|PS,Polish|PL,Portuguese|PT,Punjabi|PA,Romanian|RO,Rundi|RN,Russian|' \
                        'RU,Rwanda|RW,Samoan|SM,Sanskrit|SA,Serbian|SR,Sesotho|ST,Sinhala|SI,Slovak|SK,Slovenian|SL,Somali|SO,Spanish|ES,Sundanese|SU,Swahili|' \
                        'SW,Swedish|SV,Tagalog|TL,Tajiki|TG,Tamil|TA,Tatar|TT,Telugu|TE,Thai|TH,Tigrigna|TI,Tongan|TO,Tswana|TN,Turkish|TR,Turkmen|TK,Twi|TW,Ukrainian|' \
                        'UA,Urdu|UR,Uzbek|UZ,Vietnamese|VI,Welsh|CY,Wolof|WO,Xhosa|XH,Yiddish|YI,Yoruba|YO,Zulu|ZU\n' \
                        '### koniec pliku ###'
config_file_name = basename(splitext(__file__)[0]) + '.ini'

CreateIniFile(inicontent)

config = configparser.ConfigParser()
with open(config_file_name) as cf:
    config.read(config_file_name)
    lookup_dir = config.get('Dir', 'lookup_dir', fallback='>>--folder wyszukiwania--<<')
    final_dir = config.get('Dirs', 'final_dir', fallback='>>--folder docelowy--<<')
    konwerter_dir = config.get('Dirs', 'konwerter_dir', fallback=False)
    langs_with_codes = config.get('Misc', 'langs_with_codes', fallback='(^English|^Polish|^German|^French')
    debug = config.get('Odrobaczanie', 'debug', fallback=False)

# funkcja gromadząca w tablicy ścieżki do wszystkich plików o wskazanym rozszerzeniu znajdujących się w danym folderze (rekurencyjnie lub nie)
# uwaga: w AHK rekurencyjność oznaczano jako 'R', w Pythonie – jako 'True'

lookup_dir = 'C:\\AutoHotKey\\Do prób\\ToKonwertuj'
final_dir = 'C:\\AutoHotKey\\Do prób'
konwerter_dir = 'C:\\Konwerter_v3.1\\Konwerter_v3.exe'
logfile = final_dir + basename(sys.argv[0]) + '.log.txt'
print(logfile)

log_time = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')

if not exists(dirname(logfile)):
    try:
        makedirs(dirname(logfile))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

with open(logfile, 'a', encoding='utf-8') as f:
    f.write(log_time + '\n')

PathsList = []
paths = Path(lookup_dir).glob('**/*.' + 'csv')
for path in paths:
 #   print(path)
    path_in_str = str(dirname(path))
    PathsList.append(path_in_str)
PathsList = list(set(PathsList))
PathsList.sort()
if len(PathsList) == 0:
    print('Nie znaleziono plików w żadnej ze ścieżek')
    exit()

langs_and_codes_list = []
regex_lang_line = '('
#print(langs_with_codes)
langs_with_codes = langs_with_codes.split(',')
for i in langs_with_codes:
    regex_lang_line += '^' + i.split('|')[0] + '|'
    langs_and_codes_list.append(i)

regex_lang_line = regex_lang_line.rstrip('|')
regex_lang_line += ')'
#koniec wyrażenia regularnego i przyporządkowywania zmiennych

for j in PathsList: # ta pętla kończy się z końcem pliku
    lookup_dir = j
    logfile_path = j
    print(f'Pierwsze okienko: ścieżka {j}')

    filesandcodes_list = []
    codeslist = []
    filecount = 0
    goodfilecount = 0
    emptyfile_list = []

    searched_folders = Path(lookup_dir).glob('**/*.csv')
    # część poświęcona wykrywaniu kodowania pliku
    detector = UniversalDetector()
    for filename in searched_folders:
        #        print(filename)
        detector.reset()
        with open(filename, 'rb') as f:
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            encoding = detector.result['encoding']
        #            print(f'Kodowanie pliku .csv to {encoding} :o')
        # koniec części poświęconej wykrywaniu kodowania pliku


        #   for filename in searched_folders:
        #        print(basename(filename))
        filename_with_langs = str(basename(filename)) + '#' # na tym etapie jeszcze bez 'langs'
        with open(filename, 'r', encoding=encoding) as f:
            headline = f.readline()
        #           print(headline)
        #            for line in f:
        #              headline = str(line)
        #             print(headline)
        filecount += 1
        #      print(f'Nagłówek:\n{headline}')
#        print(f'regex_lang_line={regex_lang_line}')
        headings = headline.split(';') # !!!na prawdziwych plikach poprawić na średnik!!!
#        print(headings)
        for c in headings:
#            print(c)
            result = re.search(regex_lang_line, c)
            if result == None:
                pass
            else:
                raw_lang = result.group()
#                print(f'tututu {raw_lang}')
                if raw_lang != '':
                    if raw_lang not in filename_with_langs:
                        filename_with_langs += raw_lang + '-'

        #       print(langs_and_codes_list)
        for i in langs_and_codes_list:
#            print(f'pozycja z lity kodów: {i}')
#            print(i.split('|')[0])
#            print(i.split('|')[1])
#            print('regex' + filename_with_langs)
            filename_with_langs = filename_with_langs.replace(i.split('|')[0], i.split('|')[1])
        filename_with_langs = filename_with_langs.rstrip('-')
        if re.search('[A-Z]{2}-[A-Z]{2}$', filename_with_langs): # żeby odsiać ew. niepotrzebne pliki
            print(f'Dopasowanie: {filename_with_langs}')
            filesandcodes_list.append(filename_with_langs) # tu powstała lista nazw plików z kodami języków tych plików
            print(filesandcodes_list)
            goodfilecount += 1
        else:
            emptyfile_list.append(basename(filename))
        newcode = filename_with_langs.split('#')[1]
        if len(newcode) > 0:
            codeslist.append(newcode.rstrip('#'))
    emptyfile_list = list(set(emptyfile_list))
    emptyfile_list.sort()
    badfilecount = len(emptyfile_list)

    with open(logfile, 'a') as log:
        if filecount == goodfilecount:
            log.write(f'***Folder {logfile_path}\n\nZnaleziono plików: {filecount}\nWybrano plików: {goodfilecount}\n'
                      f'Połączono wszystkie pliki.\n')
        else:
            log.write(f'***Folder {logfile_path}\n\nZnaleziono plików: {filecount}\nWybrano plików: {goodfilecount}\n'
                      f'--pozostałe pliki były puste albo nieprawidłowe\n\nLista plików, które się nie przydały ({badfilecount}):\n'
                      f'{emptyfile_list}\n')
    reverse_fnw_langs = []
    print(filesandcodes_list)
    for f in filesandcodes_list:
#        print('Dochodzi do tego miejsca')
        tymcz = f.split('#')
        reverse_fnw_langs.append(tymcz[1] + '#' + tymcz[0])

        codeslist = list(set(codeslist))
        codeslist.sort()
#        codeslist.ltrim(codeslist, '\n')
        print(f'Kody językowe to:\n{codeslist}')

        files_attributed_to_codes = []
        for c in codeslist:
            files_attributed_to_codes.append(c + '#')

        for c in files_attributed_to_codes:
            tymcz = c
            print(f'rewers: {reverse_fnw_langs}')
            for f in reverse_fnw_langs:
                if tymcz in f:
                    c += f.split('#')[1] + ';'
            c = c.rstrip(';')

        arg1 = lookup_dir
        sourcefoldername = basename(lookup_dir)
        print(f'Pliczki z kodami: {files_attributed_to_codes}')
        for i in files_attributed_to_codes:
            filename_init = i.split('#')[0]
            creation_time = datetime.now().strftime('%d-%m-%Y')
            full_file_name = filename_init + '_' + sourcefoldername + '_dump_' + creation_time + '.csv'
            full_final_path = final_dir + '\\' + full_file_name
            arg2 = i.split('#')[1]
            arg3 = full_final_path

            with open(logfile, 'a') as log:
                if exists(konwerter_dir):
                    liczba_plików = len(arg2.split(';'))
                    print(f'Uruchomiony zostanie konwerter pod adresem {konwerter_dir}\narg1 = {arg1}\narg2 = {arg2}\narg3 = {arg3}')
                    log.write(f'#Uruchomiono Konwerter w ścieżce {konwerter_dir}\nPrzekazano następujące argumenty:\n'
                              f'{arg1}\n{arg2}\n{arg3}\n')
 #                   os.system(f'{konwerter_dir} {arg1} {arg2} {arg3}')
                else:
                    print(f'Nie udało się uruchomić konwetera. Nie odnaleziono pliku\n{konwerter_dir}')
                    log.write(f'Nie udało się uruchomić konwetera. Nie odnaleziono pliku\n{konwerter_dir}')
                    exit()


# koniec pętli for j na końcu pliku na końcu tęczy