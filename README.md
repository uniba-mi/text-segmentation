<p align="center">
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="license">
    <br>
</p>
    
<h2 align="center">Contrasting Traditional Models and LLMs:

An Evaluation Based on Text Segmentation</h2>

<p align="center">
    <a href="#summary">Summary</a>
    •
    <a href="#installation-and-prerequisites">Installation and Prerequisites</a>
    •
    <a href="#data">Data</a>
    •
    <a href="#usage">Usage</a>
    •
    <a href="#citation">Citation</a>
    •
    <a href="#license">License</a>
</p>

## Summary

This repository contains the code produced for applying the text segmentation approaches presented in the paper "Contrasting Traditional Models and LLMs: An Evaluation Based on Text Segmentation" at the NLP4Sustain Workshop at KONVENS 2025 in Hildesheim, Germany.

## Installation and Prerequisites

Thanks to Docker, only [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) are required for using the the scripts.

## Data
Our dataset is unfortunately not publicly available.
However, other data can be easily tested, provided that the data is formatted as JSON in the following schema: ` {"id":"text","id":"text","id":"text"}`
Save your file as *video_segments_checked.json* in the [data](./data) folder.
## Usage 

After cloning or downloading this repository, simply run `docker compose up text-segmentation` in a command line from the root folder of the repository to prepare the libraries.

Afterwards run `docker compose run text-segmentation` to open the bash, through which the different scripts and parameter configurations can be applied.


### Extract Segments
Four variants are implemented here, three using the TextTiling approach from Hearst (see [https://aclanthology.org/J97-1003/](https://aclanthology.org/J97-1003/)) and one by applying GPT-4o (see [https://openai.com/index/hello-gpt-4o/](https://openai.com/index/hello-gpt-4o/))

#### For TextTiling:
- Parameter configurations are available for two parameters, as used in the original publication from Hearst, see [https://aclanthology.org/J97-1003/](https://aclanthology.org/J97-1003/):
    - *w*: The size of pseudosentences or token-sequence size
    - *k*: The block size used in the comparison mechanism
- Three different parameter sets are included in as configured:
    - `python segment-extractor.py texttiling_default` processes the input text using the default parameter of w=20 and k=10, from the original Hearst publication, see p. 54 in [https://aclanthology.org/J97-1003/](https://aclanthology.org/J97-1003/)
    - `python segment-extractor.py texttiling_basic` processes the input text using the parameters of w=[20,30] and k=[5,10]
    - `python segment-extractor.py texttiling_all` processes the input text using the parameters of w=[1,2,3,5,8,10,15,20,30,40,50] and k=[1,2,3,5,8,10,15,20,30,40,50]

#### For GPT-4o
- To use GPT-4o add your OpenAI-API-key in file [segment-extractor.py](./segment-extractor.py) in line 22
- Afterwards simply run `python segment-extractor.py gpt`

### Analyze Results
Simply call `python result-analzyer.py`, provided that the output files from the extraction scripts produced a JSON file, that is available in the [data](./data) folder.


## Citation
If you use this software, please cite it as below: 

*Will be added after the proceedings have been published.*

## License

See [License](./LICENSE/)
