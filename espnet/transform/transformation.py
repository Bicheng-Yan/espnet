from collections import OrderedDict
<<<<<<< HEAD
import copy
import io
import logging
import sys

import yaml

from espnet.utils.check_kwargs import check_kwargs
from espnet.utils.dynamic_import import dynamic_import

=======
import contextlib
import copy
import importlib
import io
import json
import logging
import sys
import threading
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986

PY2 = sys.version_info[0] == 2

if PY2:
    from collections import Sequence
<<<<<<< HEAD
    from funcsigs import signature
else:
    # The ABCs from 'collections' will stop working in 3.8
    from collections.abc import Sequence
    from inspect import signature


# TODO(karita): inherit TransformInterface
# TODO(karita): register cmd arguments in asr_train.py
import_alias = dict(
    identity='espnet.transform.transform_interface:Identity',
    time_warp='espnet.transform.spec_augment:TimeWarp',
    time_mask='espnet.transform.spec_augment:TimeMask',
    freq_mask='espnet.transform.spec_augment:FreqMask',
    spec_augment='espnet.transform.spec_augment:SpecAugment',
    speed_perturbation='espnet.transform.perturb:SpeedPerturbation',
    volume_perturbation='espnet.transform.perturb:VolumePerturbation',
    noise_injection='espnet.transform.perturb:NoiseInjection',
    bandpass_perturbation='espnet.transform.perturb:BandpassPerturbation',
    rir_convolve='espnet.transform.perturb:RIRConvolve',
    delta='espnet.transform.add_deltas:AddDeltas',
    cmvn='espnet.transform.cmvn:CMVN',
    utterance_cmvn='espnet.transform.cmvn:UtteranceCMVN',
    fbank='espnet.transform.spectrogram:LogMelSpectrogram',
    spectrogram='espnet.transform.spectrogram:Spectrogram',
    stft='espnet.transform.spectrogram:Stft',
    istft='espnet.transform.spectrogram:IStft',
    stft2fbank='espnet.transform.spectrogram:Stft2LogMelSpectrogram',
    wpe='espnet.transform.wpe:WPE',
    channel_selector='espnet.transform.channel_selector:ChannelSelector')
=======
else:
    # The ABCs from 'collections' will stop working in 3.8
    from collections.abc import Sequence


def dynamic_import(import_path):
    alias = dict(
        delta='espnet.transform.add_deltas:AddDeltas',
        cmvn='espnet.transform.cmvn:CMVN',
        utterance_cmvn='espnet.transform.cmvn:UtteranceCMVN',
        fbank='espnet.transform.spectrogram:LogMelSpectrogram',
        spectrogram='espnet.transform.spectrogram:Spectrogram',
        stft='espnet.transform.spectrogram:Stft',
        wpe='espnet.transform.wpe:WPE',
        channel_selector='espnet.transform.channel_selector:ChannelSelector')

    if import_path not in alias and ':' not in import_path:
        raise ValueError(
            'import_path should be one of {} or '
            'include ":", e.g. "espnet.transform.add_deltas:AddDeltas" : '
            '{}'.format(set(alias), import_path))
    if ':' not in import_path:
        import_path = alias[import_path]

    module_name, objname = import_path.split(':')
    m = importlib.import_module(module_name)
    return getattr(m, objname)


class TransformConfig(object):
    def __init__(self, config=None, thread_local=True):
        self.thread_local = thread_local
        if config is not None:
            if not isinstance(config, TransformConfig):
                raise TypeError('Must be {}, but got {}'
                                .format(self.__class__.__name__, type(config)))
            self.parent = config
        else:
            self.parent = {}

        if thread_local:
            self.status = threading.local()
        else:
            self.status = {}

    def reset(self):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status
        for k in list(d):
            del d[k]

    def __repr__(self):
        rep = '\n'.join('{}={}'.format(k, v) for k, v in self.items())
        return self.__class__.__name__ + ':\n' + rep

    def __contains__(self, key):
        return key in set(self)

    def __setitem__(self, key, value):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status
        d[key] = value

    def __getitem__(self, key):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status

        if key in d:
            return d[key]
        elif key in self.parent:
            return self.parent[key]
        else:
            raise KeyError('{} is not found in transform_config:\n{}'
                           .format(key, self))

    def __delitem__(self, key):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status

        del d[key]

    def __iter__(self):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status
        return iter(sorted(set(self.parent) | set(d)))

    def keys(self):
        return iter(self)

    def values(self):
        for k in self:
            yield self[k]

    def items(self):
        for k in self:
            yield k, self[k]

    def update(self, v=None, **kwargs):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status

        if v is not None:
            d.update(v, **kwargs)
        else:
            d.update(**kwargs)

    def get(self, key, default=None):
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status

        return d.get(key, self.parent.get(key, default))

    def setdefault(self, key, default=None):
        if key in self.parent:
            return self.parent[key]
        if self.thread_local:
            d = self.status.__dict__
        else:
            d = self.status

        return d.setdefault(key, default)


global_transform_config = TransformConfig(thread_local=False)
# FIXME(kamo): train should be False or not?
global_transform_config.update(train=True)
transform_config = TransformConfig(global_transform_config,
                                   thread_local=True)


@contextlib.contextmanager
def using_transform_config(d, config=transform_config):
    assert isinstance(d, dict), type(d)
    assert isinstance(config, TransformConfig), type(config)

    old = {}
    for key, value in d.items():
        if key in config:
            old[key] = config[key]
        config[key] = value
    try:
        yield config
    finally:
        for key in d:
            if key in old:
                config[key] = old[key]
            else:
                del config[key]
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986


class Transformation(object):
    """Apply some functions to the mini-batch

    Examples:
        >>> kwargs = {"process": [{"type": "fbank",
        ...                        "n_mels": 80,
        ...                        "fs": 16000},
        ...                       {"type": "cmvn",
        ...                        "stats": "data/train/cmvn.ark",
        ...                        "norm_vars": True},
<<<<<<< HEAD
        ...                       {"type": "delta", "window": 2, "order": 2}]}
        >>> transform = Transformation(kwargs)
=======
        ...                       {"type": "delta", "window": 2, "order": 2}],
        ...           "mode": "sequential"}
        >>> transform = Transformation(**kwargs)
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986
        >>> bs = 10
        >>> xs = [np.random.randn(100, 80).astype(np.float32)
        ...       for _ in range(bs)]
        >>> xs = transform(xs)
    """

<<<<<<< HEAD
    def __init__(self, conffile=None):
        if conffile is not None:
            if isinstance(conffile, dict):
                self.conf = copy.deepcopy(conffile)
            else:
                with io.open(conffile, encoding='utf-8') as f:
                    self.conf = yaml.safe_load(f)
                    assert isinstance(self.conf, dict), type(self.conf)
        else:
            self.conf = {'mode': 'sequential', 'process': []}
=======
    def __init__(self, conf=None, **kwargs):
        if conf is not None:
            with io.open(conf, encoding='utf-8') as f:
                conf = json.load(f)
                assert isinstance(conf, dict), type(conf)
            conf.update(kwargs)
            kwargs = conf

        if len(kwargs) == 0:
            self.conf = {'mode': 'sequential', 'process': []}
        else:
            # Deep-copy to avoid sharing of mutable objects
            self.conf = copy.deepcopy(kwargs)
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986

        self.functions = OrderedDict()
        if self.conf.get('mode', 'sequential') == 'sequential':
            for idx, process in enumerate(self.conf['process']):
                assert isinstance(process, dict), type(process)
                opts = dict(process)
                process_type = opts.pop('type')
<<<<<<< HEAD
                class_obj = dynamic_import(process_type, import_alias)
                # TODO(karita): assert issubclass(class_obj, TransformInterface)
                check_kwargs(class_obj, opts)
                try:
                    self.functions[idx] = class_obj(**opts)
                except TypeError:
                    try:
                        signa = signature(class_obj)
                    except ValueError:
                        # Some function, e.g. built-in function, are failed
                        pass
                    else:
                        logging.error('Expected signature: {}({})'
                                      .format(class_obj.__name__, signa))
                    raise
=======
                class_obj = dynamic_import(process_type)
                self.functions[idx] = class_obj(**opts)
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986
        else:
            raise NotImplementedError(
                'Not supporting mode={}'.format(self.conf['mode']))

    def __repr__(self):
        rep = '\n' + '\n'.join(
            '    {}: {}'.format(k, v) for k, v in self.functions.items())
        return '{}({})'.format(self.__class__.__name__, rep)

<<<<<<< HEAD
    def __call__(self, xs, uttid_list=None, **kwargs):
=======
    def __call__(self, xs, uttid_list=None):
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986
        """Return new mini-batch

        :param Union[Sequence[np.ndarray], np.ndarray] xs:
        :param Union[Sequence[str], str] uttid_list:
        :return: batch:
        :rtype: List[np.ndarray]
        """
        if not isinstance(xs, Sequence):
            is_batch = False
            xs = [xs]
        else:
            is_batch = True
<<<<<<< HEAD

=======
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986
        if isinstance(uttid_list, str):
            uttid_list = [uttid_list for _ in range(len(xs))]

        if self.conf.get('mode', 'sequential') == 'sequential':
            for idx in range(len(self.conf['process'])):
                func = self.functions[idx]
<<<<<<< HEAD
                # TODO(karita): use TrainingTrans and UttTrans to check __call__ args
                # Derive only the args which the func has
                try:
                    param = signature(func).parameters
                except ValueError:
                    # Some function, e.g. built-in function, are failed
                    param = {}
                _kwargs = {k: v for k, v in kwargs.items()
                           if k in param}
                try:
                    if uttid_list is not None and 'uttid' in param:
                        xs = [func(x, u, **_kwargs)
                              for x, u in zip(xs, uttid_list)]
                    else:
                        xs = [func(x, **_kwargs) for x in xs]
=======
                try:
                    if uttid_list is not None and \
                            hasattr(func, 'accept_uttid') and \
                            getattr(func, 'accept_uttid') is True:
                        xs = [func(x, u) for x, u in zip(xs, uttid_list)]
                    else:
                        xs = [func(x) for x in xs]
>>>>>>> 3c086dddcae725e6068d5dffc26e5962617cf986
                except Exception:
                    logging.fatal('Catch a exception from {}th func: {}'
                                  .format(idx, func))
                    raise
        else:
            raise NotImplementedError(
                'Not supporting mode={}'.format(self.conf['mode']))

        if is_batch:
            return xs
        else:
            return xs[0]
