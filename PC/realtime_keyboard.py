import Tkinter as tk

def onKeyPress(event):
    text.insert('end', 'You pressed %s\n' % (event.char, ))

def leftKey(event):
    text.insert('end', 'Left arrow')

def rightKey(event):
    text.insert('end', 'Right arrow')

def upKey(event):
    text.insert('end', 'Up arrow')

def downKey(event):
    text.insert('end', 'Down arrow')




root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)

root.mainloop()