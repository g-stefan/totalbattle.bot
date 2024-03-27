# TotalBattle.bot
# Copyright (c) 2024 Grigore Stefan <g_stefan@yahoo.com.hpp>
# Apache License 2.0 <https://opensource.org/license/apache-2-0/>
# SPDX-FileCopyrightText: 2024 Grigore Stefan <g_stefan@yahoo.com.hpp>
# SPDX-License-Identifier: Apache-2.0

#
# Version 1.1.0 2024-03-27
#

import flet
from flet import Page, Text, TextField, Switch, ElevatedButton, Row, Divider, DatePicker, TimePicker, icons, SnackBar
import threading
import cv2 as cv
import numpy as np
import pyautogui
import time
import pytesseract
from datetime import datetime, timedelta
import csv
import os.path

buttonClan01 = cv.imread("images/button-clan-01.png", cv.IMREAD_GRAYSCALE)
buttonClan02 = cv.imread("images/button-clan-02.png", cv.IMREAD_GRAYSCALE)
buttonDelete01 = cv.imread("images/button-delete-01.png", cv.IMREAD_GRAYSCALE)
buttonDelete02 = cv.imread("images/button-delete-02.png", cv.IMREAD_GRAYSCALE)
buttonGiftsActive01 = cv.imread("images/button-gifts-active-01.png", cv.IMREAD_GRAYSCALE)
buttonGiftsActive02 = cv.imread("images/button-gifts-active-02.png", cv.IMREAD_GRAYSCALE)
buttonGiftsInactive01 = cv.imread("images/button-gifts-inactive-01.png", cv.IMREAD_GRAYSCALE)
buttonGiftsInactive02 = cv.imread("images/button-gifts-inactive-02.png", cv.IMREAD_GRAYSCALE)
buttonOpen01 = cv.imread("images/button-open-01.png", cv.IMREAD_GRAYSCALE)
buttonOpen02 = cv.imread("images/button-open-02.png", cv.IMREAD_GRAYSCALE)
windowClanTitle01 = cv.imread("images/window-clan-title-01.png", cv.IMREAD_GRAYSCALE)
windowClanTitle02 = cv.imread("images/window-clan-title-02.png", cv.IMREAD_GRAYSCALE)
# ---
screenIs4K = False
screenShotRGB = None
screenShotGray = None
cropImage = None
# ---
topX=0
topY=0
posXMouseDelta=0
posYMouseDelta=0
posXMouse=0
posYMouse=0
# ---
giftsCaptureRegionX=0
giftsCaptureRegionY=0
giftsCaptureRegionLnX=0
giftsCaptureRegionLnY=0
# ---
giftNameRegionX=0
giftNameRegionY=0
giftNameRegionLnX=0
giftNameRegionLnY=0
# ---
giftFromRegionX=0
giftFromRegionY=0
giftFromRegionLnX=0
giftFromRegionLnY=0
# ---
giftSourceRegionX=0
giftSourceRegionY=0
giftSourceRegionLnX=0
giftSourceRegionLnY=0
# ---
giftContainsRegionX=0
giftContainsRegionY=0
giftContainsRegionLnX=0
giftContainsRegionLnY=0
# ---
threadStarted=False
stopProcessing=False
processingDone=False

def getScreenshot():
    global screenShotRGB,screenShotGray
    screenShotRGB=cv.cvtColor(np.array(pyautogui.screenshot()),cv.COLOR_RGB2BGR)
    screenShotGray=cv.cvtColor(screenShotRGB,cv.COLOR_RGB2GRAY)

def getScreenshotX(x,y,lnX,lnY):
    global screenShotRGB,screenShotGray
    screenShotRGB=cv.cvtColor(np.array(pyautogui.screenshot(region=(int(x),int(y),int(lnX),int(lnY)))),cv.COLOR_RGB2BGR)
    screenShotGray=cv.cvtColor(screenShotRGB,cv.COLOR_RGB2GRAY)    

def matchImage(image):
    global screenShotGray,screenShotRGB,topX,topY,posXMouse,posYMouse
    w, h = image.shape[::-1]
    res = cv.matchTemplate(screenShotGray,image,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= 0.8)    
    found = False
    for pt in zip(*loc[::-1]):        
        topX=int(pt[0])
        topY=int(pt[1])
        posXMouse=int(pt[0] + w/2)
        posYMouse=int(pt[1] + h/2)
        cv.rectangle(screenShotRGB, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        found = True
        break    
    return found

def saveGiftsCaptureRegion():
    global giftsCaptureRegionX,giftsCaptureRegionY,giftsCaptureRegionLnX,giftsCaptureRegionLnY
    global giftNameRegionX,giftNameRegionY,giftNameRegionLnX,giftNameRegionLnY
    global giftFromRegionX,giftFromRegionY,giftFromRegionLnX,giftFromRegionLnY
    global giftSourceRegionX,giftSourceRegionY,giftSourceRegionLnX,giftSourceRegionLnY
    global giftContainsRegionX,giftContainsRegionY,giftContainsRegionLnX,giftContainsRegionLnY

    global posXMouseDelta,posYMouseDelta
    # ---
    giftsCaptureRegionX=topX-36
    giftsCaptureRegionY=topY+110
    giftsCaptureRegionLnX=625
    giftsCaptureRegionLnY=94
    # --- 
    giftNameRegionX=4
    giftNameRegionY=4
    giftNameRegionLnX=404
    giftNameRegionLnY=31
    # ---
    giftFromRegionX=48
    giftFromRegionY=37
    giftFromRegionLnX=392
    giftFromRegionLnY=21
    # ---
    giftSourceRegionX=57
    giftSourceRegionY=58
    giftSourceRegionLnX=375
    giftSourceRegionLnY=20
    # ---
    giftContainsRegionX=70
    giftContainsRegionY=77
    giftContainsRegionLnX=421
    giftContainsRegionLnY=17
    # ---
    posXMouseDelta=giftsCaptureRegionX
    posYMouseDelta=giftsCaptureRegionY
    # ---

def getGiftScreenshot():
    global giftsCaptureRegionX,giftsCaptureRegionY,giftsCaptureRegionLnX,giftsCaptureRegionLnY
    getScreenshotX(giftsCaptureRegionX,giftsCaptureRegionY,giftsCaptureRegionLnX,giftsCaptureRegionLnY)

def saveScreenshot(info):
    global screenShotRGB
    cv.imwrite(info+"-screenshot.png",screenShotRGB)

def saveCropImage(info):
    global cropImage
    cv.imwrite(info+"-crop.png",cropImage)

def clickX():
    global posXMouse,posYMouse,posXMouseDelta,posYMouseDelta
    pyautogui.moveTo(int(posXMouse+posXMouseDelta),int(posYMouse+posYMouseDelta),0.2)
    pyautogui.click(int(posXMouse+posXMouseDelta),int(posYMouse+posYMouseDelta))

def clickAt(x,y):
    pyautogui.moveTo(int(posXMouse+posXMouseDelta),int(posYMouse+posYMouseDelta),0.2)
    pyautogui.click(int(x),int(y))

def ocr(image,x,y,lnX,lnY):
    global cropImage
    cropImage = image[y:y+lnY, x:x+lnX]
    text = pytesseract.image_to_string(cropImage, config="--psm 12 --oem 1")
    return text

def getGiftName():
    global screenShotGray
    global giftNameRegionX,giftNameRegionY,giftNameRegionLnX,giftNameRegionLnY
    text = ocr(screenShotGray,giftNameRegionX,giftNameRegionY,giftNameRegionLnX,giftNameRegionLnY)
    text = text.strip()
    return text

def getGiftFrom():
    global screenShotGray
    global giftFromRegionX,giftFromRegionY,giftFromRegionLnX,giftFromRegionLnY
    text = ocr(screenShotGray,giftFromRegionX,giftFromRegionY,giftFromRegionLnX,giftFromRegionLnY)
    text = text.strip()
    return text

def getGiftSource():
    global screenShotGray
    global giftSourceRegionX,giftSourceRegionY,giftSourceRegionLnX,giftSourceRegionLnY
    text = ocr(screenShotGray,giftSourceRegionX,giftSourceRegionY,giftSourceRegionLnX,giftSourceRegionLnY)
    text = text.strip()
    return text

def getGiftContains():
    global screenShotGray
    global giftContainsRegionX,giftContainsRegionY,giftContainsRegionLnX,giftContainsRegionLnY
    text = ocr(screenShotGray,giftContainsRegionX,giftContainsRegionY,giftContainsRegionLnX,giftContainsRegionLnY)
    text = text.strip()
    return text

def matchImageWindowClanTitle():
    global screenIs4K
    global windowClanTitle01,windowClanTitle02
    if screenIs4K: return matchImage(windowClanTitle02)
    return matchImage(windowClanTitle01)

def matchImageButtonClan():
    global screenIs4K
    global buttonClan01,buttonClan02
    if screenIs4K: return matchImage(buttonClan02)
    return matchImage(buttonClan01)

def matchImageButtonGiftsActive():
    global screenIs4K
    global buttonGiftsActive01,buttonGiftsActive02
    if screenIs4K: return matchImage(buttonGiftsActive02)
    return matchImage(buttonGiftsActive01)
    
def matchImageButtonGiftsInactive():
    global screenIs4K
    global buttonGiftsInactive01,buttonGiftsInactive02
    if screenIs4K: return matchImage(buttonGiftsInactive02)
    return matchImage(buttonGiftsInactive01)

def matchImageButtonDelete():
    global screenIs4K
    global buttonDelete01,buttonDelete02
    if screenIs4K: return matchImage(buttonDelete02)
    return matchImage(buttonDelete01)

def matchImageButtonOpen():
    global screenIs4K
    global buttonOpen01,buttonOpen02
    if screenIs4K: return matchImage(buttonOpen02)
    return matchImage(buttonOpen01)

# ---
tableOcrFixGiftContent=[]

def ocrFixGiftContentLoad():
    global tableOcrFixGiftContent
    tableOcrFixGiftContent=[]
    filename="./config/ocr-fix-gift-content.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableOcrFixGiftContent.append(row)
    #print(tableOcrFixGiftContent)

def ocrFixGiftContent(value):
    global tableOcrFixGiftContent
    for item in tableOcrFixGiftContent:
        if item[0] == value:
            return item[1].strip()
    return value.strip()
    
# ---
tableOcrFixGiftFrom=[]

def ocrFixGiftFromLoad():
    global tableOcrFixGiftFrom
    tableOcrFixGiftFrom=[]
    filename="./config/ocr-fix-gift-from.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableOcrFixGiftFrom.append(row)
    #print(tableOcrFixGiftFrom)

def ocrFixGiftFrom(value):
    global tableOcrFixGiftFrom
    for item in tableOcrFixGiftFrom:
        if item[0] == value:
            return item[1].strip()
    return value.strip()

# ---
tableOcrFixGiftName=[]

def ocrFixGiftNameLoad():
    global tableOcrFixGiftName
    tableOcrFixGiftName=[]
    filename="./config/ocr-fix-gift-name.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableOcrFixGiftName.append(row)
    #print(tableOcrFixGiftName)

def ocrFixGiftName(value):
    global tableOcrFixGiftName
    for item in tableOcrFixGiftName:
        if item[0] == value:
            return item[1].strip()
    return value.strip()

# ---
tableOcrFixGiftSource=[]

def ocrFixGiftSourceLoad():
    global tableOcrFixGiftSource
    tableOcrFixGiftSource=[]
    filename="./config/ocr-fix-gift-source.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableOcrFixGiftSource.append(row)
    #print(tableOcrFixGiftSource)

def ocrFixGiftSource(value):
    global tableOcrFixGiftSource
    for item in tableOcrFixGiftSource:
        if item[0] == value:
            return item[1].strip()
    return value.strip()

# ---
tableGiftScore=[]

def giftScoreLoad():
    global tableGiftScore
    tableGiftScore=[]
    filename="./config/gift-score.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableGiftScore.append(row)
    #print(tableGiftScore)

def getGiftScore(value):
    global tableGiftScore
    for item in tableGiftScore:
        if item[0].lower() == value.lower():
            return int(item[1].strip())
    return 0

# ---
tablePlayerList=[]

def playerListLoad():
    global tablePlayerList
    tablePlayerList=[]
    filename="./config/player-list.csv"
    if os.path.isfile(filename):
        with open(filename, newline='') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
            next(csvReader)
            for row in csvReader:
                if len(row) == 0:
                    continue
                tablePlayerList.append(row)
    #print(tablePlayerList)
                        
def playerListSave():
    global tablePlayerList
    filename="./config/player-list.csv"
    with open(filename, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
        csvWriter.writerow(["Player"])
        for row in tablePlayerList:
            csvWriter.writerow(row)

# ---
def sortSecond(val):    
    return val[1]
# ---
tableGiftIgnore=[]

def giftIgnoreLoad():
    global tableGiftIgnore
    tableGiftIgnore=[]
    filename="./config/gift-ignore.csv"
    if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    next(csvReader)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        tableGiftIgnore.append(row)
    #print(tableGiftIgnore)

def giftIgnore(value):
    global tableGiftIgnore
    for item in tableGiftIgnore:
        if item[0].lower() == value.lower():
            return True
    return False

# ---

def main(page: Page):
    global stopProcessing,processingDone,threadStarted,screenIs4K
    page.window_width = 360
    page.window_height = 600 
    page.title = "TotalBatttle.bot"
    page.vertical_alignment = "top"    

    status = Text("ready")
    stopProcessing = False
    processingDone = False
    screenIs4K = False

    txtNumber = TextField(value="100", text_align="right", width=100)
    switch4K = Switch(label="Display is 4k", value=screenIs4K)

    def threadProc():
        global stopProcessing, processingDone,threadStarted
        global posXMouse,posYMouse,posXMouseDelta,posYMouseDelta
        threadStarted = True
        status.value = "starting up ..."        
        page.update()
        time.sleep(1)
        count = 0
        countLN = int(txtNumber.value)
        while not stopProcessing:
            time.sleep(1)
            posXMouse = 0
            posYMouse = 0
            posXMouseDelta = 0
            posYMouseDelta = 0
            getScreenshot()            
            #saveScreenshot("main")
            if not matchImageWindowClanTitle():
                #saveScreenshot("no-wnd-clan")
                status.value = "no clan window found"
                time.sleep(3)                
                if not matchImageButtonClan():
                    #saveScreenshot("no-clan-btn")
                    status.value = "no clan button found"
                    page.update()
                    stopProcessing = True
                    processingDone = True                
                    threadStarted = False
                    return
                status.value = "click clan button"
                page.update()
                clickX()                
                time.sleep(1)
                pyautogui.move(50, 50, 0.5)
                time.sleep(1)
                continue
            saveGiftsCaptureRegion()            
            if not matchImageButtonGiftsActive():
                if not matchImageButtonGiftsInactive():
                    status.value = "no gifts button found"
                    page.update()
                    stopProcessing = True
                    processingDone = True                
                    threadStarted = False
                    return
                status.value = "click gifts button"
                page.update()               
                clickX()
                time.sleep(1)
                pyautogui.move(50, 50, 0.5)
                time.sleep(1)
                continue
            while not stopProcessing:
                status.value = "process gift ..."
                page.update()                
                getGiftScreenshot()
                isDeleted = False
                if matchImageButtonDelete():
                    isDeleted = True
                if not matchImageButtonOpen():
                    if not isDeleted:
                        #saveScreenshot("open-1")
                        status.value = "no more gifts, done"
                        page.update()
                        time.sleep(2)
                        stopProcessing=True
                        break
                
                dateNow = datetime.now()
                giftDate = dateNow.strftime("%Y-%m-%d %H:%M:%S")
                dateDay = dateNow.strftime("%Y-%m-%d")

                #saveScreenshot("gift") 
                giftFrom = getGiftFrom()
                if giftFrom == "":
                    saveScreenshot("./errors/"+dateNow.strftime("%Y-%m-%d_%H-%M-%S_"))
                    saveCropImage("./errors/"+dateNow.strftime("%Y-%m-%d_%H-%M-%S_"))
                    status.value = "OCR Error - Gift From"
                    page.update()
                    return
                giftName = getGiftName()                
                giftSource = getGiftSource()
                giftContains = "unknown"
                giftStatus = "Ok"
                if isDeleted:
                    giftContains = getGiftContains()
                    giftStatus = "Deleted"
                #print("Gift Name: "+giftName)
                #print("Gift From: "+giftFrom)
                #print("Gift Source: "+giftSource)                                
                fileName = "./repository/"+dateDay+"-chest-info.csv"
                outFile = open(fileName, "a")
                outFile.write("\""+giftDate+"\",\""+giftFrom+"\",\""+giftName+"\",\""+giftSource+"\",\""+giftContains+"\",\""+giftStatus+"\"\n")
                outFile.close()
                #---
                count = count + 1
                status.value = "["+str(count)+"/"+str(countLN)+"] "+giftFrom+", "+giftName
                page.update()                
                #---
                clickX()
                #print("ClickX: "+str(int(posXMouse+posXMouseDelta))+" Y:"+str(int(posYMouse+posYMouseDelta)))
                time.sleep(25/1000)
                pyautogui.move(50, 50, 25/1000)
                # ---                     
                if count >= countLN:
                    break
                # --- next
            break
        status.value = "done"
        page.update()  
        stopProcessing = True
        processingDone = True                
        threadStarted = False

    def getChests(e):
        global stopProcessing, processingDone, threadStarted,screenIs4K
        page.update()
        if threadStarted:
            page.update()
            return
        screenIs4K=switch4K.value
        threadStarted = True
        stopProcessing = False
        processingDone = False
        status.value = "preparing"
        page.update()
        (threading.Timer(1.0,threadProc)).start()        

    def stopProcess(e):
        global stopProcessing, processingDone
        stopProcessing = True
        page.update()

        
    # ---
    dateStart = datetime.now() #(datetime.now()-timedelta(days=1))
    dateStartText = dateStart.strftime("%Y-%m-%d")

    async def changeDateStart(e):
        dateStart=datepickerStart.value        
        txtDateStart.value= dateStart.strftime("%Y-%m-%d")
        e.control.page.update()

    datepickerStart = DatePicker(value=dateStart,on_change=changeDateStart)
    txtDateStart = TextField(value=dateStartText, text_align="center", width=120)

    async def openStartDatePicker(e):
            datepickerStart.pick_date()            
    
    buttonPickStartDate = ElevatedButton(
                    "Pick start date",
                    icon=icons.CALENDAR_MONTH,
                    on_click=openStartDatePicker,
                    width=180
                )
    
    # ---
    dateEnd = datetime.now() #(datetime.now()-timedelta(days=1))
    dateEndText = dateEnd.strftime("%Y-%m-%d")

    async def changeDateEnd(e):
        dateEnd=datepickerEnd.value        
        txtDateEnd.value= dateEnd.strftime("%Y-%m-%d")
        e.control.page.update()

    datepickerEnd = DatePicker(value=dateEnd,on_change=changeDateEnd)
    txtDateEnd = TextField(value=dateEndText, text_align="center", width=120)

    async def openEndDatePicker(e):    
            datepickerEnd.pick_date()            
    
    buttonPickEndDate = ElevatedButton(
                    "Pick end date",
                    icon=icons.CALENDAR_MONTH,
                    on_click=openEndDatePicker,
                    width=180
                )
    # ---
    def cmdButtonSubmit(e):
        strDateStart=txtDateStart.value
        strDateEnd=txtDateEnd.value
        if strDateEnd < strDateStart:
            strDateStart=txtDateEnd.value
            strDateEnd=txtDateStart.value
        dateStart = datetime.strptime(strDateStart,"%Y-%m-%d")
        dateEnd = datetime.strptime(strDateEnd,"%Y-%m-%d")
        dateList = []
        while dateStart <= dateEnd:
            dateList.append(dateStart)
            dateStart += timedelta(days=1)
        giftsTable=[]
        for day in dateList:
            filename="./repository/"+day.strftime("%Y-%m-%d")+"-chest-info.csv"
            if os.path.isfile(filename):
                with open(filename, newline='') as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    for row in csvReader:
                        if len(row) == 0:
                            continue
                        giftsTable.append(row)
        #print(giftsTable)        
        ocrFixGiftContentLoad()
        ocrFixGiftFromLoad()
        ocrFixGiftNameLoad()
        ocrFixGiftSourceLoad()
        giftScoreLoad()
        playerListLoad()
        giftIgnoreLoad()

        playerStats={}        
        giftsTableFinal=[]
        giftsTableFinal.append(["Date","Player","Name","Source","Content","Status","Score"])
        for line in giftsTable:
            if len(line)==0:
                continue
            giftFrom = ocrFixGiftFrom(line[1])
            giftName = ocrFixGiftName(line[2])
            giftSource = ocrFixGiftSource(line[3])
            giftContains = ocrFixGiftContent(line[4])
            giftScore = getGiftScore(giftSource)

            giftsTableFinal.append([line[0],giftFrom,giftName,giftSource,giftContains,line[5],giftScore])
            if giftIgnore(giftName):
               continue

            if not giftFrom in playerStats:
                playerStats[giftFrom]=["",0,0,False]            
            
            playerStats[giftFrom][0]=giftFrom
            playerStats[giftFrom][1]+=giftScore
            playerStats[giftFrom][2]+=1            

        reportDate=datetime.now().strftime("%Y-%m-%d")
        filename="./report/"+reportDate+"-chest-info.csv"
        with open(filename, 'w', newline='') as csvFile:
                    csvWriter = csv.writer(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    for row in giftsTableFinal:                        
                        csvWriter.writerow(row)
        
        # ---
        playerStatsSort = []        
        for player in playerStats:
             playerStatsSort.append([playerStats[player][0],playerStats[player][1],playerStats[player][2]])
        playerStatsSort.sort(key=sortSecond) 
        playerStatsSort.reverse()

        # ---
        playerStatsTable = []
        playerStatsTable.append(["Player","Score","Count"])
        for line in playerStatsSort:
             playerStatsTable.append(line)

        filename="./report/"+reportDate+"-player-top.csv"
        with open(filename, 'w', newline='') as csvFile:
                    csvWriter = csv.writer(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
                    for row in playerStatsTable:
                        csvWriter.writerow(row)

        # ---
        global tablePlayerList

        playerInfoTable=[]
        playerInfoTable.append(["Player","Score","Count"])
        playerNoGifts=[]
        playerNoGifts.append(["Player"])
        for line in tablePlayerList:
            player = line[0]
            if player in playerStats:
                playerInfoTable.append([playerStats[player][0],playerStats[player][1],playerStats[player][2]])
                playerStats[player][3]=True
            else:
                playerInfoTable.append([player,0,0])
                playerNoGifts.append([player])

        for player in playerStats:
             if not playerStats[player][3]:
                  tablePlayerList.append([player])
                  playerInfoTable.append([playerStats[player][0],playerStats[player][1],playerStats[player][2]])                  

        playerListSave()

        filename="./report/"+reportDate+"-player-stats.csv"
        with open(filename, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
            for row in playerInfoTable:
                csvWriter.writerow(row)

        filename="./report/"+reportDate+"-player-no-gifts.csv"
        with open(filename, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=',', quotechar='\"',quoting=csv.QUOTE_ALL)
            for row in playerNoGifts:
                csvWriter.writerow(row)

        e.control.page.snack_bar = SnackBar(Text("Report done!"))
        e.control.page.snack_bar.open = True
        e.control.page.update()
        return
    
    buttonSubmit = ElevatedButton(text="Submit", on_click=cmdButtonSubmit)
    # ---

    page.add(
        Row(
            [
                ElevatedButton(text="Get Chests", on_click=getChests),                
            ],
            alignment="center",
        ),
        Row(
            [
                ElevatedButton(text="Stop", on_click=stopProcess),
            ],
            alignment="center",
        ),
        Row(
            [
                Text("Status:"),
                status,
            ],
            alignment="left",
        ),
        Row(
            [
                Text("Count:"),
                txtNumber,
            ],
            alignment="left",
        ),
        Row(
            [
                switch4K
            ],
            alignment="left",
        ),
        Divider(),
        Row(
            [
                Text("Report"),
            ],
            alignment="left",
        ),
        Row(
            [
                datepickerStart,
                buttonPickStartDate,
                txtDateStart
            ],
            alignment="left",
        ),
        Row(
            [
                datepickerEnd,
                buttonPickEndDate,
                txtDateEnd
            ],
            alignment="left",
        ),
        Row(
            [
                buttonSubmit
            ],
            alignment="left",
        )        
        )


flet.app(target=main)
