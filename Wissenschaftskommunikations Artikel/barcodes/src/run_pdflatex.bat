@echo off
set FOLDER_PATH=%1

if "%FOLDER_PATH%"=="" (
  echo No folder path provided.
  exit /b 1
)

for %%f in (%FOLDER_PATH%\*.tex) do (
  pdflatex --shell-escape %%f
)