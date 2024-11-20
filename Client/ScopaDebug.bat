@echo off

@echo off
mode con:cols=80 lines=25

setlocal enabledelayedexpansion

REM Imposta la cartella che vuoi controllare
set targetPath=C:\Percorso\Da\Controllare

REM Inizializza il contatore
set count=0

REM Usa WMIC per elencare tutti i cmd.exe con la directory corrente
for /f "tokens=*" %%A in ('wmic process where "name='cmd.exe'" get CommandLine ^| findstr /i /c:"%targetPath%"') do (
    set /a count+=1
)

REM Mostra il numero di cmd.exe avviati nella directory specifica
title player %count%

:: Continua con il resto del codice...
python .\main.py
pause