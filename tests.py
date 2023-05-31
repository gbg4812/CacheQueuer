import json
import math
import subprocess


def enableHouModule(hou_version: str):
    '''Set up the environment so that "import hou" works.'''
    import sys
    import os
    hou_home = "C:\Program Files\Side Effects Software\Houdini {}".format(
        hou_version)
    # Importing hou will load Houdini's libraries and initialize Houdini.
    # This will cause Houdini to load any HDK extensions written in C++.
    # These extensions need to link against Houdini's libraries,
    # so the symbols from Houdini's libraries must be visible to other
    # libraries that Houdini loads.  To make the symbols visible, we add the
    # RTLD_GLOBAL dlopen flag.
    if hasattr(sys, "setdlopenflags"):
        old_dlopen_flags = sys.getdlopenflags()
        sys.setdlopenflags(old_dlopen_flags | os.RTLD_GLOBAL)

    # For Windows only.
    # Add %HFS%/bin to the DLL search path so that Python can locate
    # the hou module's Houdini library dependencies.  Note that
    # os.add_dll_directory() does not exist in older Python versions.
    # Python 3.7 users are expected to add %HFS%/bin to the PATH environment
    # variable instead prior to launching Python.
    if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
        os.add_dll_directory("{}/bin".format(hou_home))

    try:
        import hou
    except ImportError:
        # If the hou module could not be imported, then add
        # $HFS/houdini/pythonX.Ylibs to sys.path so Python can locate the
        # hou module.
        sys.path.append("{}/houdini/python3.9libs".format(hou_home))
        import hou
    finally:
        # Reset dlopen flags back to their original value.
        if hasattr(sys, "setdlopenflags"):
            sys.setdlopenflags(old_dlopen_flags)


data = {"hip_file": "D:/3D Objects/projects/PipelineDev/CacheQueuer/test_v1.hiplc",
        "node_path": "/obj/Sim_Test/cache_cloth_fire"}

data = json.dumps(data)

subp = subprocess.Popen(["python", "D:/Documents/houdini19.5/Scripts/CacheQueuer/hou_render.py",
                        data], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    data = subp.stdout.readline()
    data = data.rstrip(b'\r\n')

    if data:
        try:
            objdata: dict = json.loads(data)
            print(objdata.get("Progress"))
        except json.JSONDecodeError:
            print(data.decode("utf-8"))

    if subp.poll() is not None:
        break

print(subp.stderr.read().decode("utf-8"))
