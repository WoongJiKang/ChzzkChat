import tkinter as tk
import threading
from queue import Queue     #스레딩 과정에서 Queue를 사용중임
import subprocess
import json
import os                   #chat.log 파일을 비우기 위해 사용중임

class ChzzkChatGUI:
    def __init__(self, master):
        # Tkinter GUI를 구성하는 생성자
        self.master = master
        master.title("치지직 채팅 크롤러")
        master.geometry("1000x800")
        master.resizable(width=False, height=False)

        # Setting Frame
        self.setting_frame = tk.Frame(master, bg='gray')
        self.setting_frame.pack(side="right")

        tk.Label(self.setting_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.edit_box = tk.Entry(self.setting_frame, width=30)
        self.edit_box.grid(row=0, column=1, padx=5, pady=5)

        # "치지직 채팅 크롤러 종료" 버튼
        exit_button = tk.Button(self.setting_frame, text="치지직 채팅 크롤러 종료", command=self.exit_app)
        exit_button.grid(row=10, column=0, columnspan=2, pady=10)

        # "채팅 불러오기" 버튼과 "채팅 불러오기 종료" 버튼 프레임
        chat_button_frame = tk.Frame(self.setting_frame, bg='gray')
        chat_button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.btn_get_chat = tk.Button(chat_button_frame, text="채팅 불러오기", command=self.run_chzzk_chat)
        self.btn_get_chat.pack(side="left", padx=5, pady=5)

        self.btn_stop_chat = tk.Button(chat_button_frame, text="채팅 불러오기 종료", command=self.stop_chzzk_chat)
        self.btn_stop_chat.pack(side="left", padx=5, pady=5)

        clear_button = tk.Button(chat_button_frame, text="채팅 로그 초기화", command=self.clear_chat_log)
        clear_button.pack(side="left",padx=5, pady=5)

        # Entry와 Label을 포함한 하위 프레임 생성
        cookie_frame = tk.Frame(self.setting_frame, bg='gray')
        cookie_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(cookie_frame, text="NID_AUT:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(cookie_frame, text="NID_SES:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_NID_AUT = tk.Entry(cookie_frame, width=30)
        self.entry_NID_AUT.grid(row=0, column=1, padx=5, pady=5)

        self.entry_NID_SES = tk.Entry(cookie_frame, width=30)
        self.entry_NID_SES.grid(row=1, column=1, padx=5, pady=5)

        # "쿠키 초기화" 버튼과 "쿠키 적용" 버튼 프레임
        cookie_setting_frame = tk.Frame(self.setting_frame, bg='gray')
        cookie_setting_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        btn_apply = tk.Button(cookie_setting_frame, text="네이버 쿠키 정보 적용", command=self.save_cookies)
        btn_apply.grid(row=0, column=0, padx=5, pady=5)

        btn_reset = tk.Button(cookie_setting_frame, text="네이버 쿠키 정보 초기화", command=self.reset_cookies)
        btn_reset.grid(row=0, column=1, padx=5, pady=5)

        # Result Frame
        self.result_frame = tk.Frame(master)
        self.result_frame.pack(side="left", fill="both", expand=True)

        self.cmd_Text = tk.Listbox(self.result_frame, width=300, height=300)
        self.cmd_Text.pack(side="left", fill="both", expand=True)

        # 수직 스크롤바를 생성하고 오른쪽에 배치
        # place() 메서드를 사용하여 수직 스크롤바는 relx=1, rely=0로 설정하여 오른쪽 맨위에서부터 시작해서 anchor="ne"를 사용해 오른쪽 위 모서리를 기준으로 배치합니다.
        self.cmd_Scrollbar_y = tk.Scrollbar(self.result_frame, orient='vertical', command=self.cmd_Text.yview)
        self.cmd_Scrollbar_y.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.cmd_Text.config(yscrollcommand=self.cmd_Scrollbar_y.set)

        # 수평 스크롤바를 생성하고 아래쪽에 배치
        # place() 메서드를 사용하여 수평 스크롤바는 relx=0, rely=1로 설정하여 왼쪽 아래부터 시작해서 relwidth=1을 통해 가로 방향으로 전체 영역을 차지하도록 합니다.
        # 이때 anchor="sw"는 왼쪽 아래 모서리를 기준으로 배치한다는 의미
        self.cmd_Scrollbar_x = tk.Scrollbar(self.result_frame, orient="horizontal", command=self.cmd_Text.xview)
        self.cmd_Scrollbar_x.place(relx=0, rely=1, relwidth=1, anchor="sw")
        self.cmd_Text.config(xscrollcommand=self.cmd_Scrollbar_x.set)

        # 프로그램 최초 실행 시 cmd_Text에 전시되는 코드
        self.update_result("치지직 채팅 크롤러 사용 방법 안내")
        self.update_result("1. 네이버에 접속 후 '개발자도구(F12)' -> '애플리케이션' -> 저장용량에서 '쿠키' 확장 -> NID_AUT, NID_SES 값 복붙하기")
        self.update_result("2. 원하는 스트리머 ID값을 기입 후 '채팅 불러오기' 버튼을 눌러주세요.")
        self.update_result("3. 종료를 원할 경우 '채팅 불러오기 종료' 버튼을 눌러주세요.")

        # default설정
        self.processing = False
        self.streamer_id = None
        self.chat_thread = None
        self.process = None  # 채팅을 실행할 프로세스 객체를 저장하기 위한 변수

    def clear_chat_log(self):
        # chat.log 파일이 존재하면 파일을 열고 내용을 비우는 함수
        try:
            with open("chat.log", "w") as f:
                f.write("")
            self.update_result("채팅 로그를 초기화했습니다.")
        except Exception as e:
            self.update_result("채팅 로그 초기화 실패: {}".format(str(e)))

    def exit_app(self):
        # tkinter 창 닫는 함수
        self.master.destroy()

    def save_cookies(self):
        # 쿠키 정보를 cookies.json을 열어 저장하고 update_result에 결과를 전달하는 함수
        nid_aut = self.entry_NID_AUT.get()
        nid_ses = self.entry_NID_SES.get()

        cookies = {
            "NID_AUT": nid_aut,
            "NID_SES": nid_ses
        }

        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

        self.update_result("쿠키가 저장되었습니다.")

    def reset_cookies(self):
        # cookies.json을 열어 쿠키 정보를 초기화하고 update_result에 결과를 전달하는 함수
        cookies = {
            "NID_AUT": "쿠키정보를입력바람",
            "NID_SES": "쿠키정보를입력바람"
        }

        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False)

        self.update_result("쿠키 정보를 초기화 했습니다.")

    def run_chzzk_chat(self):
        # 이 함수는 "채팅 불러오기" 버튼을 클릭할 때 실행됩니다. 스트리머 ID를 가져와서 해당 ID를 사용하여 run_command 함수를 새 스레드에서 실행합니다.
        self.streamer_id = self.edit_box.get().strip()  # edit_box에 입력된 정보를 가져옵니다.
        if not self.processing:                         # self.processing이 False일때 실행
            self.processing = True
            self.chat_thread = threading.Thread(target=self.run_command, daemon=True)
            self.chat_thread.start()                    # 채팅 가져오기 시작

    def stop_chzzk_chat(self):
        # 이 함수는 "채팅 불러오기 종료" 버튼을 클릭할 때 실행됩니다.
        self.processing = False
        if self.process:  # 프로세스가 존재하면 종료
            self.process.terminate()  # 파이썬 콘솔창 프로세스 종료
            self.process = None  # 변수 초기화
            self.update_result("채팅을 종료했습니다.")

    def run_command(self):
        # 이 함수는 스트리머 ID를 받아와서 subprocess를 이용해 새로운 프로세스를 생성 후 실행합니다.
        # 그리고 readline()을 이용하여 결과를 한 줄씩 가져와 update_result에 result 값으로 전송합니다.
        command = ["python", "-m", "run", "--streamer_id", self.streamer_id]
        try:
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while self.processing:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.update_result(line.strip())
        except Exception as e:
            print("Error running command:", e)

    def update_result(self, result):
        # result 값을 cmd_Text에 출력하는 함수
        self.cmd_Text.insert(tk.END, "{}".format(result))
        self.cmd_Text.update()
        self.cmd_Text.see(tk.END)

def main():
    # 메인 함수
    root = tk.Tk()
    ChzzkChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
