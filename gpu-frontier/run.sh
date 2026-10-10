#!/usr/bin/env bash
# Prime Tread GPU Frontier launcher — wires up the CUDA 12 runtime libs and
# the local display, then hands all args to the app.
SP="$HOME/.local/lib/python3.10/site-packages/nvidia"
export LD_LIBRARY_PATH="$SP/cuda_nvrtc/lib:$SP/cuda_runtime/lib:${LD_LIBRARY_PATH}"
export DISPLAY="${DISPLAY:-:1}"
exec python3 "$(dirname "$0")/gpu_frontier.py" "$@"
