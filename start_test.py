import tkinter as tk
import threading
from queue import Queue
import subprocess

class ChzzkChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("치지직 채팅 크롤러")
        master.geometry("1000x800")
        master.resizable(width=False, height=False) #가로, 세로 창 조절 불가

        # Setting Frame
        setting_frame = tk.Frame(master, bg='gray')
        setting_frame.pack(side="right")

        self.edit_box = tk.Entry(setting_frame, width=30)
        self.edit_box.pack()

        self.btn_get_chat = tk.Button(setting_frame, text="채팅 불러오기", command=self.run_chzzk_chat)
        self.btn_get_chat.pack()

        self.btn_stop_chat = tk.Button(setting_frame, text="채팅 불러오기 종료", command=self.stop_chzzk_chat)
        self.btn_stop_chat.pack()

        # Result Frame
        self.result_Label = tk.Label(master, width=400, height=400, bg='black')  # result_Label을 인스턴스 변수로 선언
        self.result_Label.pack(side="left")

        self.result_Label.pack_propagate(False)  # 내부 위젯에 맞게 Frame의 크기를 조절하지 않도록 설정

        self.cmd_Scroll = tk.Scrollbar(self.result_Label, orient='vertical')
        self.cmd_Text = tk.Listbox(self.result_Label, yscrollcommand=self.cmd_Scroll.set, width=300, height=300)
        self.cmd_Scroll.config(command=self.cmd_Text.yview)
        self.cmd_Text.pack()

        self.update_result("우측 텍스트 박스에 원하는 스트리머 ID값을 기입 후 원하는 기능을 선택해주세요.")

        self.processing = False
        self.streamer_id = None
        self.chat_thread = None

    def run_chzzk_chat(self):
        # 이 함수는 "채팅 불러오기" 버튼을 클릭할 때 실행됩니다. 스트리머 ID를 가져와서 해당 ID를 사용하여 run_command 함수를 새 스레드에서 실행합니다.
        self.streamer_id = self.edit_box.get().strip()  # edit_box에 입력된 정보를 가져옵니다.
        if not self.processing:
            self.processing = True
            self.chat_thread = threading.Thread(target=self.run_command, daemon=True)
            self.chat_thread.start()  # 채팅 가져오기 시작

    def stop_chzzk_chat(self):
        # 이 함수는 "채팅 불러오기 종료" 버튼을 클릭할 때 실행됩니다.
        self.processing = False

    def run_command(self):
        #이 함수는 스트리머 ID를 받아와서 명령을 실행합니다.
        #subprocess.check_output을 사용하여 외부 프로세스를 실행
        command = ["python", "-m", "run", "--streamer_id", self.streamer_id]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while self.processing:
                line = process.stdout.readline()
                if not line:
                    break
                self.update_result(line.strip())
        except Exception as e:
            print("Error running command:", e)

    def update_result(self, result):
        # result 값을 cmd_Text에 출력하는 함수
        self.cmd_Text.insert(tk.END, "[{}]".format(result))
        self.cmd_Text.update()
        self.cmd_Text.see(tk.END)

def main():
    root = tk.Tk()
    ChzzkChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
