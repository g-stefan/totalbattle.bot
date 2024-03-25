@echo off
rem Created by Grigore Stefan <g_stefan@yahoo.com>
rem Public domain (Unlicense) <http://unlicense.org>
rem SPDX-FileCopyrightText: 2024 Grigore Stefan <g_stefan@yahoo.com>
rem SPDX-License-Identifier: Unlicense
rem ---
pushd %~dp0\vendor\python
set PATH=%CD%;%PATH%
popd
pushd %~dp0\vendor\tesseract
set PATH=%CD%;%PATH%
popd
rem ---
start "" pythonw .\totalbattle-bot.py
