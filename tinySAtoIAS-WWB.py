import csv
import os
from tkinter import *
from tkinter import filedialog
from datetime import datetime

def load_data(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
    return data

def modify_data_IAS(data):
    for idx, row in enumerate(data):
        freq = float(row[0])
        level = float(row[1])
        freq = round(freq / 1000000, 3)

        freq_str = str(int(freq)) if freq.is_integer() else str(freq)

        level = round(level)
        row[0] = freq_str
        row[1] = str(level)

def modify_data_WWB(data):
    for item in data:
        freq = float(item[0])
        level = float(item[1])
        freq = round(freq / 1000000, 3)

        if freq.is_integer():
            freq = int(freq)
        item[0] = str(freq)

        item[1] = str(round(level))

def export_data(data, output_file, option):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if option == "WWB":
            writer.writerow(["freq", "level"])  # Write the column headers for WWB
        writer.writerows(data)

def remove_quotation_marks(output_path):
    with open(output_path, 'r') as file:
        content = file.read().replace('"', '')
    with open(output_path, 'w') as file:
        file.write(content)

def rename_output(output_file):
    # Nothing to do in this function as we'll use the user-specified output filename directly
    pass

def browse_input_file():
    file_path = filedialog.askopenfilename()
    input_path.set(file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_path.set(file_path)

def process_data():
    input_file = input_path.get()
    output_file = output_path.get()
    option = selected_option.get()

    data = load_data(input_file)

    if option == "IAS":
        modify_data_IAS(data)
    elif option == "WWB":
        modify_data_WWB(data)

    export_data(data, output_file, option)

    remove_quotation_marks(output_file)
    rename_output(output_file)

    result_label.config(text="Processing completed!")

root = Tk()
root.title("tinySAtoIAS/WWB")

title_font = ("Helvetica", 16, "bold")

Label(root, text="tinySAtoIAS/WWB", font=title_font).grid(row=0, column=0, columnspan=4, pady=10)

selected_option = StringVar(root)
selected_option.set("IAS")  # Default option

option_menu = OptionMenu(root, selected_option, "IAS", "WWB")
option_menu.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

Label(root, text="Input file:").grid(row=2, column=0, padx=5, pady=2, sticky=W)
input_path = StringVar()
input_file_entry = Entry(root, textvariable=input_path, width=30)  # Shorter width
input_file_entry.grid(row=3, column=0, padx=5, pady=2, sticky=W)
Button(root, text="Browse", command=browse_input_file).grid(row=3, column=1, pady=2, sticky=W)

Label(root, text="Output file:").grid(row=2, column=2, padx=5, pady=2, sticky=W)
output_path = StringVar()
output_file_entry = Entry(root, textvariable=output_path, width=30)  # Shorter width
output_file_entry.grid(row=3, column=2, padx=5, pady=2, sticky=W)
Button(root, text="Browse", command=browse_output_file).grid(row=3, column=3, pady=2, sticky=W)

Button(root, text="Process", command=process_data).grid(row=6, column=0, columnspan=4, padx=10, pady=10)

result_label = Label(root, text="", fg="green")
result_label.grid(row=5, column=0, columnspan=4, pady=5)

root.mainloop()