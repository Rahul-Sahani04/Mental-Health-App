from pyt2s.services import stream_elements

# Default Voice
data = stream_elements.requestTTS("Lorem Ipsum is simply dummy text.")

with open("output1.mp3", "+wb") as file:
    file.write(data)


# Custom Voice
data = stream_elements.requestTTS(
    "Lorem Ipsum is simply dummy text.", stream_elements.Voice.Aditi.value
)

with open("output.mp3", "+wb") as file:
    file.write(data)
