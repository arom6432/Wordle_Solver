from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con
import random

start = False

#reads the file an dturns it into a list
file = open('wordsList.txt','r')
words = file.read()
wordsList = words.split('\n')
file.close()

#Choses a random word from the list if you would like to start with a specific word just change the value of 'startWord'
startWord = wordsList[random.randint(0,len(wordsList)-1)]
#startWord = ''

wordsList.remove(startWord)

#list of keys 
VK_CODE = {
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'enter':0x0D
}

#colors:
#Grey = (58,58,60) = 1
#Yellow = (181,159,59) = 2
#Green = (83,141,78) = 3

#List for creating the wordle array to read the colors
rows = []


def press(*args):
    #function to press keys 
    
    for i in args:
        for r in i:
            win32api.keybd_event(VK_CODE[r], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE[r],0 ,win32con.KEYEVENTF_KEYUP ,0)
            
    win32api.keybd_event(VK_CODE['enter'], 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE['enter'],0 ,win32con.KEYEVENTF_KEYUP ,0)
    
def Check_Row(row,word):
    #function to check what colors are in each point on the grid
    
    #list of letters in each color and their locations
    green = []
    yellow =[]
    grey = []

    check = [['',0],['',0],['',0],['',0],['',0]]
    for i in range(len(rows[row])):
        if pyautogui.pixel(rows[row][i][0],rows[row][i][1])[0] == 58:
            #grey = 1    
            grey.append([word[i],i])         
        elif pyautogui.pixel(rows[row][i][0],rows[row][i][1])[0] == 181:
            #yellow = 2
            yellow.append([word[i],i])
        elif pyautogui.pixel(rows[row][i][0],rows[row][i][1])[0] == 83:
            #green
            if [word[i],i] not in green:
                green.append([word[i],i])

    greyR = []
    for g in green:
        for r in grey:
            if g[0] == r[0] and r not in greyR:
                yellow.append(g)
                greyR.append(r)
    for y in yellow:
        for g in grey:
            if y[0] == g[0] and g not in greyR:
                greyR.append(g)        
    for i in greyR:
        grey.remove(i)
        
    for i in grey:
        check[i[1]][0] = i[0]
        check[i[1]][1] = 1
    for i in yellow:
        check[i[1]][0] = i[0]
        check[i[1]][1] = 2
    for i in green:
        check[i[1]][0] = i[0]
        check[i[1]][1] = 3
    remove = []
    for i in range(len(check)):
        if check[i][1] == 1:
            for w in wordsList:
                if check[i][0] in w and w not in remove:
                    remove.append(w)

        if check[i][1] == 2:
            for w in wordsList:
                if check[i][0] not in w and w not in remove:
                    remove.append(w)
                if check[i][0] ==  w[i] and w not in remove:
                    
                    remove.append(w)
        if check[i][1] == 3:
            for w in wordsList:
                if check[i][0] != w[i] and w not in remove:
                    remove.append(w)
    for i in remove:
        wordsList.remove(i)
                    
        
            

def calibrate():
    x = []
    y = []  
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
    while True:
        
        
        a = win32api.GetKeyState(0x01)

        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                pass
            else:
                print('Left Click')
                if len(x) < 5 :
                    x.append(pyautogui.position()[0])
                    
                elif len(x) >= 5 and len(y) < 6:
                    y.append(pyautogui.position()[1])
                    
                if len(y) == 6:
                    
                    break                                       
        time.sleep(0.001)
    for i in y:
        row = []
        for r in x:
            row.append((r,i))
        rows.append(row)


def start(): 
    time.sleep(5.0)
    press(list(startWord))
    time.sleep(2.0)
    print(len(wordsList))
    Check_Row(0,startWord)
    print(len(wordsList))

    for i in range(5):
        press(list(wordsList[0]))
        print('next row')
        time.sleep(3.0)

        print(len(wordsList))
        Check_Row(i+1,wordsList[0])
        print(len(wordsList))

    

print('Click enter to start. Once start click on all the top left corners of all the boxes on the top row and then do the same for the first column to calibrate the script')
state_enter = win32api.GetKeyState(VK_CODE['enter'])
while True:
        
        
        a = win32api.GetKeyState(VK_CODE['enter'])

        if a != state_enter:  # Button state changed
            state_enter = a
            if a < 0:
                pass
            else:
                print('enter')
                break
            time.sleep(0.001)


calibrate()
start()

