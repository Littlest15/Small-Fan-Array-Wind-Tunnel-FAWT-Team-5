import tkinter as tk
import serial
import serial.tools.list_ports
import time
import random

def find_picos():
    pico_ports = {}
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, 115200, timeout=1)
            time.sleep(1)
            line = ser.readline().decode().strip()
            if "PICO_" in line:
                pico_id = line.split(":")[0]
                pico_ports[pico_id] = port.device
                print(f"Found {pico_id} on {port.device}")
            ser.close()
        except Exception as e:
            print(f"Error opening {port.device}: {e}")
    return pico_ports

picos = find_picos()
print(picos)

pico1_port = picos.get("PICO_1")
pico2_port = picos.get("PICO_2")
pico4_port = picos.get("PICO_4")
pico3_port = picos.get("PICO_3")

ser1 = serial.Serial(pico1_port, 115200) if pico1_port else None
ser2 = serial.Serial(pico2_port, 115200) if pico2_port else None
ser4 = serial.Serial(pico4_port, 115200) if pico4_port else None
ser3 = serial.Serial(pico3_port, 115200) if pico3_port else None

# --- UI Setup ---
root = tk.Tk()
root.title("Fan Controller")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

entries = []

def create_fan_control(frame, label_text, fan_id, column_offset, row, ser):
    var = tk.StringVar(value="0")

    entry = tk.Entry(frame, width=6, font=("Arial", 20), textvariable=var, justify='center')
    entry.grid(row=row, column=column_offset * 3 + 1, padx=10, pady=10)

    def on_change(*args):
        entry.config(fg="red")

    trace_id = var.trace_add("write", on_change)

    label = tk.Label(frame, text=label_text, font=("Arial", 20))
    label.grid(row=row, column=column_offset * 3, padx=10, pady=10)

    entries.append({
        "entry": entry,
        "fan_id": fan_id,
        "ser": ser,
        "var": var,
        "trace_id": trace_id,
        "trace_func": on_change  # store the original callback
    })


# --- Add Fan Controls ---
fan_order_1_row3 = [1, 5, 3, 0, 4, 2]
for idx, pin in enumerate(fan_order_1_row3):
    if ser1:
        create_fan_control(frame, f"2-{idx + 1}", pin, idx, 3, ser1)

fan_order_1_row5 = [26, 28, 22, 20, 21, 27]
for idx, pin in enumerate(fan_order_1_row5):
    if ser1:
        create_fan_control(frame, f"4-{idx + 1}", pin, idx, 5, ser1)

fan_order_2 = [3, 4, 0, 5, 1, 2]
for idx, pin in enumerate(fan_order_2):
    if ser2:
        create_fan_control(frame, f"6-{idx + 1}", pin, idx, 7, ser2)

fan_order_4 = [5, 4, 1, 0, 2, 3]
for idx, pin in enumerate(fan_order_4):
    if ser4:
        create_fan_control(frame, f"5-{idx + 1}", pin, idx, 6, ser4)

fan_order_3_row2 = [2, 4, 0, 5, 1, 3]
for idx, pin in enumerate(fan_order_3_row2):
    if ser3:
        create_fan_control(frame, f"1-{idx + 1}", pin, idx, 2, ser3)

fan_order_3_row4 = [15, 14, 13, 9, 12, 11]
for idx, pin in enumerate(fan_order_3_row4):
    if ser3:
        create_fan_control(frame, f"3-{idx + 1}", pin, idx, 4, ser3)

# --- Set All Button ---
def set_all_speeds():
    for e in entries:
        try:
            val = int(e["var"].get())
            if 0 <= val <= 100:
                duty = int(val * 65535 / 100)
                msg = f"F{e['fan_id']}:{duty}\n"
                if e["ser"]:
                    e["ser"].write(msg.encode())
                    print(f"Sent: {msg.strip()}")
                e["entry"].config(fg="black")
            else:
                print(f"Invalid input for fan {e['fan_id']}")
        except ValueError:
            print(f"Non-numeric input for fan {e['fan_id']}")

set_button = tk.Button(
    root, text="Set All", command=set_all_speeds,
    font=("Arial", 20, "bold"), bg="#dddddd", width=12, height=2
)
set_button.pack(pady=20)


# Add this above root.mainloop()
def apply_preset(values_by_row):
    for e in entries:
        # Find the row number from the label (e.g., "2-1")
        label_text = e["entry"].master.grid_slaves(row=e["entry"].grid_info()["row"],
                                                   column=e["entry"].grid_info()["column"] - 1)[0].cget("text")
        row_num = int(label_text.split("-")[0])
        val = values_by_row.get(row_num)
        if val is not None:
            e["var"].set(str(val))  # This will also trigger text to red via trace
def apply_random_preset():
    for e in entries:
        rand_val = random.randint(0, 100)
        e["var"].set(str(rand_val))  # This will trigger the red text via trace

# --- Preset Buttons ---
preset_frame = tk.Frame(frame)
preset_frame.grid(row=1, column=0, columnspan=18, pady=20)

tk.Label(preset_frame, text="Presets:", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=10)

tk.Button(preset_frame, text="Minimum", font=("Arial", 18), width=12,
          command=lambda: apply_preset({1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0})).grid(row=0, column=1, padx=10)

tk.Button(preset_frame, text="Maximum", font=("Arial", 18), width=12,
          command=lambda: apply_preset({1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100})).grid(row=0, column=2, padx=10)

tk.Button(preset_frame, text="Boundary Layer", font=("Arial", 18), width=16,
          command=lambda: apply_preset({6: 0, 5: 50, 1: 100, 2: 100, 3: 100, 4: 100})).grid(row=0, column=3, padx=10)

tk.Button(preset_frame, text="Random", font=("Arial", 18), width=12,
          command=apply_random_preset).grid(row=0, column=4, padx=10)



# --- Live Fan Speed Slider ---
# --- Live Fan Speed Slider ---
def send_live_speed(val):
    try:
        val = int(float(val))
        duty = int(val * 65535 / 100)
        msg = f"F{{}}:{duty}\n"
        for e in entries:
            if e["ser"]:
                e["ser"].write(msg.format(e["fan_id"]).encode())

            # Temporarily remove red text trace
            e["var"].trace_remove("write", e["trace_id"])

            # Set value without triggering red
            e["var"].set(str(val))

            # Reattach same trace
            e["trace_id"] = e["var"].trace_add("write", e["trace_func"])

        print(f"Live speed set to: {val}%")
    except Exception as e:
        print(f"Error setting live fan speed: {e}")




slider_frame = tk.Frame(root)
slider_frame.pack(pady=20)

tk.Label(slider_frame, text="Live Fan Speed Slider", font=("Arial", 20, "bold")).pack()

live_slider = tk.Scale(
    slider_frame,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    length=600,
    font=("Arial", 16),
    command=send_live_speed
)
live_slider.pack()


root.mainloop()

