import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from claim5_a3_conformance import run
def test_ranks_and_finite():
 r=run(7)
 assert r['qk_rank'] <= r['rank'] and r['ov_rank'] <= r['rank']
 assert all(float(r[k]) >=0 for k in ['qk_activation_aware_error','qk_raw_svd_error','ov_activation_aware_error','ov_raw_svd_error','mlp_cur_keep_error','mlp_low_energy_control_error'])
def test_controls_degrade_on_fixed_fixture():
 r=run(11)
 assert r['qk_activation_aware_error'] < r['qk_raw_svd_error']
 assert r['ov_activation_aware_error'] < r['ov_raw_svd_error']
 assert r['mlp_cur_keep_error'] < r['mlp_low_energy_control_error']
