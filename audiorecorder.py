import wave
import pyaudio
import threading
import os

class audiorecorder():
    def __init__(self):
        self.filename='now.wav'
        self.homepath = '/home/poochi/Desktop/micrecorder/recording'        
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = os.path.join(self.homepath,self.filename);
        self.p = pyaudio.PyAudio()        
        self.tempfile = None;
        self.total_chunk = 0;
        self.frames = [];
        self._asktofreeresource = False
        self._freedresource = True
        self.isRecording = False
        self.isPlaying = False
        #0 is correct others arent
        self.errorcodes = {'_save':[['Oops!,I did not Record anything','Can you click on the Record Button ?'],             
             ["I'm Busy Recording what you are saying !","Click on StopRecording once you think you are done :) "],
             ["Oops!, Im playing out !"," Can you Stop me before asking me to save ? :) "],             
             ['Aww :(,Somethings Wrong !','Can you restart the app ?']
        
                                     ]}


    def acquire_resource(self):
        print 'acuire_resourse'
        if self._freedresource == True:
            print 'returning'
            return;
        
        self._asktofreeresource = True;
        self._stop()

    def  stop(self):
        print 'Trying to stop'
        self.acquire_resource();
            
    def _stop(self):
        print 'stopping'
        print str(self._asktofreeresource) + ' _asktofreeresource'
        #wait till resource is free [or 10 secs in case]which
        while self._freedresource == False:
            pass;
        print '_asktofreeresource is false stopped'            
        self._asktofreeresource=False;
    
            
    
    def _record(self):
        
        self.isRecording == True
        print 'isRecording T',self._asktofreeresource
        self._freedresource = False
        print 'REORDING BEGUN'
        try:
            streamin = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
                
            while self._asktofreeresource == False:
                data = streamin.read(self.CHUNK)
                self.total_chunk += self.CHUNK;
                self.frames.append(data);
                            
            print 'RECORDING STOPPED'
            print len(self.frames)
            streamin.close()
        except:
                print 'Recording error'
        self._freedresource = True;
        self._asktofreeresource=False;
        self.isRecording == False
    def record(self):
        self.total_chunk = 0;
        self.frames = [];
            
        print 'RECORDING to a temp file'
        print 'RECORDING STARTED'
        self.acquire_resource();
        self.t = threading.Thread(target=self._record)
        self.t.start();
        print 'Parallel thread'

    def play(self,filename=None):
        self.acquire_resource()
        print 'begun playing'
        self.isPlaying =True
        while self._freedresource == False:
                pass;
        
        if filename == None:
            print 'SoooooSOEarly ---',len(self.frames)
            self.t = threading.Thread(target=self._play,args=(self.frames,))
            self.t.start();
            
            #self._play(self.frames)
            print 'SOooooooooooLAte'
        else:
            w = wave.open(open(os.path.join(self.homepath,filename),'rb'));
            
            data = w.readframes(1024)
            frames = []
            while data != '':
                    frames.append(data)
                    data = w.readframes(1024)
          
            w.close()           
            self.t = threading.Thread(target=self._play,args=(frames,w,))
            self.t.start();
            
    def _play(self,frames=None,w=None):         
        self._freedresource = False       
        print 'Trying to play '
        print 'PLAYING ----',len(frames)
        try:
        #if 1>0:
            if w !=None:
                streamout = self.p.open(format=self.FORMAT,
                        channels=w.getnchannels(),
                        rate=w.getframerate(),
                        output=True)
            else:
                streamout = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            output=True)
                    
            
                
            for each in frames:
                if self._asktofreeresource == False:
                    streamout.write(each);
                else:
                    break;
                        
            streamout.close();
                
        except:
            print 'Playing out error'
        self._freedresource = True;
        self._asktofreeresource=False;
        self.isPlaying = False
        print 'Done playout'
        
 

    def _save(self,name):        
        self.filename = name.split('.')[0];
        self.filename +='.wav'
        
        if self.isRecording == False and self.isPlaying == False:
            if len(self.frames)>0 :
                                        
                    self.WAVE_OUTPUT_FILENAME = os.path.join(self.homepath,self.filename);
                    print self.WAVE_OUTPUT_FILENAME
                    wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(self.CHANNELS)
                    wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                    wf.setframerate(self.RATE)        
                    wf.writeframes(b''.join(self.frames))
                    wf.close()
                    return 0;
                
            else:                
                return 1;
        else:
                if self.isPlaying == True:
                        print'ge'
                        return 2;
        return 3;
    
            
          

    def remove(self):
        self.p.terminate();
        
        
