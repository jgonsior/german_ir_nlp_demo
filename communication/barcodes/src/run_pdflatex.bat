@echo off
set FOLDER_PATH=%1
set OUTPUT_PATH=%2

if "%FOLDER_PATH%"=="" (
  echo No folder path provided.
  exit /b 1
)

for %%f in (%FOLDER_PATH%\*.tex) do (
  pdflatex -interaction=batchmode -output-path=%OUTPUT_PATH% --shell-escape %%f
)