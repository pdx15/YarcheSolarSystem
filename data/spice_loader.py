import os
import spiceypy as spice


KERNEL_DIR = os.path.join("data", "kernels")
TEXT_KERNEL_EXTENSIONS = (".tls", ".tpc", ".tf", ".tm")
SPK_EXTENSIONS = (".bsp",)


def _list_kernel_files(base_dir):
    if not os.path.isdir(base_dir):
        return []

    entries = [
        os.path.join(base_dir, name)
        for name in os.listdir(base_dir)
        if os.path.isfile(os.path.join(base_dir, name))
    ]

    text_kernels = sorted(
        path for path in entries
        if os.path.splitext(path)[1].lower() in TEXT_KERNEL_EXTENSIONS
    )
    spk_kernels = sorted(
        path for path in entries
        if os.path.splitext(path)[1].lower() in SPK_EXTENSIONS
    )

    return text_kernels + spk_kernels


def load_kernels():
    loaded = []

    for kernel_path in _list_kernel_files(KERNEL_DIR):
        spice.furnsh(kernel_path)
        loaded.append(kernel_path)

    return loaded


def get_loaded_spk_targets(kernel_paths):
    targets = set()

    for kernel_path in kernel_paths:
        if os.path.splitext(kernel_path)[1].lower() not in SPK_EXTENSIONS:
            continue

        try:
            targets.update(int(code) for code in spice.spkobj(kernel_path))
        except Exception:
            continue

    return targets
    
def get_et():
    return spice.str2et("2025-01-01T00:00:00")

def advance_et(et, dt, scale):
    return et + dt * scale
