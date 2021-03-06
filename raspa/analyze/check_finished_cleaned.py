"""
Read RASPA simulations
"""
import os
import sys
import glob
import yaml
from raspa_output import parse_output

run_dir = sys.argv[1]
results_file = '%s_results.yaml' % os.path.basename(os.path.abspath(run_dir))
finished, warnings, not_started = 0, 0, 0
all_results = []
n_mofs = len(os.listdir(run_dir))
for i, mof in enumerate(os.listdir(run_dir)):
    print('\rReading results... %3i / %3i' % (i + 1, n_mofs), end='')
    mof_dir = os.path.join(run_dir, mof)
    # ads_path = glob.glob(os.path.join(mof_dir, 'Output', 'System_0', '*.data'))
    ads_path = os.path.join(mof_dir, 'raspa_out.data')
    if os.path.exists(ads_path):
        results = parse_output(ads_path, verbose=False, save=False, framework=mof)
        all_results.append(results)
        if results['finished'] == True:
            finished += 1
        if len(results['warnings']) > 0:
            warnings += 1
    else:
        not_started += 1
print('\n----------------------------------------')
print('%i / %i finished' % (finished, n_mofs))
print('%i / %i warnings' % (warnings, n_mofs))
print('%i / %i not_started' % (not_started, n_mofs))

with open(results_file, 'w') as resfile:
    yaml.dump(all_results, resfile)
print('Results saved -> %s' % (results_file))
