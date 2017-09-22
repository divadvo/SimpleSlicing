from Tkinter import *

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    
    self.button_start = Button(frame, 
                         text="START", fg="red",
                         command=self.button_start_click, height=5, width=20)
    self.button_start.grid(row=0, column=0)

    self.button_update = Button(frame,
                         text="Update",
                         command=self.button_update_click, height=5, width=20)
    self.button_update.grid(row=0, column=1)
    
  def button_update_click(self):
    print("Update Git")
    import git 
    import os

    self.button_start.config(state="disabled")
    self.button_update.config(state="disabled")

    g = git.cmd.Git(os.getcwd())
    g.pull()


    self.button_start.config(state="normal")
    self.button_update.config(state="normal")

    print "pull ready Test"

  def button_start_click(self):
    print("Start")

    import subprocess
    import os
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fileName = os.path.join(__location__, 'gui.py')

    subprocess.Popen("python " + fileName, shell=True)

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

if __name__ == '__main__':
  root = Tk()
  root.title("3D Druck")
  root.geometry("400x100")
  center(root)

  app = App(root)
  root.mainloop()
