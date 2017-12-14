import os.path
import collections
from cfg import *
import glob
import sys

#VMODS = ['"Carbamidomethyl (C)"', '"Oxidation (M)"']
VMODS = ['false']
FMODS = ['false']

USER_DATA = os.getcwd()

DOCKER_DATA = "/data"
DOCKER_CMD = "docker run --rm -it -v"

OPENMS_DOCKER_IMAGE = "mfreitas/openms:2.3.3"
MM_DOCKER_IMAGE = "mfreitas/mm:0.5"

#Parse ms files in /raw folder
RAWFILES = glob.glob("raw/*")
SAMPLES = []
allowed_exts = [".raw",".RAW",".mzml",".mzML","MZML"]
for rawfile in RAWFILES:
    rbase = os.path.basename(rawfile)
    rbase,rext = os.path.splitext(rbase)
    if rext in allowed_exts:
        if rbase not in SAMPLES:
            SAMPLES.append(rbase)

#parse fasta files in /fasta folder
DBFILES = glob.glob("fasta/*")
DATABASES = []
allowed_exts = [".fasta",".FASTA"]
for dbfile in DBFILES:
    dbase = os.path.basename(dbfile)
    dbase,dext = os.path.splitext(dbase)
    if dext in allowed_exts:
        DATABASES.append(dbase)

vmods =  ' '.join(VMODS)
fmods =  ' '.join(FMODS)

#set targets
rule targets:
    input:
        expand("work/{sample}_myr_pep.tsv", sample=SAMPLES),
        expand("work/{sample}_msgf_pep.tsv", sample=SAMPLES),
        expand('work/{sample}_idx.tsv', sample=SAMPLES),
        "results/proteins.csv",
        "results/alldata.csv"

################################################################
# Combine Databases and add reverse decoys
################################################################

rule DecoyDatabaseRule:
    input:
        fasta = expand('fasta/{database}.fasta', database=DATABASES)
    output:
        fasta = 'work/combined_database_rev.fasta'
    threads: 90
    run:
        DecoyDatabaseParams['in'] = " ".join([DOCKER_DATA+"/" + s for s in input.fasta])
        cmd_str = cmd(DecoyDatabaseParams)
        print(cmd_str)
        shell(cmd_str)


################################################################
# Run virtual Windows Machine to convert files to mzML and mzXML
################################################################
rule VBConvertmzML:
    input:
        raw = expand('raw/{sample}.raw',sample=SAMPLES)
    output:
        mzml = expand('raw/{sample}.mzML',sample=SAMPLES)
    threads: 1
    priority: 80
    shell:
         "python vbox_msconvert/vbox_msconvert_mzml.py {input.raw}"

rule VBConvertmzXML:
    input:
        raw = expand('raw/{sample}.raw',sample=SAMPLES)
    output:
        mzxml = expand('raw/{sample}.mzXML',sample=SAMPLES)
    threads: 1
    priority: 80
    shell:
         "python vbox_msconvert/vbox_msconvert_mzxml.py {input.raw}"

################################################################
# Myrimatch Search
################################################################

rule MyriMatchAdapterRule:
    input:
        mzml = "raw/{datafile}.mzML",
        fasta = ancient('work/combined_database_rev.fasta')
    output:
        idxml = "dbsearch/{datafile}_myr.idXML"
    threads: 70
    run:
        MyriMatchAdapterParams['variable_modifications'] = vmods
        cmd_str = cmd(MyriMatchAdapterParams)
        print(cmd_str)
        shell(cmd_str)

rule IDPosteriorErrorProbabilityMyr:
    input:
        idxml = "dbsearch/{datafile}_myr.idXML"
    output:
        idxml = "work/{datafile}_myr_pep.idXML"
    threads: 1
    priority: 71
    run:
        cmd_str = cmd(IDPosteriorErrorProbabilityParams)
        print(cmd_str)
        shell(cmd_str)

rule MzTabExporterMyr:
    input:
        idxml = "work/{datafile}_myr_pep.idXML"
    output:
        tsv = "work/{datafile}_myr_pep.tsv"
    threads: 1
    priority: 72
    run:
        cmd_str = cmd(MzTabExporterParams)
        print(cmd_str)
        shell(cmd_str)

################################################################
# MSFG+ Search
################################################################

rule MSGFPlusAdapter:
    input:
        mzml = "raw/{datafile}.mzML",
        fasta = ancient('work/combined_database_rev.fasta')
    output:
        idxml = "dbsearch/{datafile}_msgf.idXML"
    threads: 1
    priority: 70
    run:
        MSGFPlusAdapterParams['variable_modifications'] = vmods
        cmd_str = cmd(MSGFPlusAdapterParams)
        print(cmd_str)
        shell(cmd_str)

rule IDPosteriorErrorProbabilityMsgf:
    input:
        idxml = "dbsearch/{datafile}_msgf.idXML"
    output:
        idxml = "work/{datafile}_msgf_pep.idXML"
    threads: 1
    priority: 71
    run:
        cmd_str = cmd(IDPosteriorErrorProbabilityParams)
        print(cmd_str)
        shell(cmd_str)


rule MzTabExporterMsgf:
    input:
        idxml = "work/{datafile}_msgf_pep.idXML"
    output:
        tsv = "work/{datafile}_msgf_pep.tsv"
    threads: 1
    priority: 72
    run:
        cmd_str = cmd(MzTabExporterParams)
        print(cmd_str)
        shell(cmd_str)


################################################################
# Consensus PSM Analysis
################################################################

rule IDMergeConsensusPep:
    input:
        idxmls = ["work/{datafile}_myr_pep.idXML", "work/{datafile}_msgf_pep.idXML"]
    output:
        idxml = "work/{datafile}_combined_id_pep.idXML",
    threads: 1
    priority: 60
    run:
        IDMergerParams['in'] = " ".join([DOCKER_DATA+"/" + s for s in input.idxmls])
        IDMergerParams['out'] = DOCKER_DATA+"/"+ output.idxml

        cmd_str = cmd(IDMergerParams)
        print(cmd_str)
        shell(cmd_str)

rule ConsensusID:
    input:
        idxml = "work/{datafile}_combined_id_pep.idXML"
    output:
        idxml = "work/{datafile}_consensus.idXML"
    threads: 1
    priority: 61
    run:
        #ConsensusIDParams['algorithm']='best'
        #ConsensusIDParams['algorithm']='ranks'
        cmd_str = cmd(ConsensusIDParams)
        print(cmd_str)
        shell(cmd_str)

rule PeptideIndexer:
    input:
        idxml = "work/{datafile}_consensus.idXML",
        fasta = ancient('work/combined_database_rev.fasta')
    output:
        idxml = "work/{datafile}_idx.idXML"
    threads: 1
    priority: 63
    run:
        cmd_str = cmd(PeptideIndexerParams)
        print(cmd_str)
        shell(cmd_str)

rule MzTabExporter:
    input:
        idxml = "work/{datafile}_idx.idXML"
    output:
        tsv = "work/{datafile}_idx.tsv"
    threads: 1
    priority: 64
    run:
        cmd_str = cmd(MzTabExporterParams)
        print(cmd_str)
        shell(cmd_str)

        shell(cmd_str)

############################################################
# FIDO Protein Inference from consensus results
############################################################

rule IDMergeFido:
    input:
        idxmls = expand("work/{sample}_idx.idXML", sample=SAMPLES)
    output:
        idxml = "work/idmerge_fido.idXML"
    threads: 1
    priority: 50
    run:
        IDMergerParams['in'] = " ".join([DOCKER_DATA+"/" + s for s in input.idxmls])
        IDMergerParams['out'] = DOCKER_DATA+"/"+ output.idxml

        cmd_str = cmd(IDMergerParams)
        print(cmd_str)
        shell(cmd_str)

rule FidoAdapter:
    input:
        idxml = "work/idmerge_fido.idXML"
    output:
        idxml = "work/fido.idXML"
    threads: 1
    priority: 51
    run:
        cmd_str = cmd(FidoAdapterParams)
        print(cmd_str)
        shell(cmd_str)

rule TextExporterProt:
    input:
        idxml = "work/fido.idXML"
    output:
        csv = "results/proteins.csv"
    threads: 1
    priority: 53
    run:
        TextExporterParams["id:proteins_only"] = "_true"
        cmd_str = cmd(TextExporterParams)
        print(cmd_str)
        shell(cmd_str)

rule TextExporter:
    input:
        idxml = "work/fido.idXML"
    output:
        csv = "results/alldata.csv"
    threads: 1
    priority: 53
    run:
        TextExporterParams["id:proteins_only"] = "false"
        cmd_str = cmd(TextExporterParams)
        print(cmd_str)
        shell(cmd_str)

#FDR not working on Fido results

#rule FalseDiscoveryRateFido:
#    input:
#        idxml = "work/fido.idXML"
#    output:
#        idxml = "work/fido-fdr.idXML"
#    threads: 1
#    priority: 52
#    run:
#        FalseDiscoveryRateFidoParams["FDR:protein"] = "0.01"
#        cmd_str = cmd(FalseDiscoveryRateFidoParams)
#        print(cmd_str)
#        shell(cmd_str)
#
#rule TextExporterProt:
#    input:
#        idxml = "work/fido-fdr.idXML"
#    output:
#        csv = "work/proteins.csv"
#    threads: 1
#    priority: 53
#    run:
#        TextExporterParams["id:proteins_only"] = "_true"
#        cmd_str = cmd(TextExporterParams)
#        print(cmd_str)
#        shell(cmd_str)
