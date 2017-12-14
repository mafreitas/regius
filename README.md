# regius
Snakemake, OpenMS, and more

A simple workflow to demonstrate the power of snakemake and openms.

the current code requires python 3.6 and snakemake

Quick Setup

First install Snakemake:

A) via conda
```
conda config --add channels conda-forge
conda config --add channels bioconda
conda install snakemake

```
(for conda, it is preferred to add the conda-forge and bioconda channels)

or B) via pip:

```
pip install snakemake
```

ProteoWizard

Next Setup the Virtual box VM for file conversion. The workflow uses a windows 7 (also works with windows 10) virtual machine to convert instrument fiels to mzML. A python script is provided to convert the files using a VirtualBox VM containing the ProteoWizard tool msconvert.exe.

1) Download VirtualBox here:
[https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

2) Install Windows 7/10

Download and Install ProteoWizard binaries for Windows.
[http://proteowizard.sourceforge.net/](http://proteowizard.sourceforge.net/)

3) create the directory "c:\work" in the VM.  This folder is where temp files will be copied and converted.  The VM cleans up this folder.  (TODO add cleanup of orphaned files)

Next Create the docker container for OpenMS and thridp-arty tools.

```
cd docker_openms_2.2.0
docker build -t mfreitas/openms:2.2.0
```
NOTE:  if you use a different tag, you will need to change the tagged container name in the Snakefile.

The workflow needs the following directories to run:
```
mkdir work dbsearch results
```

The folder hierarch should now look like this:
```
Snakefile <- workflow description
cfg.py <- configuration options for tools
raw/ <- Location of instrument files
fasta/ <- Location of protein database files
dbsearch/ <- where search idXML files will be created
work/ <- where all tmp files will be created
results/ <- were final results will be created
vbox_msconvert/ <- location of msconvert VM scripts
docker_openms_2.2.0/ <- Location of Dockerfile for OpenMS container
```

The example workflow performs consensus analysis of MyriMatch and MSGF+ database search.

The DAG representation of the example workflow is shown below.

![workflow](docs/images/dag1.png)

to perform a dryrun issue the following command.

```
snakemake -n
```

To run the workflow:
```
snakemake
```

By using snakemake with vm based tool delivery a workflow can be reproduced on any system capable of running VirtualBox, Docker and Python 3.6.
