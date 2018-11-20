# Pyomeca tutorials

This repository contains some tutorials on the [pyomeca](https://github.com/pyomeca/pyomeca) python library and some tips to make effective computations in Biomechanics.

<img src="https://github.com/pyomeca/design/blob/master/logo/logo_plain.svg" width="70%" height="70%">

## How to Use this repo
- By running the code using the Jupyter notebooks available in this repository's notebooks directory.
- By launching executable versions of these notebooks using binder: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/pyomeca/tutorials/master?filepath=notebooks%2FIndex.ipynb)
- By launching executable versions of these notebooks using Google Colab: [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pyomeca/tutorials/blob/master/notebooks/Index.ipynb)
- By reading the online (non-executable) version of the notebooks using nbviewer: [![Nbviewer](https://raw.github.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg?sanitize=true)](https://nbviewer.jupyter.org/github/pyomeca/tutorials/blob/master/notebooks/Index.ipynb)

## About
See [Index.ipynb](https://nbviewer.jupyter.org/github/pyomeca/tutorials/blob/master/notebooks/Index.ipynb) for an index of the notebooks available to accompany the text.

## Software
The packages we used to run the code in these tutorials are listed in [environment.yml](environment.yml).

To create a stand-alone environment named `tutorials` with Python 3 and all the required package versions, run the following:

```bash
$ conda env create -n tutorials -f environment.yml
```

You can read more about using conda environments in the [Managing Environments](http://conda.pydata.org/docs/using/envs.html) section of the conda documentation.

---
Project based on the romainmartinez's [cookiecutter jupyter notebooks template](https://github.com/romainmartinez/cookiecutter-jupyter-notebooks).
