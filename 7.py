import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style



large_font=("Helvetica",12)
style.use("ggplot")


f=Figure(figsize=(5,5),dpi=100)
a=f.add_subplot(111)



def animate(i):
	pullData=open("sampleData.txt","r").read()
	dataList=pullData.split('\n')
	xList=[]
	yList=[]
	for eachLine in dataList:
		if len(eachLine)>1:
			x,y=eachLine.split(',')
			xList.append(int(x))
			yList.append(int(y))

	a.clear()
	a.plot(xList,yList)

class seaofBTCapp(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		#tk.Tk.iconbitmap(self,default='@/home/ramesh/Desktop/tkinter/person.xbm')
		tk.Tk.wm_title(self,"Person")
		container=tk.Frame(self)
		container.pack(side="top",fill="both",expand="True")
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
		self.frames={}

		for F in (StartPage,PageOne,PageTwo,PageThree):
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
		label=tk.Label(self,text="Start Page",font=large_font)
		label.pack(pady=10,padx=10)
		button=ttk.Button(self,text="Visit page 1",
			command=lambda: controller.show_frame(PageOne))
		button.pack()
		button2=ttk.Button(self,text="Visit page 2",
			command=lambda: controller.show_frame(PageTwo))
		button2.pack()
		button3=ttk.Button(self,text="Graph Page",
			command=lambda: controller.show_frame(PageThree))
		button3.pack()


class PageOne(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Page One",font=large_font)
		label.pack(pady=10,padx=10)
		button1=ttk.Button(self,text="Back to Home",
			command=lambda: controller.show_frame(StartPage))
		button1.pack()
		button2=ttk.Button(self,text="Page Two",
			command=lambda: controller.show_frame(PageTwo))
		button2.pack()

class PageTwo(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Page Two",font=large_font)
		label.pack(pady=10,padx=10)
		button1=ttk.Button(self,text="Back to Home",
			command=lambda: controller.show_frame(StartPage))
		button1.pack()
		button2=ttk.Button(self,text="Page One",
			command=lambda: controller.show_frame(PageOne))
		button2.pack()

class PageThree(tk.Frame):
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