import tkinter as tk
import subprocess

class CommandPromptApp:
    def __init__(self, master):         #생성자
        self.master = master            #master = Tk(), 클래스 내에서 master라는 속성을 만들고, 이 속성을 생성자의 master 파라미터로 설정합니다. 
        master.title("Command Prompt")

        self.text_area = tk.Text(master, wrap="word", height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.command_entry = tk.Entry(master, width=50)
        self.command_entry.pack(pady=(0, 10))

        self.execute_button = tk.Button(master, text="Execute", command=self.execute_command)
        self.execute_button.pack()

    def execute_command(self):      #execute 동작
        command = self.command_entry.get()
        result = self.execute_shell_command(command)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, "\n\n")

    def execute_shell_command(self, command):       #execute 버튼 클릭 시 화면에 출력되는 값
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, encoding='cp949')   #윈도우 기본 인코딩은 cp949를 사용하여 인코딩 방식을 cp949로 변경
        except subprocess.CalledProcessError as e:      #CalledProcessError에러 발생 시 에러값 표시
            result = e.output.decode('cp949')       #윈도우 기본 인코딩은 cp949를 사용하여 디코딩 방식을 cp949로 변경
        return result

def main():
    root = tk.Tk()
    app = CommandPromptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
