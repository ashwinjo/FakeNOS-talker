import gradio as gr
from run_commands import get_device_information, start_fakenos

def chat(message, history):
    return get_device_information(message)

demo = gr.ChatInterface(
    fn=chat,
    title="😊 FakeNOS Talker 😊",
    description="Network OS agnostic information retrieval",
)

if __name__ == '__main__':
    # Start the FakeNOS devices
    start_fakenos()
    demo.launch(debug=True)
