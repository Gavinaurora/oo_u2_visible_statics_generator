import json
import tkinter as tk

import rng

rng.__init__()
rng.mono_lift_mono_from_burst_gen()

parameter = json.load(open('config.json', 'r', encoding="utf-8"))

window = tk.Tk()
window.title("OO U2 数据生成器 by Gavinaurora")
window.iconbitmap("the_d6.ico")
window.geometry("1000x750")
window.resizable(False, False)

func_list = parameter['FUNC_LIST']
func_description = parameter['FUNC_DESCRIPTION']

help_info = tk.StringVar()
help_info.set("你好，欢迎使用我的可视化数据生成器！")
help_info_label = tk.Label(window, textvariable=help_info, width=85, height=2,
                           bg='white', fg='black', font=('Arial', 12), anchor='w')
help_info_label.place(x=0, y=690)

now_func_list = []
chosenFuncVar = tk.StringVar()
chosenFunc = tk.Label(window, bg='white', fg='black', font=('Arial', 12), width=30, textvariable=chosenFuncVar,
                      justify='left')
chosenFunc.place(x=700, y=0)

req = []
file_name = "file1.txt"


def clear_txt():
    with open(file_name, "w") as f:
        pass


def print_func_queue():
    value = ""
    for i in now_func_list:
        value += i
        value += "\n"
    chosenFuncVar.set(value)


def add_func():
    try:
        now_func_list.append(lb.get(lb.curselection()))
    except tk.TclError:
        help_info.set("ERROR! 似乎你并没有选择一种可以加入的策略。")
        return
    else:
        pos = func_list.index(lb.get(lb.curselection()))
        if len(req) < 20:
            help_info.set(func_description[pos])
        else:
            help_info.set("WARNING! 你选择生成的数据太多了(但可以正常生成)。")
        req.append(pos)
        print_func_queue()


def del_func():
    if len(req) == 0:
        help_info.set("ERROR! 队列里已经没有策略可以删除。")
    else:
        req.pop(len(req) - 1)
        now_func_list.pop(len(now_func_list) - 1)
        print_func_queue()
        help_info.set("成功移除了一组策略。")


def del_all_func():
    req.clear()
    now_func_list.clear()
    print_func_queue()
    help_info.set("成功移除了所有策略。")


def get_func_info():
    try:
        lb.get(lb.curselection())
    except tk.TclError:
        help_info.set("WARNING! 无法展示一个不存在的策略的信息。")
        return
    else:
        pos = func_list.index(lb.get(lb.curselection()))
        help_info.set(func_description[pos])


def gen():
    if len(req) == 0:
        help_info.set("WARNING! 你没有选择任何策略,生成数据的请求已经被终止")
        return
    clear_txt()
    rng.fin_gen(req)
    help_info.set("生成数据成功！")
    string = str(round(rng.time, 1)) + 's'
    time_output.config(text=string)
    with open(file_name, "r", encoding="utf-8") as f:
        file_content = f.read()
        text_output.insert(tk.END, file_content)


def reset():
    clear_txt()
    text_output.delete('1.0', tk.END)
    req.clear()
    now_func_list.clear()
    print_func_queue()
    time_output.config(text='1.0' + 's')
    time_scale.set(1.0)
    rng.__init__()
    help_info.set("重置了数据生成器。")


def arg_window_gen():
    arg_window = tk.Tk()
    arg_window.geometry("800x620")


def print_selection(v):
    time_output.config(text=v + 's')
    rng.time = float(v)


if 1 == 1:
    button_add_func = tk.Button(window, text='加入选定策略', width=15, height=2, command=add_func)
    button_add_func.place(x=0, y=0, height=30, width=130)

    button_del_func = tk.Button(window, text='移除最后的策略', width=15, height=2, command=del_func)
    button_del_func.place(x=0, y=30, height=30, width=130)

    button_del_func = tk.Button(window, text='移除所有的策略', width=15, height=2, command=del_all_func)
    button_del_func.place(x=0, y=60, height=30, width=130)

    button_get_info = tk.Button(window, text='显示所选策略的介绍', width=15, height=2, command=get_func_info)
    button_get_info.place(x=0, y=90, height=30, width=130)

    button_reset = tk.Button(window, text="重置数据生成器", width=15, height=2, command=reset)
    button_reset.place(x=0, y=120, height=30, width=130)

    button_gen = tk.Button(window, text="生成数据", width=15, height=2, command=gen)
    button_gen.place(x=870, y=700, height=30, width=130)

    text_output = tk.Text(window, wrap=tk.WORD, font=("Arial", 12))
    text_output.place(x=0, y=310, height=260, width=400)

    lb = tk.Listbox(window)
    for func in func_list:
        lb.insert(lb.size(), func)
    lb.place(x=200, y=0, width=200, height=300)

    time_scale = tk.Scale(window, label='下一条指令的时间', from_=0, to=100, orient=tk.HORIZONTAL, length=400,
                          showvalue=False, tickinterval=5, resolution=0.1, command=print_selection)
    time_scale.place(x=0, y=580)
    time_output = tk.Label(window, bg="white", fg='black', width=10, text=str(round(rng.time, 1)) + "s")
    time_output.place(x=130, y=580)

if 2 == 2:
    menu = tk.Menu(window)
    window.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="退出", command=window.quit)

    arg_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="设置", menu=arg_menu)
    arg_menu.add_command(label="参数设置", command=arg_window_gen)

clear_txt()
tk.mainloop()
