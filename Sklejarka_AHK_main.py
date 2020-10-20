#!/usr/bin/python

import sys
import configparser
import errno
import re
import subprocess
import webbrowser
from datetime import datetime
from os import read, makedirs, startfile
from os.path import basename, abspath, dirname, exists, splitext
from pathlib import Path
from chardet import UniversalDetector
from my_functions import CreateIniFile, Index_Folders_of_Files_of_Interest


wersja = '2.0'
srclang = ''
# 0. parametry pliku .ini
inicontent = '[Info]\n### plik konfiguracyjny narzędzia ' + basename(__file__) + ' ###\n' \
                '# Autor: Piotr Wielecki\n# Wersja: ' + wersja + ', październik 2020 r.\n' \
                    '# Wyłączność użytkowania: REDDO Translations\n\n' \
                        '[Dirs]\n# domyślne ścieżki:\n' \
                        'lookup_dir=-->Tu należy wpisać przeszukiwaną ścieżkę<--\n' \
                        'final_dir=-->Tu należy podać ścieżkę docelową<--\n\n' \
                        '[Odrobaczanie]\n' \
                        '# może mieć wartość Boole’a albo liczbową; wówczas jest to liczba sekund wyświetlania odrobaczających okien informacyjnych.\n\n' \
                        'debug=False\n;msgboxtime=0\n\n### koniec pliku ###'
config_file_name = basename(splitext(__file__)[0]) + '.ini'
"""
def CreateIniFile(inicontent, filename=''):
    if filename == '':
        filename = basename(splitext(__file__)[0])
    try:
        with open(filename + '.ini', 'x') as ini:
            ini.write(inicontent)
        print(f'Przy pierwszym uruchomieniu należy ustawić\nścieżkę źródłową i docelową w pliku {filename}.ini.\nMożna tam też ustawiać inne parametry.\nDobrej zabawy!')
        subprocess.call(['notepad.exe', filename + '.ini'])
    except FileExistsError:
        print('Plik już istnieje')
        return
    except PermissionError:
        print('Nie udało się utworzyć pliku konfiguracyjnego.\nSprawdź uprawnienia dostępu i spróbuj ponownie.')
    return
"""
CreateIniFile(inicontent)

config = configparser.ConfigParser()
with open(config_file_name) as cf:
    config.read(config_file_name)
    lookup_dir = config.get('Dirs', 'lookup_dir', fallback='>>--folder wyszukiwania--<<')
    final_dir = config.get('Dirs', 'final_dir', fallback='>>--folder docelowy--<<')
    debug = config.get('Odrobaczanie', 'debug', fallback=False)

# print(f'Z konfigu:\n{lookup_dir}')

# funkcja gromadząca w tablicy ścieżki do wszystkich plików o wskazanym rozszerzeniu znajdujących się w danym folderze (rekurencyjnie lub nie)
# uwaga: w AHK rekurencyjność oznaczano jako 'R', w Pythonie – jako 'True'

lookup_dir = 'C:\\AutoHotKey\\Do prób\\Test Sklejarki TMX'
final_dir = 'C:\\AutoHotKey\\Do prób\\Test Sklejarki TMX docel\\'
logfile = final_dir + basename(sys.argv[0]) + '.log.txt'
print(logfile)
"""
def Index_Folders_of_Files_of_Interest(lookup_dir, extension, recursive=False):
    PathsList = []
    paths = Path(lookup_dir).glob('**/*.' + extension)
    for path in paths:
        #        print(path)
        path_in_str = str(dirname(path))
        PathsList.append(path_in_str)
    PathsList = list(set(PathsList))
    PathsList.sort()
    if len(PathsList) == 0:
        if recursive == True:
            print(f'Nie znaleziono plików .{extension} we wskazanym folderze {lookup_dir} ani w podfolderach')
        else:
            print(f'Nie znaleziono plików .{extension} we wskazanym folderze {lookup_dir}')
        return
    else:
        pass
    return PathsList
"""
log_time = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')

if not exists(dirname(logfile)):
    try:
        makedirs(dirname(logfile))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

with open(logfile, 'a', encoding='utf-8') as f:
    f.write(log_time + '\n')

PathsList = Index_Folders_of_Files_of_Interest(lookup_dir, 'tmx', True)

# logfile_directory = ''

for i in PathsList: # ta pętla kończy się na końcu skryptu niemal :o
#    print('zaczynam od' + i)
    filecount = 0
    goodfilecount = 0
    badfilecount = 0
    emptyfile_list = []

    XmlFilesContainer = []
    XmlEncodingsList = []
    first_line_list = ''
    lookup_dir = i
    logfile_directory = i
    sourcefoldername = basename(lookup_dir)
    creation_time = datetime.now().strftime('%d-%m-%Y')
    full_file_name = sourcefoldername + '_' + creation_time + '.tmx'
    #    print(full_file_name)

    # część poświęcona wykrywaniu kodowania pliku
    detector = UniversalDetector()
    searched_folders = Path(lookup_dir).glob('**/*.tmx')
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
            # koniec części poświęconej wykrywaniu kodowania pliku
            XmlEncodingsList.append(encoding)
            XmlEncodingsList = list(set(XmlEncodingsList))
            XmlEncodingsList.sort()
            if len(XmlEncodingsList) > 1:
                print(f'Kodowanie podanych plików z folderu {basename(filename)} różni się, wobec czego w obecnej wersji sklejarki nic nie zrobisz.\nWykryte rodzaje kodowania to:\n{XmlEncodingsList}')
                exit
            else:
                pass
        #                print(f'We wszystkich plikach wykryto jednakowe kodowanie:\n{XmlEncodingsList[0]}')
        filecount += 1
        with open(filename, 'r', encoding=encoding) as filecontent:
            filecontent = filecontent.read()
            filecontent = str(filecontent)
            filecontent_cripple = re.sub(r'<\?xml(.|\n)+<body>', '', filecontent) # w tych okolicach z pliku xml zostaje tylko część <body>, i to pozbawiona znaczników
            filecontent_cripple = re.sub(r'</body>', '', filecontent_cripple) # usuwa domknięcie pliku przed przyłączeniem następnego
            filecontent_cripple = re.sub(r'</tmx>', '', filecontent_cripple)
            filecontent_cripple.rstrip()
            filecontent_cripple = re.sub(r'(?<=<tuv xml:lang=\")([a-z]{2})-[a-z]{2}(?=\">)', '\1', filecontent_cripple)
            filecontent_cripple = re.sub(r'\n\n', '', filecontent_cripple)
            if re.search('<seg>.+</seg>', filecontent_cripple, re.DOTALL):
                goodfilecount += 1
                XmlFilesContainer.append(filecontent_cripple)
            else:
                emptyfile_list.append(basename(filename))
                emptyfile_list = list(set(emptyfile_list))
                emptyfile_list.sort()
                emptyfile_string = '\n'.join(emptyfile_list)
    print(f'Na złej liście jest {len(emptyfile_list)} plików')
    print(f'Zła lista:\n{emptyfile_string}')
    print(f'Na dobrej liście jest {goodfilecount} plików')
    #    print(f'Dobra lista:\n{XmlFilesContainer}')

    with open(logfile, 'a', encoding='utf-8') as f:
        if filecount == goodfilecount:
            f.write(f'\n***Folder {logfile_directory}\n\nZnaleziono plików: {filecount}\nWybrano plików: {goodfilecount}\nPołączono wszystkie pliki.\n')
        else:
            f.write(f'\n***Folder {logfile_directory}\n\nZnaleziono plików: {filecount}\nWybrano plików: {goodfilecount}\n--pozostałe pliki były puste albo nieprawidłowe\n\nLista plików, które się nie przydały ({len(emptyfile_list)}):\n\n{emptyfile_string}\n')

    if len(XmlFilesContainer) < 1:
        print(f'Nie udało się połączyć wskazanych plików.\nPoddaję się w przypadku folderu\n{i}')
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(f'***\nNie udało się [lipa] w przypadku folderu\n {i}\n***\n')

    glue_time = datetime.now().strftime('%d-%m-%Y')
    xml_opening = '<?xml version=\"1.0\" encoding=\"' + encoding + '\"?>\n<!DOCTYPE tmx SYSTEM \"tmx14.dtd\">\n<tmx version=\"1.4\">'
    inline_header_properties = '<prop type=\"defclient\"> </prop>\n\t<prop type=\"defproject\">sklejono ' + glue_time + '</prop>\n\t<prop type=\"defdomain\">various</prop>\n\t<prop type=\"defsubject\">various</prop>\n\t<prop type=\"description\"> </prop>\n'
    header = '<header creationtool=\"' + basename(__file__) + '\" creationtoolversion=\"' + wersja + '\" segtype=\"sentence\" adminlang=\"en-us\" creationid=\"REDDO_MRU\" srclang=\"' + srclang + '\" o-tmf=\"MemoQTM\" datatype=\"unknown\">\n' + inline_header_properties + '</header>\n<body>'

    target_file = final_dir + '\\' + full_file_name
    tmx_heading = xml_opening + '\n' + header
    tmx_closing = '</body>\n</tmx>'

    if exists(target_file):
        pass
    else:
        with open(target_file, 'a', encoding=encoding) as f:
            f.write(tmx_heading)
            for k in XmlFilesContainer:
                f.write(k + '\n')
            f.write(tmx_closing)
