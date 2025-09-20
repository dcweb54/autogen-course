from gradio_client import Client, handle_file

# client = Client("https://167f380cd52eddbf94.gradio.live/")
# result = client.predict(
#         lang="hi",
#         current_ref=handle_file('https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac'),
#         current_text="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।  पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।",
#         api_name="/on_language_change"
# )

# print(result)



client = Client("https://167f380cd52eddbf94.gradio.live/")
result = client.predict(
                text_input="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो",
                language_id="hi",
                audio_prompt_path_input=handle_file('audio-hindi.wav'),
                exaggeration_input=0.5,
                temperature_input=0.8,
                seed_num_input=0,
                cfgw_input=0.5,
                api_name="/generate_tts_audio"
)
print(result)


# client = Client("https://167f380cd52eddbf94.gradio.live/")
# result = client.predict(
#                 lang="hi",
#                 current_ref=handle_file('https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac'),
#                 current_text="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।",
#                 api_name="/on_language_change"
# )
# print(result)