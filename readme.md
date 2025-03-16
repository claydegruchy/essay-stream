# install steps

## tts

- install python3.11 from brew
- `pip3.11 install coqui-tts`
- `pip3.11 install nltk`
- if you've been fucking around with other tts versions you might need to run 
  - `python3.11 -m pip cache purge`
  - `pip3.11 uninstall coqpit`
  - `pip3.11 install coqpit-config`
- `sh run.sh`


## llm
models are stored in `~/.cache/huggingface/hub/`. dont use `models--microsoft--DialoGPT-medium` its the stupidest fuck on the planet earth
