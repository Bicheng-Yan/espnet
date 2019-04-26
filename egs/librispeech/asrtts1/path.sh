MAIN_ROOT=/mnt/matylda6/baskar/espnet_cyc
KALDI_ROOT=$MAIN_ROOT/tools/kaldi
SPNET_ROOT=$MAIN_ROOT/espnet
BUT_CONDA=/homes/kazi/baskar/anaconda3/
CUDAROOT=/usr/local/share/cuda-9.0.176
export CUDA_HOME=$CUDAROOT
export CUDA_PATH=$CUDAROOT

[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/sctk/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C

export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/sph2pipe_v2.5/:$CUDAROOT/bin:$PWD:$PATH

export PATH=$MAIN_ROOT/utils/:$SPNET_ROOT/bin/:$PATH
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$MAIN_ROOT/tools/chainer_ctc/ext/warp-ctc/build:$CUDAROOT/lib64
#source $MAIN_ROOT/tools/venv/bin/activate
source $BUT_CONDA/bin/activate py36_cuda9_torch4
export PYTHONPATH=$MAIN_ROOT:$SPNET_ROOT:$KALDI_ROOT/kaldi-io-for-python:$BUT_CONDA/envs/py36_cuda9_torch4/bin:$SPNET_ROOT/lm/:$SPNET_ROOT/tts:$SPNET_ROOT/asr/:$SPNET_ROOT/nets/:$MAIN_ROOT/utils/:$SPNET_ROOT/bin/:$PYTHONPATH

export OMP_NUM_THREADS=1
export CC="/usr/local/bin/gcc-5.3"
export CXX="/usr/local/bin/g++-5.3"

export CPATH=$CUDA_HOME/include
