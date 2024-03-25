# TotalBattle.bot

A TotalBattle bot to keep stats about gifts

![Screenshot](docs/screenshot.png?raw=true "Screenshot")

## Configuration

#### config/gift-score.csv

Gift Scores

#### config/ocr-fix-gift-content.csv
#### config/ocr-fix-gift-from.csv
#### config/ocr-fix-gift-name.csv
#### config/ocr-fix-gift-source.csv

Fixes for ocr 

#### config/player-list.csv

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
```

Full tesseract-ocr

## License

Copyright (c) 2024 Grigore Stefan <g_stefan@yahoo.com>

Licensed under the [Apache License 2.0](LICENSE) license.

## Disclaimer
* This software is not affiliated or endorsed by TotalBattle
