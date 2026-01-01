import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.filedialog as tkfdlg
import patternOffsetter as ptnOfst

debug = False
 
tkVarFpathToOffset  :tk.StringVar
tkVarNumToOffset    :tk.StringVar

labelPath           :tk.Label   # label for edit box (path)
btnSelFpathToOffset :tk.Button  # button to select filepath (of Famitracker Txt)
editFpathToOffset   :tk.Entry   # edit box to set famitracker textfile path

labelNumOffset      :tk.Label
editNumToOffset     :tk.Entry
btnRunOffset        :tk.Button

offsetter           :ptnOfst.pattenOffsetter

def OnClickSelFile():
    tmpPath = tkfdlg.askopenfilename()
    tkVarFpathToOffset.set(tmpPath)
    if(True == debug):
        print(tmpPath)

def OnClickRunOffset():
    if((tkVarFpathToOffset.get() == '')or (tkVarNumToOffset.get() == '')):
        tkmsgbox.showerror(title='pattern offsetter', message='please select file and set number to offset')
        return
    offsetter = ptnOfst.pattenOffsetter()
    offsetter.setPath(tkVarFpathToOffset.get())
    offsetter.setOffset(int(tkVarNumToOffset.get(), 16))
    offsetter.doAll()

def OnclickDbgBtn():
    if(True == debug):
        print(tkVarFpathToOffset.get())
        print(tkVarNumToOffset.get())
    
# ==== PREPARATION OF DIALOG ====    
root = tk.Tk()
root.geometry("320x240")
root.resizable(False, False)

tkVarFpathToOffset  = tk.StringVar()
tkVarNumToOffset    = tk.StringVar()

labelPath           = tk.Label(root, text = 'Famitracker Textfile:')
editFpathToOffset   = tk.Entry(root,textvariable = tkVarFpathToOffset)
btnSelFpathToOffset = tk.Button(root, text='select',command=OnClickSelFile)
labelNumOffset      = tk.Label(root, text = 'Number to offset (in HEX):')
editNumToOffset     = tk.Entry(root,textvariable = tkVarNumToOffset)
btnRunOffset        = tk.Button(root, text='RUN',command=OnClickRunOffset)

if(True == debug):
    btnDebug    = tk.Button(root,text='DBG', command=OnclickDbgBtn)
    btnDebug.grid(row=2, column=0)

labelPath.grid          (row=0, column=0)
editFpathToOffset.grid  (row=0, column=1)
btnSelFpathToOffset.grid(row=0, column=2)
labelNumOffset.grid     (row=1, column=0)
editNumToOffset.grid    (row=1, column=1)
btnRunOffset.grid       (row=1, column=2)

root.mainloop()