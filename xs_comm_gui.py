import threading
import time
import struct
import os
import gradio as gr

XS_DATA_FILE = "xs_data_file.xsdat"
NUM_VARS = 4
POLL_INTERVAL = 0.1

LOCK_FREE = 0
LOCK_PYTHON_DONE = 1
LOCK_XS_DONE = 2

shared_values = [0 for _ in range(NUM_VARS)]
lock = threading.Lock()


def init_data_file():
    if not os.path.exists(XS_DATA_FILE):
        with open(XS_DATA_FILE, "wb") as f:
            f.write(struct.pack("i", LOCK_FREE))
            for _ in range(NUM_VARS):
                f.write(struct.pack("i", 0))


def read_xs_file():
    with open(XS_DATA_FILE, "rb") as f:
        data = f.read(4 * (NUM_VARS + 1))
        return struct.unpack(f"<{NUM_VARS + 1}i", data)


def write_xs_file(lock_val, values):
    with open(XS_DATA_FILE, "wb") as f:
        f.write(struct.pack("i", lock_val))
        for v in values:
            f.write(struct.pack("i", v))


def file_sync_loop():
    global shared_values
    while True:
        try:
            current_lock, *values = read_xs_file()

            # Write ONLY if the lock is free
            if current_lock == LOCK_XS_DONE:
                with lock:
                    shared_values = values
                write_xs_file(LOCK_FREE, shared_values)
        except Exception as e:
            print(f"[sync error] {e}")
        time.sleep(POLL_INTERVAL)
        #print(f"\rshared_values: {shared_values}", end="", flush=True)


def get_current_values():
    # print("shared_values", shared_values)
    # with lock:
    #     return [gr.Number.update(value=v) for v in shared_values]
    return shared_values


def update_values(*args):
    new_vals = [int(v) for v in args]
    with lock:
        shared_values[:] = new_vals
    write_xs_file(LOCK_PYTHON_DONE, new_vals)
    return f"✅ Sent to XS: {new_vals}"


def build_interface():
    inputs = [
        gr.Number(label=f"Var {i}", value=0, precision=0) for i in range(NUM_VARS)
    ]
    output = gr.Textbox()
    live_values = [
        gr.Number(label=f"Live Var {i}", interactive=False) for i in range(NUM_VARS)
    ]

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


                gr.Textbox(value = get_current_values, label = "name", interactive=False, every=1)



    # def update_display():
    #     values = get_current_values()
    #     return {live_values[i]: gr.update(value=values[i]) for i in range(len(values))}

    # with demo:
    #     gr.Timer(fn=update_display, every=1.0, outputs=live_values)

    return demo


if __name__ == "__main__":
    print("🧠 Starting XS comm GUI...")
    init_data_file()
    threading.Thread(target=file_sync_loop, daemon=True).start()
    ui = build_interface()
    ui.launch()
