import torch
from torch.utils.data import DataLoader

import logging

from cormorant.cg_lib import rotations as rot
from cormorant.data import collate_fn


def _gen_rot(data, angles, maxl):
	alpha, beta, gamma = angles
	D = rot.WignerD_list(maxl, alpha, beta, gamma)
	R = rot.EulerRot(alpha, beta, gamma)

	return D, R

def covariance_test(model, data):
	logging.info('Beginning covariance test!')
	targets_rotout, outputs_rotin = [], []

	angles = torch.rand(3)
	D, R = _gen_rot(data, angles, max(model.maxl))

	data_rotout = data

	data_rotin = {key: val.clone() if type(val) is torch.Tensor else None for key, val in data.items()}
	data_rotin['positions'] = rot.rotate_cart_vec(R, data_rotin['positions'])

	outputs_rotout, reps_rotout, _ = model(data_rotout, covariance_test=True)
	outputs_rotin, reps_rotin, _ = model(data_rotin, covariance_test=True)

	reps_rotout, reps_rotin = reps_rotout[0], reps_rotin[0]

	invariance_test = (outputs_rotout - outputs_rotin).norm()

	reps_rotout = [rot.rotate_rep(D, reps) for reps in reps_rotout]
	covariance_test_norm = [[(part_in - part_out).norm().item() for (part_in, part_out) in zip(level_in, level_out)] for (level_in, level_out) in zip(reps_rotin, reps_rotout)]
	covariance_test_mean = [[(part_in - part_out).abs().mean().item() for (part_in, part_out) in zip(level_in, level_out)] for (level_in, level_out) in zip(reps_rotin, reps_rotout)]


	if set([len(part) for part in reps_rotout]) == 1:
		covariance_test_norm = torch.tensor(covariance_test_norm)
		covariance_test_mean = torch.tensor(covariance_test_mean)
	else:
		covariance_test_norm = [torch.tensor(p) for p in covariance_test_norm]
		covariance_test_mean = [torch.tensor(p) for p in covariance_test_mean]


	logging.info('Rotation Invariance test:', invariance_test)
	logging.info('Rotation Covariance test (norm):', covariance_test_norm)
	logging.info('Rotation Covariance test (mean):', covariance_test_mean)


def permutation_test(model, data):
	logging.info('Beginning permutation test!')

	mask = data['charges'] > 0
	perm = 1*torch.arange(mask.shape[1]).expand(mask.shape[0], -1)
	for idx in range(len(mask)):
		num_atoms = mask[idx, :].sum()
		perm[idx, :num_atoms] = torch.randperm(num_atoms)
	apply_perm = lambda mat: torch.stack([mat[idx, p] for (idx, p) in enumerate(perm)])

	assert((mask == apply_perm(mask)).all())

	data_noperm = data
	data_perm = {key: apply_perm(val) if type(val) is torch.Tensor else None for key, val in data.items()}

	outputs_perm = model(data_perm, covariance_test=False)
	outputs_noperm = model(data_noperm, covariance_test=False)

	invariance_test = (outputs_perm - outputs_noperm).norm()

	logging.info('Permutation Invariance test:', invariance_test)


def cormorant_tests(model, dataloader, args, tests=['covariance'], charge_scale=1):
	if args.skip_test:
		logging.info("WARNING: network tests disabled!")
		return

	logging.info("Testing network for symmetries:")
	model.eval()

	charge_power, num_species = model.charge_power, model.num_species

	data = next(iter(dataloader))

	covariance_test(model, data)
	# permutation_test(model, data)

	logging.info('Test complete!')
