# TotalBattle.bot

A TotalBattle bot to keep stats about gifts

![Screenshot](docs/screenshot.png?raw=true "Screenshot")

## Configuration

#### config/gift-score.xlsx

Gift Scores

#### config/gift-ignore.xlsx

Gift Ignore in reports

#### config/player-ignore.xlsx

Player Ignore in reports

#### config/ocr-fix-gift-content.xlsx
#### config/ocr-fix-gift-from.xlsx
#### config/ocr-fix-gift-name.xlsx
#### config/ocr-fix-gift-source.xlsx

Fixes for ocr 

#### config/player-list.xlsx

Clan players, this is updated automatically on report generation

#### report/*

This folder will contain generated reports

#### repository/*

Main database with gifts info

#### Vendor requirements

``` shell
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
```

Full tesseract-ocr

## License

Copyright (c) 2024 Grigore Stefan <g_stefan@yahoo.com>

Licensed under the [Apache License 2.0](LICENSE) license.

## Disclaimer
* This software is not affiliated or endorsed by TotalBattle

## Commercial software with more advanced options
[Total Battle Assistant](https://total-battle-assistant.com/)
