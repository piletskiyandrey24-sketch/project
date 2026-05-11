import tkinter as tk
from tkinter import ttk, messagebox

class interface:                        

    @staticmethod
    def create_buttons(frame, frame_name):                               #создание кнопок
        tk.Button(frame, text=frame_name, font=('Arial', 15),
                  command=lambda: interface.show_info_frame(frame_name), height=4, width=13, bg='lightblue').pack(side=tk.TOP, fill=tk.X, pady=2)
    
    @staticmethod
    def create_frames_for_operations(frame_name):                           #создание слоев
        info_frames[frame_name] = ttk.Frame(root, padding="20").grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frames[frame_name].grid_remove()
    
    @staticmethod
    def hide_all_frames():                            #прячем все слои
        for frame in info_frames.values():
            frame.grid_remove()   

    @staticmethod
    def show_info_frame(frame_name):                         #достаем определённый слой
        interface.hide_all_frames()
        info_frames[frame_name].grid()
    
    @staticmethod
    def show_main_buttons():
        interface.hide_all_frames()
        info_frames['Главная'].grid()


def frame_main(frame):                              #главное окно
    ttk.Label(frame, text='выберите операцию',
            font=("Arial", 16, "bold")).pack(pady=10)
    main_frame = ttk.Frame(frame)
    main_frame.pack(fill=tk.BOTH, expand=True)
    for frame_name in operations_windows:
        if frame_name == 'Главная':
            continue
        else:
            interface.create_buttons(main_frame, frame_name)




class dobavit:
    def frame_dobavit(frame):
        ttk.Label(frame, text='операция "добавить"',
            font=("Arial", 16, "bold")).grid(row=0, column=0)
    def 
        

class prodaja:
    def frame_prodaja(frame):
        ttk.Label(frame, text='операция "продажа"',
            font=("Arial", 16, "bold")).grid(row=0, column=0)
        
#main

root = tk.Tk()
root.title("window")
root.geometry("960x540")
root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy()))

info_frames = {}
operations_windows = {'Главная': frame_main, 'Добавить': dobavit.frame_dobavit, 'Продажа': prodaja.frame_prodaja}

for name, function in operations_windows.items():
    frame = tk.Frame(root)
    function(frame)
    info_frames[name] = frame
    frame.grid(row=0, column=0, sticky="nsew") 
    if name != 'Главная':
        tk.Button(frame, text='назад', font=('Arial', 15),
                    command=interface.show_main_buttons).grid(row=99, column=0, pady=10, sticky='s')
        frame.grid_remove()

root.mainloop()            

