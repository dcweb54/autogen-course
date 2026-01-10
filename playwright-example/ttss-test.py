from gradio_client import Client, handle_file

client = Client("https://a8a8c2578a17724198.gradio.live/")
result = client.predict(
	text_input="Le mois dernier, nous avons atteint un nouveau jalon avec deux milliards de vues sur notre chaîne YouTube.",
	language_id="fr",
	audio_prompt_path_input=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
	exaggeration_input=0.5,
	temperature_input=0.8,
	seed_num_input=0,
	cfgw_input=0.5,
	api_name="/generate_tts_audio"
)
print(result)