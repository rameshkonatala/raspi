import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
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


large_font=("Helvetica",12)
style.use("ggplot")


f=Figure(figsize=(5,5),dpi=100)
a=f.add_subplot(111)



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
	a.plot_date(buyDates,buys['price'])
	a.plot_date(sellDates,sells['price'])



class seaofBTCapp(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		#tk.Tk.iconbitmap(self,default='@/home/ramesh/Desktop/tkinter/person.xbm')
		tk.Tk.wm_title(self,"Sea of BTC client")
		container=tk.Frame(self)
		container.pack(side="top",fill="both",expand="True")
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
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
ani=animation.FuncAnimation(f,animate,interval=1000)
app.mainloop()