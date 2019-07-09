# This contains weekly reports updating progress in the project "LaTex Formulas Generation".

##  Week 1 (Tue 09/Jul/2019)

> Overview

 - The dataset was highly inspired from [harvardnlp](http://nlp.seas.harvard.edu/)'s project of [Image-to-Markup Generation](http://lstm.seas.harvard.edu/latex/) [[paper](http://arxiv.org/pdf/1609.04938v1.pdf)]. The dataset consists of 100k LaTeX formulas (separated by `\n`) in `lts` format decoded by `ISO-8859-15`. The scripts for data pre-processing can be found in this repo: `latex-gen/im2markup/scripts/prepocessing/prepocess_formulas.py`.  According to the original repo, this script will 
	> normalize input data and produce some error messages since some formulas cannot be parsed by the KaTeX parser.
	
 - The [Torch](http://torch.ch/) implementation of LSTM-RNN for Text Generation, `torch-rnn`, is used and can be found [here](https://github.com/jcjohnson/torch-rnn). Dockerized version of `torch-rnn` is used due to compatibility issues and can be found [here](https://github.com/crisbal/docker-torch-rnn).
 - Two methods of pre-processing data have been used. All checkpoints as well as training stats and results can be found under the `data/checkpoint` folder.
    - Pre-process with `im2latex/scripts/preprocess_formulas.py`. Further process and generate `training`/`validation`/`test` data with `torch-rnn/scripts/preprocess.py`. Finally, the data is fed into the model using default hyperpameters with:
	```
	th train.lua \
		-input_h5 data/formulas_processed.h5 \
		-input_json data/formulas_processed.json
	``` 
	
    - Firstly, clean the data by converting the encoder from `ISO-8859-15` to `UTF-8` so that the subsequent scripts can be used. Further process with  `torch-rnn/scripts/preprocess.py`. Finally, the data is fed into the model with:
	```
	th train.lua \
		-input_h5 data/formulas.h5 \
		-input_json data/formulas.json \
		-sequence_length 500 \
		-rnn_size 512 \
		-dropout 0.4 \
		-num_layers 3 \
		-max_epochs 200 \
		-lr_decay_factor 0.7
	```
> Problems

 - Due to the compatibility issues, dockerized version of torch-rcnn is used.

> References

> TODO:

 - [ ] References.
 - [ ] Training results/ visualization.
 - [ ] Tool for converting results in text to LaTeX format.
 - [ ] Literature review.
 - [ ] Further process/clean data.
 - [ ] Try out different hyperparameters, techniques and network architecture.

