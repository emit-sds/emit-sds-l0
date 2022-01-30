# emit-sds-l0

## Description

Welcome to the emit-sds-l1a repository.  This repository contains scripts for executing the various EMIT L0 PGEs.  These PGEs include the following functions:
* Stripping HOSC headers from input HOSC files and outputting CCSDS files
* Getting the start and stop times of CCSDS files

To understand how this repository is linked to the rest of the emit-sds repositories, please see the [repository guide](https://github.com/emit-sds/emit-main/wiki/Repository-Guide).

## Installation Instructions

Clone the repository:
```
git clone https://github.jpl.nasa.gov/emit-sds/emit-sds-l0.git
```
Run pip install:
```
cd emit-sds-l0
pip install -e .
```
Clone the L0 EDP repository:
```
git clone https://github.jpl.nasa.gov/emit/emit-l0edp.git
```
Build cargo
```
cd emit-l0edp
cargo build --release
```

## Dependency Requirements

This repository is based on Python 3.x.  See `emit-sds-l0/setup.py` for specific dependencies.

## Example Execution Commands

### Stripping HOSC Headers

```
./run_l0.sh <in_dir> <out_dir> <report_log> <ccsds_check_script> <l0_proc_exe>
```
Where:
* in_dir: The input directory
* out_dir: The output directory
* report_log: The path to an output report log file
* ccsds_check_script: The path to the packet count check script (typically just `packet_cnt_check.py`)
* l0_proc_exe: The path to the L0 processing executable (tyically `emit-l0edp/target/release/emit_l0_proc`)

### Getting CCSDS Start and Stop Times

```
python get_ccsds_start_stop_times.py <input_ccsds_path> <output_json_path>
```
