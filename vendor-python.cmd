@echo off
rem Created by Grigore Stefan <g_stefan@yahoo.com>
rem Public domain (Unlicense) <http://unlicense.org>
rem SPDX-FileCopyrightText: 2024 Grigore Stefan <g_stefan@yahoo.com>
rem SPDX-License-Identifier: Unlicense
rem ---
pushd %~dp0\vendor\python
set PATH=%CD%;%PATH%
popd
rem ---
python -m pip install --upgrade pip
python -m pip install wheel
python -m pip install setuptools
python -m pip install clipboard
python -m pip install pytesseract
python -m pip install opencv-python
python -m pip install pyautogui
python -m pip install easyocr
python -m pip install xlsxwriter
python -m pip install openpyxl

