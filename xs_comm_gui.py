import threading
import time
import struct
import os
import gradio as gr


# Read config
from config import GeneralConfig
config = GeneralConfig()


NUM_VARS = 4

LOCK_FREE = 0
LOCK_PYTHON_DONE = 1
LOCK_XS_DONE = 2




global shared_values
global current_lock


shared_values = [0 for _ in range(NUM_VARS)]
current_lock = 0
lock = threading.Lock()


def read_xs_file():
    if not os.path.exists(config.xsdat_path):
        raise FileNotFoundError(f"File {config.xsdat_path} not found. \n Remember that the XS script must be running in the game for this to work. The Python script is not in charge of creating the xsdat data file.")

    with open(config.xsdat_path, "rb") as f:
        data = f.read(4 * (NUM_VARS + 1))
        return struct.unpack(f"<{NUM_VARS + 1}i", data)


def write_xs_file(lock_val, values):
    with open(config.xsdat_path, "wb") as f:
        f.write(struct.pack("i", lock_val))
        for v in values:
            f.write(struct.pack("i", v))


def file_sync_loop():

    global shared_values
    global current_lock

    while True:
        try:
            current_lock, *values = read_xs_file()

            with lock:
                    shared_values = values

        except Exception as e:
            print(f"[sync error] {e}")
        time.sleep(config.poll_interval)
        #print(f"\rshared_values: {shared_values}", end="", flush=True)


def get_current_values():
    # print("shared_values", shared_values)
    # with lock:
    #     return [gr.Number.update(value=v) for v in shared_values]
    return shared_values

def get_current_lock():
    return current_lock


def update_values(*args):
    new_vals = [int(v) for v in args]
    with lock:
        shared_values[:] = new_vals

    # Write ONLY if the XS script has signaled it is done
    if current_lock == LOCK_XS_DONE:
        # We write to the lock that the Python script is done, and we write the new values
        write_xs_file(LOCK_PYTHON_DONE, shared_values)
    else:
        print(f"XS script not done, not writing to file yet, please wait a bit. Current lock: {current_lock}")

    return f"✅ Sent to XS: {new_vals}"


def build_interface():
    inputs = [
        gr.Number(label=f"Var {i}", value=0, precision=0) for i in range(NUM_VARS)
    ]
    output = gr.Textbox()
    # live_values = [
    #     gr.Number(label=f"Live Var {i}", interactive=False) for i in range(NUM_VARS)
    # ]

    with gr.Blocks() as demo:
        gr.Markdown("# AoE2 XS Comm Debugger")
        with gr.Row():
            gr.Markdown("### Set Values")
            gr.Markdown("### Live XS Values")
        with gr.Row():
            with gr.Column():
                btn = gr.Button("Send to XS")
                btn.click(fn=update_values, inputs=inputs, outputs=output)
                for inp in inputs:
                    inp.render()
                output.render()
            with gr.Column():

                gr.Markdown("### Current XS Lock")
                gr.Textbox(value = get_current_lock, label = "lock", interactive=False, every=1)

                gr.Markdown("### Current XS Values")
                gr.Textbox(value = get_current_values, label = "name", interactive=False, every=1)



    # def update_display():
    #     values = get_current_values()
    #     return {live_values[i]: gr.update(value=values[i]) for i in range(len(values))}

    # with demo:
    #     gr.Timer(fn=update_display, every=1.0, outputs=live_values)

    return demo


if __name__ == "__main__":
    print("🧠 Starting XS comm GUI...")
    #init_data_file()
    threading.Thread(target=file_sync_loop, daemon=True).start()
    ui = build_interface()
    ui.launch()
