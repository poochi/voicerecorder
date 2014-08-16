from setuptools import setup    
setup(
    name = "Recorder",    
    version = "1.0",
    description = "Record ,Rate and Keep track of your progress",
    author = "Gowtham Rangarajan R",
    author_email = "rangnewton@gmail.com",
    url = "http://github.com/poochi",
    download_url = "",
    keywords = ["Record","speaking","Toefl","Rehearse","Educational","pickledb","Tkinter"],
    install_requires=[
        'pyaudio','tkinter','tkSimpleDialog',
        'ttk','tkSimpleDialog','threading','wave',
        'pickledb'
       ],
    classifiers = [
        
        "Programming Language :: Python",
        
        "Development Status :: 1 - Beta",
        "Environment :: Linux Debian Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        
        ],
    long_description = """\
Recording Application
----------------------------
Its a dead-simple Recording application which helps you prepare for speaking sessions ,be it for interviews, lectures or perhaps for recitals in school !
I personally use it to practise my english for Toefl and ,well, for practising poerty for my girlfriend .
Check out the Screen Shots

Lastly , Sorry for the 95-ish graphics .

Details for Nerds :)
It was written using Tkinter , and its derivatives .
It uses port audio api .
It also uses Pickledb for database maintainence.
"""
)
