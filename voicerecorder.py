import Tkinter
import pyaudio
import wave
import os
import threading

class audiorecorder():
    def __init__(self):
        self.time='now.wav'
        self.path = '/home/poochi/Desktop/'
        self.state = 'WAITING'
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = os.path.join(self.path,self.time);
        self.p = pyaudio.PyAudio()
        
        self.tempfile = None;

        
        self.total_chunk = 0;
        self.frames = [];
        self._recordingprogess = False

    
    def _record(self):
        streamin = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        
        while self._recordingprogess == True:
                    data = streamin.read(self.CHUNK)
                    self.total_chunk += self.CHUNK;
                    self.frames.append(data);
                    
        print 'RECORDING STOPPED'
        streamin.close()
        
        
        
    def record(self):
            self.total_chunk = 0;
            self.frames = [];
            
            print 'RECORDING to a temp file'
            if self.tempfile != None:
                self.tempfile.close();
            print 'RECORDING STARTED'
            self._recordingprogess = True;
            self.t = threading.Thread(target=self._record)
            self.t.start();
            print 'Parallel thread'
            
            
    def stop(self):
        print 'Stop ?'
        self._recordingprogess = False;
                
        streamout = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True)
        
        print 'PLAYING'
        for each in self.frames:
                    streamout.write(each);
                
        streamout.close();
        self._isplayingprogress=False;
         
                    
        
    def save(self):
        if self._isplayingprogress == False and self._recordingprogess == False:          
            
            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)        
            wf.writeframes(b''.join(self.frames))
            wf.close()
            

    def remove(self):
        self._recordingprogess = False
        
        self.tempfile.close();
        self.p.terminate();
        
        

    


class Voicerecordapp(Tkinter.Tk):
    def __init__(self,parent,arec):
        self.parent = parent;
        Tkinter.Tk.__init__(self,parent);
        self.arec = arec
        self.buttonText = 'Record'
        self.isRecording = False;
        self.initialise();
        
        

    def cbk(self,event):
        if self.isRecording == False:
            self.startbutton['text']='StopRecording';
            self.arec.record();
            
        if self.isRecording == True:
            print 'REC'
            self.startbutton['text']='Record';
            self.arec.stop();
            
        self.isRecording = not(self.isRecording)

    def initialise(self):
        self.grid()
        self.filename = Tkinter.Entry(self)
        self.filename.grid(column =0,row =0,sticky='NW');

        self.startbutton = Tkinter.Button(self,text=self.buttonText)
        self.startbutton.bind("<Button-1>",self.cbk)
        self.startbutton.grid(column =1,row =0);
        
        
        

        pass;


def quit():
    global app,arec;
    app.destroy();
    arec.remove();
    
#BLOCKING PLAYBACK
if __name__ == '__main__':
    arec = audiorecorder();
    app = Voicerecordapp(None,arec);  
    
    app.title('VoiceRecoder');
    app.mainloop()
        
