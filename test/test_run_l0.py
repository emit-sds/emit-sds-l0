"""
Unit test for checking the run_l0.sh script

Author: Winston Olson-Duvall, winston.olson-duvall@jpl.nasa.gov
"""

import os
import subprocess


def test_run_l0():

    print("Running test_run_l0")

    test_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(test_dir, "data")
    repo_dir = os.path.dirname(test_dir)
    run_l0_exe = os.path.join(repo_dir, "run_l0.sh")
    in_dir = os.path.join(test_dir, "data")
    out_dir = os.path.join(test_dir, "output")
    report_log = os.path.join(out_dir, "l0_pge.log")
    ccsds_check_script = os.path.join(repo_dir, "packet_cnt_check.py")
    repos_base_dir = os.path.dirname(repo_dir)
    l0_proc_exe = os.path.join(repos_base_dir, "emit-l0edp", "target", "release", "emit_l0_proc")

    cmd = [run_l0_exe, in_dir, out_dir, report_log, ccsds_check_script, l0_proc_exe]

    output = subprocess.run(" ".join(cmd), shell=True, capture_output=True, env=os.environ.copy())
    if output.returncode != 0:
        print(output.stderr.decode("utf-8"))
    if output.returncode == 0:
        os.system(f"rm -rf {out_dir}")
    assert output.returncode == 0
