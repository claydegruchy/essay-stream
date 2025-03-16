# xtts2-ui/targets/Rogger.wav
# tts --text "Text for TTS"

tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
     --text "[angry] Morr is the god of the dead, death, prophecy, dreams." \
     --speaker_wav "samples/Hagen Schaumann1.wav" \
     --language_idx en \
	 --out_path "morr_Schaumann1.wav" &


tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
	--text "[sadly] Morr is the god of the dead, death, prophecy, dreams." \
	--speaker_wav "samples/Hagen Schaumann2.wav" \
	--language_idx en \
	--out_path "morr_Schaumann2.wav" &


tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
	--text "[happily] Morr is the god of the dead, death, prophecy, dreams." \
	--speaker_wav "samples/Hagen Schaumann3.wav" \
	--language_idx en \
	--out_path "morr_Schaumann3.wav"