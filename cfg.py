import collections

def cmd(od):
    cmd_string = ''
    for key, value in od.items():

        if key == 'exe':
            cmd_string = value
#        elif key == 'in':
#            cmd_string = cmd_string + ' -%s %s' %(key, value)
        elif value == 'false':
            continue
        elif value[0] == '_':  #use _ to omit the value
            cmd_string = cmd_string + ' -%s' %(key)
        elif key[0] == '_':  #use _ to omit the key
            cmd_string = cmd_string + ' %s' %(value)
        else:
            cmd_string = cmd_string + ' -%s %s' %(key, value)
    return cmd_string

FileConverterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FileConverter",
"in": "{DOCKER_DATA}/{input.mzml}",
"out": "{DOCKER_DATA}/{output.mzxml}",
'write_scan_index': "false ",
"debug": "0",
"threads": "1"
})

DecoyDatabaseParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} DecoyDatabase",
"in": "{DOCKER_DATA}/{input.fasta}",
"out": "{DOCKER_DATA}/{output.fasta}",
"decoy_string": "rev_",
"decoy_string_position": "prefix",
"method": "reverse",
"debug": "0",
"threads": "1"
})

XTandemAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} XTandemAdapter",
"in": "{DOCKER_DATA}/{input.mzml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"database": "{DOCKER_DATA}/{input.fasta}",
"xtandem_executable": "/tools/tandem.exe",
"precursor_mass_tolerance": "10.0",
"fragment_mass_tolerance": "0.3",
"precursor_error_units": "ppm",
"fragment_error_units": "Da",
"missed_cleavages": "false",
"enzyme": "Trypsin",
"output_results": "all",
"max_valid_expect": "0.1",
"use_noise_suppression": "false",
"semi_cleavage": "false",
"refinement": "false",
"debug": "0",
"threads": "1"
})

MyriMatchAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} MyriMatchAdapter",
"in": "{DOCKER_DATA}/{input.mzml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"database": "{DOCKER_DATA}/{input.fasta}",
"precursor_mass_tolerance": "10",
"precursor_mass_tolerance_unit": "ppm",
"fragment_mass_tolerance": "0.8",
"fragment_mass_tolerance_unit": "Da",
"myrimatch_executable": "/tools/myrimatch",
"CleavageRules": "Trypsin",
#"MaxMissedCleavages": "2",
'variable_modifications': 'false',
'fixed_modifications': 'false',
"debug": "0",
"threads": "1"
})

MSGFPlusAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} MSGFPlusAdapter",
"in": "{DOCKER_DATA}/{input.mzml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"database": "{DOCKER_DATA}/{input.fasta}",
"precursor_mass_tolerance": "10",
"precursor_error_units": "ppm",
'instrument': 'low_res', #'high_res', 'Q_Exactive',
"executable": "/tools/MSGFPlus.jar",
'enzyme': 'Trypsin/P',
'variable_modifications': 'false',
'fixed_modifications': 'false',
"debug": "0",
"threads": "1"
})

IDPosteriorErrorProbabilityParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} IDPosteriorErrorProbability",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"split_charge": "false",
"top_hits_only": "false",
#"fdr_for_targets_smaller": "0.05",
"ignore_bad_data": "false",
"prob_correct": "false",
"debug": "0",
"threads": "1"
})

ConsensusIDParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} ConsensusID",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"debug": "0",
"threads": "1"
})

PeptideIndexerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} PeptideIndexer",
"in": "{DOCKER_DATA}/{input.idxml}",
"fasta": "{DOCKER_DATA}/{input.fasta}",
"out": "{DOCKER_DATA}/{output.idxml}",
"decoy_string": "rev_",
"decoy_string_position": "prefix",
"missing_decoy_action": "warn",
"write_protein_sequence": "false",
"write_protein_description": "_true",
"keep_unreferenced_proteins": "_true",
"allow_unmatched": "_true",
"full_tolerant_search": "false",
"aaa_max": "4",
"IL_equivalent": "_true",
"filter_aaa_proteins": "false",
"enzyme:name": "Trypsin",
"enzyme:specificity": "none",
"debug": "0",
"threads": "1"
})

FalseDiscoveryRateParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FalseDiscoveryRate",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"protein": "false",
"PSM": " true ",
"FDR:PSM": "1",
"algorithm:no_qvalues": "false",
"algorithm:use_all_hits": "_true",
"algorithm:split_charge_variants": "_true",
"algorithm:treat_runs_separately": "_true",
"algorithm:add_decoy_peptides": "_true",
"debug": "0",
"threads": "1"
})

FalseDiscoveryRateFidoParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FalseDiscoveryRate",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"protein": "true",
"PSM": "false",
"FDR:protein": "0.01",
"debug": "0",
"threads": "1"
})

IDFilterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} IDFilter",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"length": ":",
"charge": ":",
"var_mods": "false",
"unique": "false",
"unique_per_protein": "false",
"keep_unreferenced_protein_hits": "false",
"remove_decoys": "false",
"delete_unreferenced_peptide_hits": "false",
"precursor:rt": ":",
"precursor:mz": ":",
"score:pep": "0.05",
"score:prot": "0.0",
"thresh:pep": "0.0",
"thresh:prot": "0.0",
"whitelist:protein_accessions": "_true",
"whitelist:ignore_modifications": "false",
"whitelist:modifications": "_true",
"blacklist:protein_accessions": "_true",
"blacklist:ignore_modifications": "false",
"blacklist:modifications": "_true",
"rt:p_value": "0.0",
"rt:p_value_1st_dim": "0.0",
"mz:error": "-1.0",
"mz:unit": "ppm",
"best:n_peptide_hits": "0",
"best:n_protein_hits": "0",
"best:strict": "false",
"best:n_to_m_peptide_hits": ":",
"debug": "0",
"threads": "1"
})


MapAlignerIdentificationParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} MapAlignerIdentification",
"in": "_true",
"out": "_true",
"reference:file": "_true",
"model:type": "lowess", #default: 'b_spline' valid: 'linear', 'b_spline', 'lowess'
"debug": "0",
"threads": "1"
})

FeatureFinderIdentificationParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FeatureFinderIdentification",
"in": "{DOCKER_DATA}/{input.mzml}",
"id": "{DOCKER_DATA}/{input.int}",
"id_ext": "{DOCKER_DATA}/{input.ext}",
"out": "{DOCKER_DATA}/{output.featurexml}",
"debug": "0",
"threads": "1"
})

FeatureFinderCentroidedParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FeatureFinderCentroided",
"in": "{DOCKER_DATA}/{input.mzml}",
"out": "{DOCKER_DATA}/{output.featurexml}",
"algorithm:debug": "false",
"algorithm:intensity:bins": "5",
"algorithm:mass_trace:mz_tolerance": "0.05",
"algorithm:mass_trace:min_spectra": "10",
"algorithm:mass_trace:max_missing": "1",
"algorithm:mass_trace:slope_bound": "0.1",
"algorithm:isotopic_pattern:charge_low": "1",
"algorithm:isotopic_pattern:charge_high": "4",
"algorithm:isotopic_pattern:mz_tolerance": "0.05",
"algorithm:isotopic_pattern:intensity_percentage": "10.0",
"algorithm:isotopic_pattern:intensity_percentage_optional": "0.1",
"algorithm:isotopic_pattern:optional_fit_improvement": "2.0",
"algorithm:isotopic_pattern:mass_window_width": "25.0",
"algorithm:isotopic_pattern:abundance_12C": "98.93",
"algorithm:isotopic_pattern:abundance_14N": "99.632",
"algorithm:seed:min_score": "0.8",
"algorithm:fit:max_iterations": "500",
"algorithm:feature:min_score": "0.7",
"algorithm:feature:min_isotope_fit": "0.8",
"algorithm:feature:min_trace_score": "0.5",
"algorithm:feature:min_rt_span": "0.333",
"algorithm:feature:max_rt_span": "2.5",
"algorithm:feature:rt_shape": "symmetric",
"algorithm:feature:max_intersection": "0.35",
"algorithm:feature:reported_mz": "monoisotopic",
"algorithm:user-seed:rt_tolerance": "5.0",
"algorithm:user-seed:mz_tolerance": "1.1",
"algorithm:user-seed:min_score": "0.5",
"algorithm:debug:pseudo_rt_shift": "500.0",
"debug": "0",
"threads": "1"
})

IDMapperParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} IDMapper",
"id": "{DOCKER_DATA}/{input.idxml}",
"in": "{DOCKER_DATA}/{input.featurexml}",
"out": "{DOCKER_DATA}/{output}",
"rt_tolerance": "5.0",
"mz_tolerance": "20.0",
"mz_measure": "ppm",
"mz_reference": "precursor",
"ignore_charge": "false",
"feature:use_centroid_rt": "false",
"feature:use_centroid_mz": "false",
"consensus:use_subelements": "false",
"consensus:annotate_ids_with_subelements": "false",
"debug": "0",
"threads": "1"
})


MapAlignerPoseClusteringParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} MapAlignerPoseClustering",
"in": "_true",
"out": "{DOCKER_DATA}/{input.featurexmls}",
"reference:index": "0",
"algorithm:max_num_peaks_considered": "500",
"algorithm:superimposer:mz_pair_max_distance": "0.05",
"algorithm:superimposer:rt_pair_distance_fraction": "0.1",
"algorithm:superimposer:num_used_points": "2000",
"algorithm:superimposer:scaling_bucket_size": "0.005",
"algorithm:superimposer:shift_bucket_size": "3.0",
"algorithm:superimposer:max_shift": "1000.0",
"algorithm:superimposer:max_scaling": "2.0",
"algorithm:pairfinder:second_nearest_gap": "2.0",
"algorithm:pairfinder:use_identifications": "false",
"algorithm:pairfinder:ignore_charge": "false",
"algorithm:pairfinder:distance_RT:max_difference": "300.0",
"algorithm:pairfinder:distance_RT:exponent": "1.0",
"algorithm:pairfinder:distance_RT:weight": "1.0",
"algorithm:pairfinder:distance_MZ:max_difference": "0.05",
"algorithm:pairfinder:distance_MZ:unit": "Da",
"algorithm:pairfinder:distance_MZ:exponent": "2.0",
"algorithm:pairfinder:distance_MZ:weight": "1.0",
"algorithm:pairfinder:distance_intensity:exponent": "1.0",
"algorithm:pairfinder:distance_intensity:weight": "0.0",
"debug": "0",
"threads": "1"
})

FeatureLinkerUnlabeledQTParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FeatureLinkerUnlabeledQT",
"in": "{DOCKER_DATA}/{input.featurexmls}",
"out": "{DOCKER_DATA}/{output.consensusxml}",
"keep_subelements": "false",
"algorithm:use_identifications": "false",
"algorithm:nr_partitions": "1",
"algorithm:ignore_charge": "false",
"algorithm:distance_RT:max_difference": "100.0",
"algorithm:distance_RT:exponent": "1.0",
"algorithm:distance_RT:weight": "1.0",
"algorithm:distance_MZ:max_difference": "0.05",
"algorithm:distance_MZ:unit": "Da",
"algorithm:distance_MZ:exponent": "2.0",
"algorithm:distance_MZ:weight": "1.0",
"algorithm:distance_intensity:exponent": "1.0",
"algorithm:distance_intensity:weight": "0.0",
"debug": "0",
"threads": "1"
})


FeatureLinkerUnlabeledKDParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FeatureLinkerUnlabeledKD",
"in": "{DOCKER_DATA}/{input.featurexmls}",
"out": "{DOCKER_DATA}/{output.consensusxml}",
"keep_subelements": "false",
# "algorithm:rt_tol": "60",
# "algorithm:mz_tol": "20",
# "algorithm:mz_unit": "ppm",
# "algorithm:wartp": "true",
"debug": "0",
"threads": "1"
})


ConsensusMapNormalizerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} ConsensusMapNormalizer",
"in": "{DOCKER_DATA}/{input.consensusxml}",
"out": "{DOCKER_DATA}/{output.consensusxml}",
"algorithm_type": "median",
"ratio_threshold": "0.67",
"debug": "0",
"threads": "1"
})

IDMergerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} IDMerger",
"in": "{DOCKER_DATA}/{input.idxmls}",
"out": "{DOCKER_DATA}/{output.idxml}",
"annotate_file_origin": "_true",
"pepxml_protxml": "false",
"debug": "0",
"threads": "1"
})

FidoAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} FidoAdapter",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.idxml}",
"fido_executable": "/tools/Fido",
"fidocp_executable": "/tools/FidoChooseParameters",
"all_PSMs": "_true",
"separate_runs": "false",
"keep_zero_group": "false",
"greedy_group_resolution": "_true",
"no_cleanup": "_true",
"group_level": "false",
"log2_states": "0",
"log2_states_precalc": "0",
"no_progress": "false",
"prob:protein": "0.0",
"prob:peptide": "0.0",
"prob:spurious": "0.0",
"debug": "0",
"threads": "1"
})

ProteinQuantifierIntParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA}  {OPENMS_DOCKER_IMAGE} ProteinQuantifier",
"in": "{DOCKER_DATA}/{input.consensusxml}",
"protein_groups": "{DOCKER_DATA}/{input.fido}",
"out": "{DOCKER_DATA}/{output.csv}",
"average": "sum",
"top": "0",
"include_all": "_true",
"filter_charge": "false",
"ratios": "false",
"ratiosSILAC": "false",
"consensus:normalize": "false",
"consensus:fix_peptides": "false",
"format:separator": ",",
"format:quoting": "double",
"format:replacement": "_",
"debug": "0",
"threads": "1"
})

ProteinQuantifierSpecCountsParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} ProteinQuantifier",
"in": "{DOCKER_DATA}/{input.idxml}",
"protein_groups": "{DOCKER_DATA}/{input.fido}",
"out": "{DOCKER_DATA}/{output.csv}",
"average": "sum",
"top": "0",
"include_all": "_true",
"filter_charge": "false",
"ratios": "false",
"ratiosSILAC": "false",
"consensus:normalize": "false",
"consensus:fix_peptides": "false",
"format:separator": ",",
"format:quoting": "double",
"format:replacement": "_",
"debug": "0",
"threads": "1"
})

TextExporterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} TextExporter",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.csv}",
"separator": ",",
"debug": "0",
"threads": "1"
})

MzTabExporterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} {USER_DATA}:{DOCKER_DATA} {OPENMS_DOCKER_IMAGE} MzTabExporter",
"in": "{DOCKER_DATA}/{input.idxml}",
"out": "{DOCKER_DATA}/{output.tsv}",
"debug": "0",
"threads": "1"
})
