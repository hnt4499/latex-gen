# This contains weekly reports updating progress in the project "LaTex Formulas Generation".

##  Week 1 (Tue 09/Jul/2019)

> Overview

 - The dataset was highly inspired from [harvardnlp](http://nlp.seas.harvard.edu/)'s project of [Image-to-Markup Generation](http://lstm.seas.harvard.edu/latex/) [[paper](http://arxiv.org/pdf/1609.04938v1.pdf)]. The dataset consists of 100k LaTeX formulas (separated by `\n`) in `lts` format encoded by `ISO-8859-15`. The scripts for data pre-processing can be found in this repo: [`prepocess_formulas.py`](https://github.com/hnt4499/latex-gen/blob/master/im2markup/scripts/preprocessing/preprocess_formulas.py).  According to the original repo, this script will 
	> normalize input data and produce some error messages since some formulas cannot be parsed by the KaTeX parser.
	
 - The [Torch](http://torch.ch/) implementation of LSTM-RNN for Text Generation, `torch-rnn`, is used and can be found [here](https://github.com/jcjohnson/torch-rnn). Dockerized version of `torch-rnn` is used due to compatibility issues and can be found [here](https://github.com/crisbal/docker-torch-rnn).
 - All checkpoints as well as training stats and results can be found under the [`data/checkpoints`](https://github.com/hnt4499/latex-gen/tree/master/data/checkpoints) folder.
 - Two different methods of pre-processing data have been used:
    - This first method utilize the pre-processing script from `im2latex` , [`preprocess_formulas.py`](https://github.com/hnt4499/latex-gen/blob/master/im2markup/scripts/preprocessing/preprocess_formulas.py), to filter out non-unicode characters and normalize data. Further processing with [`torch-rnn/scripts/preprocess.py`](https://github.com/jcjohnson/torch-rnn/blob/master/scripts/preprocess.py) has been done to tokenize the input data to json file containing corpus vocabulary and to save the input data in `.h5` format . Finally, the data is fed into the model using default hyperpameters with:
	```
	th train.lua \
		-input_h5 data/formulas_processed.h5 \
		-input_json data/formulas_processed.json
	``` 
	
    - The second method performs data cleaning by only converting the encoder from `ISO-8859-15` to `UTF-8` so that the subsequent scripts can be used. Further processing with  `torch-rnn/scripts/preprocess.py` has been done to tokenize the input data to json file containing corpus vocabulary and to save the input data in `.h5` format. Finally, the data is fed into the model with:
	```
	th train.lua \
		-input_h5 data/formulas.h5 \
		-input_json data/formulas.json \
		-seq_length 500 \
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

## Week 2 (15/Jul/2019)
> Overview

- Many more scripts for data pre-processing/ data visualization have been written, test carefully and added to automate the process of post-processing and data evaluation.
- All post-processing scripts can be found under the folder [`latex_gen/postprocessing`](https://github.com/hnt4499/latex-gen/tree/master/latex_gen/postprocessing) and [`latex-gen/utils`](https://github.com/hnt4499/latex-gen/tree/master/latex_gen/utils). These include:

	- [`sample.py`](https://github.com/hnt4499/latex-gen/blob/master/latex_gen/postprocessing/sample.py):  Samples arbitrary sequences of characters from trained model to a `.txt` file. Total length of sequences, checkpoint, starting sequence to sample from and sample mode can be specified.
	- [`tex_to_img.py`](https://github.com/hnt4499/latex-gen/blob/master/latex_gen/postprocessing/tex_to_img.py) :  Converts the sampled `.txt` file containing raw LaTeX formulas into images for visualization. 
	- [`results_viz.py`](https://github.com/hnt4499/latex-gen/blob/master/latex_gen/postprocessing/results_viz.py): Automatically generates graphs from a `.json` file for training loss, validation loss as well as all hyperparameters specified during training into an image file.

- Results visualization for all trained models:

	- The first model was trained on processed dataset and with the minimal hyperparameters to obtain a baseline. Below graphs are the training results and formulas sampled from trained model. As can be seen, the model can capture quite easily the training corpus, since there are only 95 tokens in the vocab. It is easy to notice that the main problem with this shallow approach is that it cannot capture that logic behind brackets. While doing a good job in some short formulas like `(10)` and `(14)`, most of the brackets are not opened/closed correctly. Having said that, the model is able to generate quite long, complex formulas like `(12)` or `(15)` without introducing many errors, indicating that we can further improve from this model to achieve much better results.
	
| Training results |
|--|
| ![](https://raw.githubusercontent.com/hnt4499/latex_gen/master/data/checkpoints/20190709_0221/training.jpg) |

| Sampled formulas |
|--|
| ![](https://raw.githubusercontent.com/hnt4499/latex_gen/master/data/checkpoints/20190709_0221/sample_batch/20190709_0221_71.png) |



<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIwMDYyOTI5NDcsMTk2MDY1OTM2OF19
-->