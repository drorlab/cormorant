import logging
import os

from cormorant.data.prepare.md17 import download_dataset_md17
from cormorant.data.prepare.qm9 import download_dataset_qm9


def prepare_dataset(datadir, dataset, suffix='', subset=None, splits=None, cleanup=True, force_download=False):
    """
    Download and process dataset.

    Parameters
    ----------
    datadir : str
        Path to the directory where the data and calculations and is, or will be, stored.
    dataset : str
        String specification of the dataset.  If it is not already downloaded, must currently by "qm9" or "md17".
    subset : str, optional
        Which subset of a dataset to use.  Action is dependent on the dataset given.
        Must be specified if the dataset has subsets (i.e. MD17).  Otherwise ignored (i.e. GDB9).
    splits : dict, optional
        Dataset splits to use.
    cleanup : bool, optional
        Clean up files created while preparing the data.
    force_download : bool, optional
        If true, forces a fresh download of the dataset.

    Returns
    -------
    datafiles : dict of strings
        Dictionary of strings pointing to the files containing the data. 

    """

    # If datasets have subsets,
    if subset:
        dataset_dir = [datadir, dataset+suffix, subset]
    else:
        dataset_dir = [datadir, dataset+suffix]
    logging.info('Loading dataset from %s'%dataset_dir)

    # If split dictionary does not exist, default splits to train/valid/test.
    if splits is None: 
        splits = {'train':'train', 'valid':'valid', 'test':'test'}
    
    # Assume one data file for each split
    datafiles = {split: os.path.join(*(dataset_dir + [splits[split] + '.npz'])) for split in splits.keys()}
    print(datafiles)
    # Check datafiles exist
    datafiles_checks = [os.path.exists(datafile) for datafile in datafiles.values()]

    # Check if prepared dataset exists, and if not set flag to download below.
    # Probably should add more consistency checks, such as number of datapoints, etc...
    new_download = False
    if all(datafiles_checks):
        logging.info('Dataset exists and is processed.')
    elif all([not x for x in datafiles_checks]):
        # If checks are failed
        logging.info('Dataset does not exist. Trying to download it.')
        new_download = True
    else:
        raise ValueError(
            'Dataset only partially processed. Try deleting {} and running again to download/process.'.format(os.path.join(dataset_dir)))

    # If need to download dataset, pass to appropriate downloader
    if new_download or force_download:
        logging.info('Dataset does not exist. Downloading!')
        if dataset.lower().startswith('qm9'):
            download_dataset_qm9(datadir, dataset, splits.keys(), cleanup=cleanup)
        elif dataset.lower().startswith('md17'):
            download_dataset_md17(datadir, dataset, subset,
                                  splits.keys(), cleanup=cleanup)
        elif dataset.lower().startswith('pdbbind'):
            raise NotImplementedError(
                'Download of PDBBind currently not implemented!')
        elif dataset.lower().startswith('res'):
            raise NotImplementedError(
                'Download of ResDel currently not implemented!')
        elif dataset.lower().startswith('mutation'):
            raise NotImplementedError(
                'Download of Mutation dataset currently not implemented!')
        elif dataset.lower().startswith('lep'):
            raise NotImplementedError(
                'Download of LEP dataset currently not implemented!')
        elif dataset.lower().startswith('esol'):
            raise NotImplementedError(
                'Download of ESOL dataset currently not implemented!')
        elif dataset.lower().startswith('freesolv'):
            raise NotImplementedError(
                'Download of FreeSolv dataset currently not implemented!')
        elif dataset.lower().startswith('lipophilicity'):
            raise NotImplementedError(
                'Download of Lipophilicity dataset currently not implemented!')
        elif dataset.lower().startswith('aqsoldb'):
            raise NotImplementedError(
                'Download of AqSolDB dataset currently not implemented!')
        elif dataset.lower().startswith('herg'):
            raise NotImplementedError(
                'Download of hERG dataset currently not implemented!')
        elif dataset.lower().startswith('pxr'):
            raise NotImplementedError(
                'Download of PXR dataset currently not implemented!')
        elif dataset.lower().startswith('fassif'):
            raise NotImplementedError(
                'Download of FASSIF dataset currently not implemented!')
        elif dataset.lower().startswith('clint'):
            raise NotImplementedError(
                'Download of CLint datasets currently not implemented!')
        elif dataset.lower().startswith('cyp'):
            raise NotImplementedError(
                'Download of CYP datasets currently not implemented!')
        elif dataset.lower().startswith('fup'):
            raise NotImplementedError(
                'Download of FUP datasets currently not implemented!')
        else:
            raise ValueError(
                'Incorrect choice of dataset! Must chose qm9/md17!')

    return datafiles
