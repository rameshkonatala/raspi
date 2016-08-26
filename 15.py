import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import urllib2
import json

import pandas as pd
import numpy as np
import sys

proxy = urllib2.ProxyHandler({'http': '172.20.0.98:8080','https': '172.20.0.98:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen


small_font=("Helvetica",8)
large_font=("Helvetica",12)
norm_font=("Helvetica",10)
style.use("ggplot")


f=Figure()
a=f.add_subplot(111)

exchange="BTC-e"
DatCounter=9000
programName='btce'

resampleSize="15Min"
dataPace="1d"
candleWidth=0.008

def changeExchange(toWhat,pn):
	global exchange
	global DatCounter
	global programName

	exchange=toWhat
	programName=pn
	DatCounter=9000

def changeTimeFrame(tf):
	global dataPace
	global DatCounter

	if tf=="7d" and resampleSize=="1Min":
		popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC")

	else:
		dataPace=tf
		DatCounter=9000

def changeSampleSize(size,width):
	global resampleSize
	global DatCounter
	global candleWidth
	if dataPace=="7d" and resampleSize=="1Min":
		popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC")

	elif dataPace=="tick":
		popupmsg("You're currently viewing tick data, not OHLC.")

	else:
		resampleSize=size
		DatCounter=9000
		candleWidth=width





def popupmsg(msg):

	popup=tk.Tk()
	popup.wn_title("!")
	label=ttk.Label(popup,text=msg,font=norm_font)
	label.pack(side="top",fill="x",pady=10)
	B1 = ttk.Button(popup,text="Okay")
	B1.pack()
	popup.mainloop()

def animate(i):
	dataLink='https://btc-e.com/api/3/trades/btc_usd?limit=2000'
	data = urllib2.urlopen(dataLink).read()
	data=data.decode("utf-8")
	data=json.loads(data)
	data=data["btc_usd"]
	data=pd.DataFrame(data)
	buys=data[(data['type']=='bid')]
	buys['datestamp']=np.array(buys['timestamp']).astype('datetime64[s]')
	buyDates=(buys['datestamp']).tolist()

	sells=data[(data['type']=='ask')]
	sells['datestamp']=np.array(sells['timestamp']).astype('datetime64[s]')
	sellDates=(sells['datestamp']).tolist()
	
	a.clear()
	a.plot_date(buyDates,buys['price'],"#00A3E0",label="buys")
	a.plot_date(sellDates,sells['price'],"#183A47",label="sells")
	a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=3,ncol=2,borderaxespad=0)
	a.set_title("BTC-e BTCUSD prices\nLast PRice: "+str(data["price"][1999]))


class seaofBTCapp(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		#tk.Tk.iconbitmap(self,default='@/home/ramesh/Desktop/tkinter/person.xbm')
		tk.Tk.wm_title(self,"Sea of BTC client")
		container=tk.Frame(self)
		container.pack(side="top",fill="both",expand="True")
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		menubar=tk.Menu(container)
		filemenu=tk.Menu(menubar,tearoff=0)
		filemenu.add_command(label="Save settings",command=lambda: popupmsg("Not suported just yet!"))
		filemenu.add_separator()
		filemenu.add_command(label="Exit",command=quit)
		menubar.add_cascade(label="File",menu=filemenu)


		exchangeChoice=tk.Menu(menubar,tearoff=1)
		exchangeChoice.add_command(label="BTC-e",command=lambda: changeExchange("BTC-e","btce"))
		exchangeChoice.add_command(label="Bitfinex",command=lambda: changeExchange("Bitfinex","bitfinex"))
		exchangeChoice.add_command(label="Bitstamp",command=lambda: changeExchange("Bitstamp","bitstamp"))
		exchangeChoice.add_command(label="Huobi",command=lambda: changeExchange("Huobi","huobi"))
		menubar.add_cascade(label="Exchange",menu=exchangeChoice)

		dataTF=tk.Menu(menubar,tearoff=1)
		dataTF.add_command(label="Tick",
			command=lambda: changeTimeFrame('tick'))
		dataTF.add_command(label="1 Day",
			command=lambda: changeTimeFrame('1d'))
		dataTF.add_command(label="2 Day",
			command=lambda: changeTimeFrame('3d'))
		
		dataTF.add_command(label="3 Day",
			command=lambda: changeTimeFrame('7d'))
		menubar.add_cascade(label="Data Time Frame",menu=dataTF)

		OHLCI = tk.Menu(menubar,tearoff=1)
		OHLCI.add_command(label="Tick",
			command=lambda: changeTimeFrame('tick'))
		OHLCI.add_command(label="1 minute",
			command=lambda: changeSampleSize('1Min',0.0005))
		OHLCI.add_command(label="5 minute",
			command=lambda: changeSampleSize('5Min',0.003))
		OHLCI.add_command(label="15 minute",
			command=lambda: changeSampleSize('15Min',0.008))
		OHLCI.add_command(label="30 minute",
			command=lambda: changeSampleSize('30Min',0.016))
		OHLCI.add_command(label="1 Hour",
			command=lambda: changeSampleSize('1H',0.032))
		OHLCI.add_command(label="3 Hour",
			command=lambda: changeSampleSize('3H',0.096))

		menubar.add_cascade(label="OHLC Interval",menu=OHLCI)

		topIndi=tk.menu(menubar,tearoff=1)
		topIndi.add_command(label="None",command=lambda: addTopIndiacator('none'))
		topIndi.add_command(label="RSI",command=lambda: addTopIndiacator('none'))
		topIndi.add_command(label="MACD",command=lambda: addTopIndiacator('none'))
		menubar.add_cascade(label="Top Indicator",menu=topIndi)







		tk.Tk.config(self,menu=menubar)
		self.frames={}

		for F in (StartPage,BTCe_page):
			frame=F(container,self)
			self.frames[F]=frame
			frame.grid(row=0,column=0,sticky="nsew")
		
		self.show_frame(StartPage)


	def show_frame(self,cont):
		frame=self.frames[cont]
		frame.tkraise()



class StartPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="""ALPHA Bitcion trading application
use at your own risk.There is no promise
of warranty.""",font=large_font)
		label.pack(pady=10,padx=10)
		button1=ttk.Button(self,text="Agree",
			command=lambda: controller.show_frame(BTCe_page))
		button1.pack()
		button2=ttk.Button(self,text="Disagree",
			command=quit)
		button2.pack()
		

class PageOne(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Page One",font=large_font)
		label.pack(pady=10,padx=10)
		button1=ttk.Button(self,text="Back to Home",
			command=lambda: controller.show_frame(StartPage))
		button1.pack()
		


class BTCe_page(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Graph Page",font=large_font)
		label.pack(pady=10,padx=10)
		button1=ttk.Button(self,text="Back to Home",
			command=lambda: controller.show_frame(StartPage))
		button1.pack()
		canvas=FigureCanvasTkAgg(f,self)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
		toolbar=NavigationToolbar2TkAgg(canvas,self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)



app=seaofBTCapp()
app.geometry("1920x1080")
ani=animation.FuncAnimation(f,animate,interval=5000)
app.mainloop()