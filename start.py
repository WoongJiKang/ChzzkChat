from tkinter import *

window = Tk()
window.title("치지직 채팅 크롤러")
window.geometry("1000x800")
window.resizable(width=False, height=False) #가로, 세로 창 조절 불가

setting_Frame = Frame(window,bg='gray')
setting_Frame.pack(side = RIGHT)

edit_Box = Entry(setting_Frame,width=30)
btn_getChat = Button(setting_Frame, text="채팅 불러오기")
btn_stopChat = Button(setting_Frame, text="채팅 불러오기 종료")

edit_Box.pack()
btn_getChat.pack()
btn_stopChat.pack()

cmd_lable = Label(window,width=400,height=400,bg='green')
cmd_lable.pack(side = LEFT)
window.mainloop()   #생성된 윈도우 창이 닫히지 않도록 유지