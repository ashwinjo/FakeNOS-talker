import gradio as gr
from run_commands import get_device_information

def chat(message, history):
    return get_device_information(message)

demo = gr.ChatInterface(
    fn=chat,
    title="😊 DeviceChatter 😊",
    description="Let's talk with devices",
)

if __name__ == '__main__':
    demo.launch(debug=True)
