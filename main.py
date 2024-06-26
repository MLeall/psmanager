from PSManagerGUI import PSManagerGUI
import tkinter as tk

def main(user, password, cluster_name):
    root = tk.Tk()
    app = PSManagerGUI(root, user=user, password=password, cluster_name=cluster_name)
    root.mainloop()

if __name__ == '__main__':
    main('user', 'password', 'cluster_name')