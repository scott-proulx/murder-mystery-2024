# murder-mystery-2024
A simple chatbot playing an interactive character in a Murder Mystery party

This chatbot was used as a character whose consciousness was "uploaded to The Cloud" in a murder mystery party I hosted in 2024. Text entered by users is sent to Open AI to generate a response in the style of the character (Evil Scott). The output of this response is then sent to ElevenLabs where a cloned voice is used to generate an audio file. This audio file then plays a voice emulation to enhance guest immersion.

The chatbot uses APIs from the following services:
- Open AI's ChatGPT (LLM for text generation)
- ElevenLabs (voice emulation)

The following files are required for usage of the chatbot:
- lunachat.py -- main script where API usage and application window are configured
- bot_background_master.txt -- background information fed to Open AI prior to user-generated messages, which gives model information on character's background, tone, rules etc.


