========
Overview
========

This is the Cormorant software package for learning on atomic environments, adapted for the needs of the Dror Lab at Stanford University.
We added models for additional types of datasets as well as the necessary features, in particular the possibilities to perform classification tasks, to use a Siamese network architecture, and to put a boundary on the Clebsch-Gordan product (the central operation of this network architecture).


Documentation
=============

To install the documentation, go to the docs folder and run "make html".  You will need to install the sphinx_rtd_theme (this can be done using pip install).

Getting started
===============

Installation
------------

Cormorant can be cloned directly from the git repo using::

    git clone https://github.com/drorlab/cormorant.git

You can currently install it from
source by going to the directory with setup.py and running::

    python setup.py

If you would like to modify the source code directly, note that Cormorant
can also be installed in "development mode" using the command::

    python setup.py develop


Training example
----------------

The example training script is in :examples/train_cormorant.py:. The same script
can train both the datasets QM9 and MD17, and can also be extended to more general datasets.
::

    python examples/train_qm9.py

::

    python examples/train_md17.py

Note that if no GPU is available, the the training script will throw an error.
To force CPU-based training, add the : --cpu: flag

Examples for other models/datasets will be published soon at a dedicated repository.

================
Architecture
================

A more detailed description of the Cormorant architecture is available in `the Cormorant paper <https://arxiv.org/abs/1906.04015>`_.

The version here was extended to work not only on regression but also on classification tasks and with a Siamese network architecture.

