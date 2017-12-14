# regius
Snakemake, OpenMS, and more

A simple workflow to demonstrate the power of snakemake and openms.

the current code requires python 3.6 and snakemake

Quick Install
```
conda config --add channels conda-forge
conda config --add channels bioconda

conda install snakemake
```

The workflow uses virtual box and docker to run various proteomics tools.

The workflow takes files as either manuracturer raw format or mzML.  A python script is provided to convert the files using a virtualbox VM containing the proteowizrd tool msconvert.

OpenMS tools are available inside a preconfigured docker container along with various thrid-party tools.

The example script performs a consensus analysis of MyriMatch and MSGFPlus search results.

The DAG for the workflow is shown below.

![workflow](docs/images/dag1.png)
