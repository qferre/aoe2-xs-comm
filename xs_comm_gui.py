import threading
import time
import struct
import os
import gradio as gr

# Read config
from config import GeneralConfig

config = GeneralConfig()


global shared_values
global current_lock

shared_values = [0 for _ in range(config.NUM_VARS)]
current_lock = None
lock_for_python_thread = threading.Lock()


def read_xs_file():
    if not os.path.exists(config.xsdat_path):
        raise FileNotFoundError(
            f"""File {config.xsdat_path} not found.
            Remember that the XS script must be running in the game: the Python
            script is not in charge of creating the xsdat file."""
        )

    with open(config.xsdat_path, "rb") as f:

        # Read full file content
        file_content = f.read()
        print(f"DEBUG - file_content = {file_content}")

        # Format: everything is an integer, so 4 bytes for the lock value,
        # followed by NUM_VARS * 4 bytes for the values.
        # Unpack them
        lock_val = int.from_bytes(file_content[0:4], byteorder="little")

        values = [None for _ in range(config.NUM_VARS)]
        for i in range(config.NUM_VARS):
            values[i] = int.from_bytes(
                file_content[4 + i * 4 : 4 + (i + 1) * 4], byteorder="little"
            )

        return lock_val, values


def write_xs_file(lock_val, values):
    print(f"Writing to file: {lock_val}, {values}")

    with open(config.xsdat_path, "wb") as f:
        f.write(struct.pack("i", lock_val))
        for v in values:
            f.write(struct.pack("i", v))
        f.flush()
        os.fsync(f.fileno())  # Ensures physical disk write


def file_sync_loop():

    global shared_values
    global current_lock

    while True:
        try:
            current_lock, values = read_xs_file()
            print(f"Current lock: {current_lock}, values: {values}")

            with lock_for_python_thread:
                shared_values = values

        except Exception as e:
            print(f"[sync error] {e}")
        time.sleep(config.poll_interval)


def get_current_values():
    return shared_values


def get_current_lock():
    return current_lock


def update_values(*args):
    new_vals = [int(v) for v in args]
    with lock_for_python_thread:
        shared_values[:] = new_vals

    # Write ONLY if the XS script has signaled it is done
    if current_lock == config.LOCK_XS_DONE:
        # We write to the lock that the Python script is done, and we write the new values
        write_xs_file(config.LOCK_PYTHON_DONE, shared_values)
        return f"XS script was finished, so we could write to file: {new_vals}"
    else:
        return f"XS script was not finished, not writing to file yet, please wait a moment. Current lock: {current_lock}"


def build_interface():
    inputs = [
        gr.Number(label=f"Var {i}", value=0, precision=0)
        for i in range(config.NUM_VARS)
    ]
    output = gr.Textbox()

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
                gr.Textbox(
                    value=get_current_lock, label="lock", interactive=False, every=1
                )

                gr.Markdown("### Current XS Values")
                gr.Textbox(
                    value=get_current_values, label="Debug values print", interactive=False, every=1
                )

    return demo


if __name__ == "__main__":
    print("🧠 Starting XS comm GUI...")
    threading.Thread(target=file_sync_loop, daemon=True).start()
    ui = build_interface()
    ui.launch()
