import sqlite3
from Tkinter import *
import tkFont
conn=sqlite3.connect('speedometer.db')
c=conn.cursor()

def getValues():
	c.execute('SELECT * FROM speedoValues ORDER BY unix DESC LIMIT 1;')
	kmph=c.fetchone()[2]
	return int(kmph)

def update():
	theLabel.config(text=getValues())
	theLabel.after(1000,update)	

root=Tk()
root.title('speedometer')
root.geometry('500x500')
text1=getValues()
customFont = tkFont.Font(family="Helvetica", size=150)
theLabel=Label(root,text=text1,font=customFont)
theLabel.grid(sticky=W)
theLabel.pack(expand=True)
update()

root.mainloop()
