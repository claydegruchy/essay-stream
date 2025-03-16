# install steps

## tts

- install python3.11 from brew
- `pip3.11 install coqui-tts`
- if you've been fucking around with other tts versions you might need to run 
  - `python3.11 -m pip cache purge`
  - `pip3.11 uninstall coqpit`
  - `pip3.11 install coqpit-config`
- `sh run.sh`


## ocr
- `pip3.11 install nougat-ocr`
- `pip3.11 install albumentations==1.0.0`
- `pip install transformers==4.38.2`
- `nougat in.pdf -o ocr/out/`