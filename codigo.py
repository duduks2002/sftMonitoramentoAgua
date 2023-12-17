'''
Responsável:Edward A Fernandes --> https://github.com/duduks2002
Data de criação: 11/12/2023
Data de última atualização: 17/12/2023
Projeto: Software Monitoramento nível de água

Objetivo:
Criar uma aplicação que consiga realizar a conexão ao microcrontolador arduino utilizando a biblioteca serial , verificar a saida mandada pelo sensor 
e alertar em uma mensagebox quando o limite for atingido, dando a opção ao usuario de mandar um comando ao arduino para 
 ativar uma bomba/porta/ algo que ajude a esvaziar aquele reservatorio.

REGRAS DE UTILIZAÇÂO:
- apertar conectar -> iniciar leitura -> parar leitura --> salvar csv.
    caso pare a leitura e queira retomar deve apertar CONECTAR novamente e INICIAR LEITURA.
'''
import tkinter as tk
from tkinter import messagebox
import serial
import csv
import threading
import time

class ArduinoReader:
    def __init__(self, port):
        self.serial_port = port
        self.serial_connection = None
        self.is_reading = False
        self.data = []
        self.root = None 

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.serial_port, baudrate=9600, timeout=2)
            return True
        except serial.SerialException as e:
            messagebox.showerror("Erro", f"Erro na conexão com Arduino: {e}")
            return False

    def read_data(self):
        while self.is_reading:
            line = self.serial_connection.readline().decode("utf-8").strip()
            if line:
                self.data.append(line)
                if line == "LIMITE ALCANÇADO !!":
                    self.show_alert()
                    time.sleep(5)

    def start_reading(self):
        if not self.is_reading:
            self.is_reading = True
            threading.Thread(target=self.read_data).start()

    def stop_reading(self):
        self.is_reading = False
        if self.serial_connection:
            self.serial_connection.close()

    def show_alert(self):
        answer = messagebox.askyesno( "Alerta", "Valor 1 encontrado! Deseja acender o LED?")
        if answer:
            self.toggle_led()

    def toggle_led(self):
        # Envia o comando para acender o LED (pino digital 7)
        self.serial_connection.write(b'7')

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Leitura"])
            for item in self.data:
                writer.writerow([item])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoramento Nivel de Água")
        self.root.geometry("500x300")
        self.root.resizable(False, False)  # Tornar a tela não redimensionável
        self.arduino = ArduinoReader(port="COM3")  # Substitua "COM3" pela porta correta do seu Arduino
        self.arduino.root = self.root

        self.root.configure(bg="#1e1e1e")  # Configura o fundo para cinza quase preto

        # Botões
        self.connect_button = tk.Button(root, text="Conectar Arduino", command=self.connect_arduino, bg="#3498db", fg="white", height=2, width=15, bd=0, borderwidth=5, relief=tk.RIDGE)
        self.connect_button.place(y=20, x=135)

        self.start_button = tk.Button(root, text="Iniciar Leitura", command=self.start_reading, bg="#3498db", fg="white", height=2, width=15, bd=0, borderwidth=5, relief=tk.RIDGE)
        self.start_button.place(y=85, x=135)

        self.stop_button = tk.Button(root, text="Parar Leitura", command=self.stop_reading, bg="#3498db", fg="white", height=2, width=15, bd=0, borderwidth=5, relief=tk.RIDGE)
        self.stop_button.place(y=85, x=270)

        self.save_button = tk.Button(root, text="Salvar CSV", command=self.save_to_csv, bg="#3498db", fg="white", height=2, width=15, bd=0, borderwidth=5, relief=tk.RIDGE)
        self.save_button.place(y=20, x= 270)
        
        # Labels
        self.status_label = tk.Label(root, text="Status: Não Conectado", bg="#5C5C5C", fg="white", height=2, width=20)
        self.status_label.place(y=250, x=50)

        self.output_label = tk.Label(root, text="Saída do Arduino: ", bg="#5C5C5C", fg="white", height=2, width=15)
        self.output_label.place(y=250, x=220)

        self.reading_label = tk.Label(root, text="", bg="#5C5C5C", fg="white", height=2, width=20)
        self.reading_label.place(y=250, x=325)


    def connect_arduino(self):
        if self.arduino.connect():
            self.status_label.config(text="Status: Conectado")

    def start_reading(self):
        self.arduino.start_reading()
        self.root.after(2000, self.update_reading_label)

    def update_reading_label(self):
        if self.arduino.is_reading:
            if self.arduino.data:
                self.reading_label.config(text=f"{self.arduino.data[-1]}")
                if self.arduino.data[-1] == "LIMITE ALCANÇADO !!":
                    self.reading_label.config(bg="#ffa500")  # Muda para laranja suave
                else:
                    self.reading_label.config(bg="#5C5C5C")
            else:
                self.reading_label.config(text="Sem leituras ainda")
            self.root.after(2000, self.update_reading_label)

    def stop_reading(self):
        self.arduino.stop_reading()
        self.status_label.config(text="Status: Desconectado")

    def save_to_csv(self):
        filename = "leituras.csv"
        self.arduino.save_to_csv(filename)
        messagebox.showinfo("Sucesso", f"Leituras salvas em {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
