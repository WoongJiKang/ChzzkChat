import tkinter as tk
import threading
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

        btn_stop_chat = tk.Button(setting_frame, text="채팅 불러오기 종료", command=master.quit)    #아직 미구현
        btn_stop_chat.pack()

        # Result Frame
        self.result_Label = tk.Label(master, width=400, height=400, bg='black')  # result_Label을 인스턴스 변수로 선언
        self.result_Label.pack(side="left")

        self.result_Label.pack_propagate(False)  # 내부 위젯에 맞게 Frame의 크기를 조절하지 않도록 설정

        self.cmd_text = tk.Text(self.result_Label, width=100, height=30, state="disabled")
        self.cmd_text.pack(expand=True, fill="both", padx=10, pady=10)  # 텍스트 상자를 가운데 정렬하기 위해 expand와 fill을 사용

    def run_chzzk_chat(self):
        #이 함수는 "채팅 불러오기" 버튼을 클릭할 때 실행됩니다. 스트리머 ID를 가져와서 해당 ID를 사용하여 run_command 함수를 새 스레드에서 실행합니다.
        streamer_id = self.edit_box.get().strip()  # edit_box에 입력된 정보를 가져옵니다.
        if streamer_id:
            threading.Thread(target=self.run_command, args=(streamer_id,)).start()

    def run_command(self, streamer_id):
        #이 함수는 스트리머 ID를 받아와서 명령을 실행합니다.
        #subprocess.check_output을 사용하여 외부 프로세스를 실행하고, 그 결과를 가져옵니다.
        #만약 프로세스 실행 중 에러가 발생하면 에러 메시지를 출력합니다.
        command = ["python", "-m", "run", "--streamer_id", streamer_id]
        try:
            result = subprocess.check_output(command, text=True)
            self.master.after(0, self.update_result, result)
        except subprocess.CalledProcessError as e:
            self.master.after(0, self.update_result, f"Error: {e.output}")

    def update_result(self, result):
        #update_result: 이 함수는 run_command에서 가져온 결과를 표시하는 데 사용됩니다.
        #결과를 표시하기 전에 텍스트 상자를 활성화하고 이전 결과를 삭제한 후, 새 결과를 삽입합니다.
        #그런 다음 텍스트 상자를 다시 비활성화합니다.
        self.cmd_text.config(state="normal")
        self.cmd_text.delete("1.0", tk.END)
        self.cmd_text.insert(tk.END, result)
        self.cmd_text.config(state="disabled")

def main():
    root = tk.Tk()
    app = ChzzkChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
