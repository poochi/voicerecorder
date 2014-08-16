import Tkinter
import re    
import tkFont
import time
import ttk
import tkSimpleDialog
from itertools import cycle

from database import *
from audiorecorder import *

def sortby(tree, col, descending,db,primarykey='Name'):
        """Sort tree contents when a column is clicked on."""
        
        # grab values to sort
        print tree.get_children('')
        data=[]
        for child in tree.get_children(''):
                res = db.getvalue(tree.set(child,primarykey))
                if col == 'Date':
                        data.append((float(res['Date']),child))
                else:
                        data.append((tree.set(child,col),child))
                
        
        
        #data = [(tree.set(child, col), child) for child in tree.get_children('')]
        #print col
        print data

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
            command=lambda col=col: sortby(tree,col, int(not descending),db,primarykey))
  



class Voicerecordapp(Tkinter.Tk):
    def __init__(self,parent,arec):
        self.parent = parent;
        Tkinter.Tk.__init__(self,parent);
        self.arec = arec
        self.buttonText = 'Start\nRecording'
        self.isRecording = False;
        self.tree_columns = ('Date','Name','Rating')
        self.db = database()
        self.tree_data_list = self.db.getlist()
        self.tree_data = []
        for t,_a,_b in self.tree_data_list:
                self.tree_data.append((self.get_time_conversion(float(t)),_a,_b))
        #self.tree_data = [('Now','A','2'),('3mintues','B','3'),('2minutes','C','4')]
        self.stopslide  = False;
        self.textshow=['Thank you Chitra!','Thank you ,people at MIT for Pyaudio!','Thanks to the python guys !','Thanks to Tkinter grand daddys too !','Developed by Gowtham Rangarajan R','Your file gets saved here ... '+self.db.homepath
                       ,'Click on me to toggle marquing','Check out the repo at www.github.com/poochi/ ','Press Enter to Save','Rate Before Saving !'] #40 characters only
        self.current = cycle(self.textshow)
        
        self._isplayingprogress = False
 
        
        self.initialise();
        self._build_tree();
        self.state = 'Start\nRecording'
        self.tree.tag_configure('Nowplaying',background='light blue')
        self.tree.tag_configure('Old',background='white')
        self.playing_selection = None;
        
        
    def done_Waiting(self):
            print' lol'
            for each in self.win:
                    each.destroy()
            
            #BRING BACK ALL WIDGETS
            self.placewidgets()
          
            
            
    def disp_error(self,messagelist=['Oops!',"Something's wrong! :("],duration=5000):
      
            print'eait'
            
            #REMOVE ALL WIDGETS            
            #self.startbutton.pi = self.startbutton.grid_info();
            self.startbutton.grid_forget()

            
            #self.textentry.pi = self.textentry.grid_info();
            self.textentry.grid_forget()

            #self.ratingscale.pi = self.ratingscale.grid_info();
            self.ratingscale.grid_forget()

            #self.tree.pi = self.tree.grid_info();
            self.tree.grid_forget()

            #self.vsb.pi = self.vsb.grid_info();
            self.vsb.grid_forget()
                   
            
            win1 = Tkinter.Label(self,text=messagelist[0],justify=Tkinter.CENTER,padx=5, pady=25,font=("Arial", 16));
            win2 = Tkinter.Label(self,text=messagelist[1],justify=Tkinter.CENTER,padx=5, pady=10,font=("Helvetica", 12));           
            win1.grid(row=0,column=0)
            win2.grid(row=2,column=0)
            self.win=[win1,win2]
            win1.after(duration, self.done_Waiting)
            
        
    def get_time_conversion(self,p):
            currenttime = time.time()
            yr = 365*24*60*60
            mon = 30*24*60*60
            days = 24*60*60
            hours = 60*60
            minutes =  60
            if (currenttime-p)/yr >= 1 :
                    return str(int((currenttime-p)/yr))+' year'+('s ago' if int((currenttime-p)/yr)!=1 else ' ago')
            if (currenttime-p)/mon >= 1 :
                    return str(int((currenttime-p)/mon))+' month'+('s ago' if int((currenttime-p)/mon)!=1 else ' ' +'ago')
            if (currenttime-p)/days >= 1 :
                    return str(int((currenttime-p)/days))+' day'+('s ago' if int((currenttime-p)/days)!=1 else ' ' +'ago')
            if (currenttime-p)/hours >= 1 :
                    v = int((currenttime-p)/hours)
                    return str(v)+' hour'+('s ' if v!=1 else ' ' )+' and '+ str(int((currenttime-p)/minutes - v*60))+' minute'+('s ago' if int((currenttime-p)/minutes)!=1 else ' ' +'ago')
            if (currenttime-p)/minutes >= 1 :
                    return str(int((currenttime-p)/minutes))+' minute'+('s ago' if int((currenttime-p)/minutes)!=1 else ' ' +'ago')
            return str(int((currenttime-p)))+' second'+('s ago' if int((currenttime-p)!=1) else ' ' +'ago')
                    
    def enterfilename(self,event):
        print 'Here'
        if self.isRecording == False:
             v = self.textentry.get();
             print self.ratingscale.get()
             
             print v
             assert(type(v) == type('pop'))
             
             
             if not re.match("^[a-zA-Z0-9_]*$", v):
                 if not re.match("^[a-zA-Z0-9_\.]*$", v):
                         self.disp_error(['Oops! Cant understand the Filename','Can you try without Extension or Special Characters ? \n(eg) Tomorrow_s_lecture'],5000);
                 else:
                         self.disp_error(['Oops! Cant understand the Filename','Can you try without Extension ? \n(eg) Tomorrow_s_lecture'],5000);
                 return;

             if self.db.getvalue(v) != None:
                     self.disp_error(["File with the same name Exists !",' Change your filename to save it :)'],3000);
                     return;
                     

             res = self.arec._save(v);
             
             if res == 0:
                 append = False;
                 print 'Saved successfully To add to db';
                 p =time.time()
                 append = self.db.addvalue(v,{'Date':str(p),'Name':v,'Rating':str(self.ratingscale.get())})
                  
                 if append == True:
                      n_l = (time.time(),v,str(self.ratingscale.get()))
                      n = (self.get_time_conversion(n_l[0]),n_l[1],n_l[2])
                      
                      self.tree_data_list.append(n_l)
                      self.tree_data.append(n)
                      self._append_tree(n)
                 else:
##                     for no,[_,fn,_] in enumerate(self.tree_data):
##                         if v == fn:
##                              olddata = self.tree_data[no];
##                              self.tree_data_list[no] = (time.time(),self.tree_data_list[no][1:])
##                              self.tree_data[no] = (self.get_time_conversion(self.tree_data_list[no][0]),self.tree_data[no][1],str(self.ratingscale.get()))
##                              
##                              self._update_tree(olddata,self.tree_data[no],no)                              
##                              break;
                         #updating is not allowed since
                         #self.disp_error(self.arec.errorcodes['_save'][res-1],3000);
                         pass;
                             
                     
             else:
                      self.disp_error(self.arec.errorcodes['_save'][res-1],3000);
             
               
        
             
        
    def initiate_check(self):
            print 'Checking arec '
            if self.arec.isPlaying == True:
                    self.startbutton.after(100,self.initiate_check)
            else:
                    print 'DONne'
                    self.startbutton['text']='Start\nRecording'
                    self.state = 'Start\nRecording'
                    
                    
                    
     #bug        
    def cbk(self,event):
        #stop whatever you are doing
        self.arec.stop();
        if self.state == 'Start\nRecording':
                self.arec.record()
                self.state = 'Stop\nRecording'
        elif self.state == 'Stop\nRecording':
                self.arec.play()
                self.state = 'Stop\nPlayback'
                self.initiate_check();
        elif self.state == 'Stop\nPlayback':                
                self.state = 'Start\nRecording'
        self.startbutton['text']=self.state
        print 'Im here' + str(self.arec.isRecording)
           
##    def check_db_play(self):
##            print 'checkdbplay ' ,self.arec.isPlaying , self.playing_selection
##            if self.playing_selection !=None and self.arec.isPlaying == False:
##                self.tree.item(self.playing_selection,tags=('Old',))
##                print 'changed tag'
##                self.playing_selection = None
##            else:
##                    self.tree.after(1000,self.check_db_play);
##
##                    
    def check_if_playing(self):
            if self.playing_selection != None and self.arec.isPlaying == False:
                    self.tree.item(self.playing_selection,tags=('Old',))
                    self.playing_selection = None
            else:
                    self.tree.after(100,self.check_if_playing)
    def doubleclick(self,event):
            item = self.tree.selection()[0]
            
            if self.playing_selection != item and self.playing_selection !=None:
                    self.arec.stop()
                    self.tree.item(self.playing_selection,tags=('Old',))
                    print "you clicked on", self.tree.item(item,"values")[1]
                    fname =  self.tree.item(item,"values")[1];
                    #fname = 'C:\\Users\\100555\\Documents\\1_s_1_0_1'
                    self.arec.play(fname+'.wav');
                    self.tree.item(item,tags=('Nowplaying',))
                    #self.tree.item(self.playing_selection,tags=('Old',))
                    print 'oNow'
                    assert(item!=None)
                    self.playing_selection = item;
                    #periodically check if the contents were deleted.
                    #self.check_db_play();
                    self.check_if_playing();
                    
                    return;
        
                    
            
            if self.arec.isPlaying == False and self.arec.isRecording == False :
                self.arec.stop()
                print "you clicked on", self.tree.item(item,"values")[1]
                fname =  self.tree.item(item,"values")[1];
                #fname = 'C:\\Users\\100555\\Documents\\1_s_1_0_1'
                self.arec.play(fname+'.wav');
                print 'Now'
                self.tree.item(item,tags=('Nowplaying',))
                self.playing_selection = item;
                #periodically check if the contents were deleted.
                #self.check_db_play();
                self.check_if_playing();
            elif self.playing_selection == item and self.arec.isPlaying == True:
                self.arec.stop()
                self.tree.item(self.playing_selection,tags=('Old',))
                self.playing_selection = None
            elif self.arec.isPlaying == True or self.arec.isRecording==True:
                
                self.arec.stop()
                
                
                self.playing_selection = item
                self.tree.item(self.playing_selection,tags=('Nowplaying',))
                self.check_if_playing();

                
                    
                                   
           
    def stopshow(self,event):
            print 'toggle'
            self.stopslide =not self.stopslide;
            self.slideshow();
    def slideshow(self):
            #Fade text away
            #slideshow
            if self.stopslide == False:
                    print 'Proceed'
                    self.sl.config(text=self.current.next())
                    self.sl.after(5000,self.slideshow)
            else:
                   print 'stop'
            
            
            
    def placewidgets(self):
                self.container.grid(column=0,row=3)
                self.container.grid_columnconfigure(0, weight=1)
                self.container.grid_rowconfigure(0, weight=1)
                self.ratingscale.grid(column =0,row =1,sticky='NW',pady=10) 
                self.textentry.grid(column =0,row =0,sticky='NW',pady=5);
                self.startbutton.grid(column =1,row =0,rowspan=2,padx=5,pady=5);
                #self.tree.grid(column=0,row=1,in_=container);
                self.tree.grid(column=0, row=1, columnspan=3,rowspan=10,sticky='nsew', in_=self.container)
                self.vsb.grid(column=2, row=1, rowspan=10,sticky='ns', in_=self.container)
        
        
    def initialise(self):
        self.grid()
        #self.ratingentry = Tkinter.Entry(self)
        #self.ratingentry.insert(0,'temp')
        #self.ratingentry.grid(column =0,row =1,sticky='NW',pady=10);
        
        self.textentry = Tkinter.Entry(self,width=25)
        
        #self.textentry.pack(side=Tkinter.LEFT)
        self.textentry.focus_set();
        self.textentry.bind("<Return>",self.enterfilename);

        self.startbutton = Tkinter.Button(self,text=self.buttonText,width=7,height=7)
        self.startbutton.bind("<Button-1>",self.cbk)
        
        #self.startbutton.pack(side=Tkinter.LEFT)

        self.container = ttk.Frame(height=1)
        
        #container.pack(fill=Tkinter.Y,expand=True);
        
        self.tree = ttk.Treeview(columns = self.tree_columns, show='headings',height=min(7,max(4,len(self.tree_data))))
        self.vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        
        
        
        


        self.tree.bind('<Double-1>',self.doubleclick);
        
        #container.grid(column=1,row=2)

        #self.ratingentry.after(5, self.updateBoard)
        self.ratingscale=Tkinter.Scale(self,orient=Tkinter.HORIZONTAL,length=150,width=20,sliderlength=10,from_=0,to=5,tickinterval=1);
        
        
        
        #self.canvas =Tkinter.Canvas(self, width=100, height=20,bg='green')
        #self.canvas.create_text(10,10,text=self.textshow[0],anchor=Tkinter.CENTER);
        #self.canvas.grid(column=0,row=6,columnspan=3,in_=container)

        self.placewidgets();

        
        

        self.sl = Tkinter.Label(self,text='',relief=Tkinter.GROOVE,justify=Tkinter.CENTER)
        self.sl.grid(column=0,row=6,columnspan=3);
        self.sl.bind("<Button-1>",self.stopshow);
        self.slideshow()
        #self._check_db_change();
        
        
        

##    def _check_db_change(self):
##            newlist = self.db.getlist()
##            new_data = []
##            for t,_a,_b in newlist:
##                new_data.append((self.get_time_conversion(float(t)),_a,_b))
##            upd =False
##            c=0;
##            #order can be jumbled taken care of
##            for each in self.tree_data_list:                    
##                if each not in newlist:
##                    upd = True;
##                    if self.playing_selection == item:
##                            self.stop();
##                            self.disp_error(message=['OMG!!','The file being played got deleted \n stopping playout'])
##                    self.tree.move(item,'',c);
##                else:
##                    c+=1
##            #remove the rest , check if playing if not display error, stop it
##                            
##            self.tree_data_list = newlist;
##            self.tree_data = new_data
##            #Periodic check 
##            self.tree.after(3000,self._check_db_change)
    
       
    def _build_tree(self):
        for col in self.tree_columns:
            print col
            self.tree.heading(col, text=col.title(),command=lambda c=col: sortby(self.tree, c, False,self.db,'Name'))
            # XXX tkFont.Font().measure expected args are incorrect according
            #     to the Tk docs
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in self.tree_data:            
            self.tree.insert('', 'end', values=item)

            # adjust columns lenghts if necessary
            for indx, val in enumerate(item):
                ilen = tkFont.Font().measure(val)
                if self.tree.column(self.tree_columns[indx], width=None) < ilen:
                    self.tree.column(self.tree_columns[indx], width=ilen)

        #Getting Tabular column as big as banner
        ilen = max( tkFont.Font().measure(each) for each in self.textshow)
        
        s = sum(self.tree.column(self.tree_columns[indx], width=None) for indx,_ in enumerate(item))
        print s ,ilen
        if s<ilen:
                for indx,_ in enumerate(item):
                        w = self.tree.column(self.tree_columns[indx], width=None)
                        
                        w+=int((ilen-s)/3);
                        
                        self.tree.column(self.tree_columns[indx], width=(w))
                
        print 'textshow ',ilen
        return;


    def _append_tree(self,newitem):
        print self.tree.column('#1')
        print 'new item' , newitem
        self.tree_data.append(newitem);
        self.tree.insert('','end',values=newitem)
        # adjust columns lenghts if necessary
        for indx, val in enumerate(newitem):
                ilen = tkFont.Font().measure(val)
                if self.tree.column(self.tree_columns[indx], width=None) < ilen:
                    self.tree.column(self.tree_columns[indx], width=ilen)
        return;

##    def _update_tree(self,olditem,newitem,rowno):               
##        self.tree.move(newitem,'',rowno);
##        for each in self.tree.get_children(''):
##                print self.tree.get(each)
##                print each,'  ',olditem
##                if each == olditem:
##                        self.tree.set(newitem)
                 
        #self.tree.insert('','end',values=newitem)
        # adjust columns lenghts if necessary
        for indx, val in enumerate(newitem):
                ilen = tkFont.Font().measure(val)
                if self.tree.column(self.tree_columns[indx], width=None) < ilen:
                    self.tree.column(self.tree_columns[indx], width=ilen)
        return;

def handler():
    print "In Quit"
    global app;
    #Release Resource    
    app.arec.stop()
    app.arec.remove()
    app.destroy()   
      
if __name__ == '__main__':
    arec = audiorecorder();
    app = Voicerecordapp(None,arec);      
    app.title('Recorder');
    app.protocol("WM_DELETE_WINDOW", handler)
    app.mainloop()

