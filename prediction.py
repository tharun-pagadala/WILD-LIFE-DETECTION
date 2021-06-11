import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from sklearn.model_selection import train_test_split
import cv2
import os
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import accuracy_score
from svm import SVM

class TitleWindow:
    parent=root=None
    loginbtn=None
    X_train=Y_train=None
    directory=""
    filename=""
    animals=labels=None
    trainData= testData=trainLabels=testLabels=None
    obj=SVM()
    def HomeScreen(self):
        TitleWindow.parent=Tk()
        TitleWindow.parent.title("MainWindow")
        TitleWindow.parent.geometry("400x400")
        Label(text="").pack()
        title=Label(TitleWindow.parent,text="DETECTION OF ANIMAL",bg='yellow',fg='black',
				font=('arial',16, "bold"))
        title.pack()
        Label(text="").pack()
        Label(width=50,font=('arial',10, "bold"),fg='blue', text="Farmers  in  India  face  serious  threats  from  pests,  natural calamities  &damage \n by  animals  resulting  in  lower  yields Traditional  methods  followed  byfarmers \n are  not  that effective and it is not feasible to hire guards to keep an \neye on  crops  and  prevent  wild  animals.  Since  safety  of  both human and animal is equally vital.\nSo, animal detection system is necessary in farm areas.").pack()
        Label(text="").pack()
        TitleWindow.loginbtn=Button(TitleWindow.parent,fg='red', text="LOGIN",width=15,height=3,font=('arial',12,"bold"),command=self.login)
        TitleWindow.loginbtn.pack()
        Label(text="").pack()
        TitleWindow.parent.mainloop()
       
    def login(self):
        
        self.loginwin=Toplevel()
        self.loginwin.title("User Login")
        self.loginwin.geometry("300x300")
        Label(self.loginwin,text="").grid(row=1,column=1,columnspan=2)
        self.title=Label(self.loginwin,text="LOGIN",fg='blue',
				font=('arial',13, "bold"))
        
        self.title.grid(row=2,column=1,columnspan=2)
        Label(self.loginwin,text="").grid(row=3,column=1,columnspan=2)
        self.userlbl=Label(self.loginwin,text="User Name",font=('arial',10, "bold"))
        self.userlbl.grid(row=4,column=1)

        self.usertxt=Entry(self.loginwin)
        self.usertxt.grid(row=4,column=2)
        
        self.pwdlbl=Label(self.loginwin,text="Passward", font=('arial',10, "bold"))
        self.pwdlbl.grid(row=6,column=1)

        self.pwdtxt=Entry(self.loginwin, show='*')
        self.pwdtxt.grid(row=6,column=2)
        Label(self.loginwin,text="").grid(row=7,column=1,columnspan=2)
        self.loginbtn=Button(self.loginwin,width=8,height=2,text="LOGIN",fg='red',font=('arial',13, "bold"),command=self.validateuser)
        self.loginbtn.grid(row=8,column=1,columnspan=2)
        self.loginwin.mainloop()
    
        
    def validateuser(self):
        f=open('users.txt','r')
        lines=f.read().splitlines()
        username=self.usertxt.get()
        password=self.pwdtxt.get()
        
        if username==lines[0] and password==lines[1]:
            TitleWindow.loginbtn.configure(state=DISABLED)
            self.loginwin.destroy()
            
            self.MainMenu()
            
            
        else:
            msg = messagebox.showinfo("Information","User Not Found, Try Again!!!")
            
            
        
    def MainMenu(self):
        self.welwin=Toplevel()
        TitleWindow.root=self.welwin
        self.welwin.title("Main Menu")
        self.welwin.geometry("400x400")
        Label(self.welwin,text="").grid(row=1,column=1,columnspan=2)
        self.title=Label(self.welwin,text="MAIN MENU",bg='green',fg='white',
				font=('arial',13, "bold"))
        Label(self.welwin,text="").grid(row=1,column=1,columnspan=2)
        self.title.grid(row=2,column=1,columnspan=2);
        
        Label(self.welwin,text="").grid(row=3,column=1,columnspan=2)
        self.diabtn=Button(self.welwin,width=15,height=2,text="Train Dataset...",font=('arial',13, "bold"),command=self.openfolderdialog)
        self.diabtn.grid(row=5,column=1,columnspan=2)

        Label(self.welwin,text="").grid(row=6,column=1,columnspan=2)
        self.diabtn=Button(self.welwin,width=15,height=2,text="Test Image",font=('arial',13, "bold"),command=self.openfiledialog)
        self.diabtn.grid(row=8,column=1,columnspan=2)

        Label(self.welwin,text="").grid(row=9,column=1,columnspan=2)
        self.diabtn=Button(self.welwin,width=15,height=2,text="Predict",font=('arial',13, "bold"),command=self.predict)
        self.diabtn.grid(row=10,column=1,columnspan=2)

        Label(self.welwin,text="").grid(row=12,column=1,columnspan=2)
        self.logoutbtn=Button(self.welwin,width=10,height=2,text="Logout",font=('arial',13, "bold"),command=TitleWindow.parent.destroy)
        self.logoutbtn.grid(row=13,column=1,columnspan=2)
        
        self.welwin.mainloop()
        
    def openfolderdialog(self):
        TitleWindow.directory = filedialog.askdirectory(parent=TitleWindow.root,title='Choose directory with image sequence stack files')
        if not TitleWindow.directory:
            return
        
        SVM.namelabels.clear()

         # Read each directory
        for directoryname in os.listdir(TitleWindow.directory):

            if directoryname.startswith("."):
                continue
            else:
                SVM.namelabels.append(directoryname)  # appends all directory names as labels

        print(SVM.namelabels)
        
        TitleWindow.animals,TitleWindow.labels= TitleWindow.obj.prepareTrainingData(TitleWindow.directory)
        print("Total animals: ", len(TitleWindow.animals))
        print("Total labels: ", len(TitleWindow.labels))

        # step2: split training and test data
        (TitleWindow.trainData, TitleWindow.testData, TitleWindow.trainLabels, TitleWindow.testLabels) = train_test_split(np.array(TitleWindow.animals), np.array(TitleWindow.labels), test_size=0.1,
                                                                  random_state=59)
        TitleWindow.obj.clf = svm.SVC(C=1000)
        

        # Train the model using the training sets
        TitleWindow.obj.clf.fit(TitleWindow.trainData, TitleWindow.trainLabels)
       
	
    def openfiledialog(self):
        TitleWindow.filename = filedialog.askopenfilename(parent=TitleWindow.root,initialdir =  "/", title = "Select AN IMAGE", filetype = (("jpeg files","*.jpg"),("png files","*.png")) )
        
	
    
    def predict(self):
        
        image = cv2.imread(TitleWindow.filename)
        
        predict = TitleWindow.obj.clf.predict(TitleWindow.obj.getFeatures(image).reshape(1, -1))[0]
        print(predict)


        predicts = TitleWindow.obj.clf.predict(TitleWindow.testData)
        print("Model Accuracy :", accuracy_score(TitleWindow.testLabels, predicts) *100)
        
        cv2.putText(image, SVM.namelabels[predict] , (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        cv2.imshow("Test", image)
        mytext = "It is a "+SVM.namelabels[predict]

        '''from gtts import gTTS
        import os
        mytext = "It is a "+SVM.namelabels[predict]
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("welcome.mp3")
        from playsound import playsound

        playsound('welcome.mp3')
        os.system("mpg321 welcome.mp3") 
        
        cv2.waitKey(0)
        os.remove("welcome.mp3")'''

        import pyttsx3
        engine = pyttsx3.init()
        engine.say(mytext)
        engine.runAndWait()
        

obj=TitleWindow()
obj.HomeScreen()



