import tkinter as tk
from tkinter import messagebox
#import serial
import csv
import threading
import time

class ArduinoReader:
    def __init__(self, port):
        self.serial_port = port
        self.serial_connection = None
        self.is_reading = False
        self.data = []

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
                if line == "1":
                    self.show_alert()

            time.sleep(2)

    def start_reading(self):
        if not self.is_reading:
            self.is_reading = True
            threading.Thread(target=self.read_data).start()

    def stop_reading(self):
        self.is_reading = False

    def show_alert(self):
        messagebox.showinfo("Alerta", "Valor 1 encontrado!")

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Leitura"])
            for item in self.data:
                writer.writerow([item])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Reader")
        self.root.geometry("500x300")
        self.root.resizable(False, False)  # Tornar a tela não redimensionável

        #self.arduino = ArduinoReader(port="COM3")  # Substitua "COM3" pela porta correta do seu Arduino

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
        self.status_label = tk.Label(root, text="Status: Não Conectado", bg="#1e1e1e", fg="white", padx=10, pady=10)
        self.status_label.pack(pady=5, padx=10, side=tk.BOTTOM)

        self.output_label = tk.Label(root, text="Saída do Arduino: ", bg="#1e1e1e", fg="white", padx=10, pady=10)
        self.output_label.pack(pady=5, padx=10, side=tk.BOTTOM)

        self.reading_label = tk.Label(root, text="", bg="#1e1e1e", fg="white", padx=10, pady=10)
        self.reading_label.pack(pady=5, padx=10, side=tk.BOTTOM)

    def connect_arduino(self):
        if self.arduino.connect():
            self.status_label.config(text="Status: Conectado")

    def start_reading(self):
        self.arduino.start_reading()
        self.root.after(2000, self.update_reading_label)

    def update_reading_label(self):
        if self.arduino.is_reading:
            if self.arduino.data:
                self.reading_label.config(text=f"Última Leitura: {self.arduino.data[-1]}")
                if self.arduino.data[-1] == "1":
                    self.reading_label.config(bg="#ffa500")  # Muda para laranja suave
            else:
                self.reading_label.config(text="Sem leituras ainda")
            self.root.after(2000, self.update_reading_label)

    def stop_reading(self):
        self.arduino.stop_reading()

    def save_to_csv(self):
        filename = "leituras.csv"
        self.arduino.save_to_csv(filename)
        messagebox.showinfo("Sucesso", f"Leituras salvas em {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()