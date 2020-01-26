import tkinter as tk


class ExampleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.some_frame = None

        tk.Button(self.master, text="Create new frame with widgets!", command = self.create_stuff).pack()

    def create_stuff(self):
        if self.some_frame == None:
            self.some_frame = tk.Frame(self.master)
            self.some_frame.pack()

            for i in range(5):
                tk.Label(self.some_frame, text = "This is label {}!".format(i+1)).pack()

            tk.Button(self.some_frame, text="Destroy all widgets in this frame!",
                      command= self.destroy_some_frame).pack()

    def destroy_some_frame(self):
        self.some_frame.destroy()
        self.some_frame = None

root = tk.Tk()
my_example = ExampleApp(root)
root.mainloop()