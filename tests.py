import subprocess
def enableHouModule(hou_version : str):
    '''Set up the environment so that "import hou" works.'''
    import sys, os
    hou_home = "C:\Program Files\Side Effects Software\Houdini {}".format(hou_version)
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

enableHouModule("19.5.435")
import hou 
import  json 

userdir = hou.getenv("HOUDINI_USER_PREF_DIR")

subp = subprocess.Popen(["python", f"{userdir}/Scripts/CacheQueuer/hou_render.py", 
                         "D:/3D Objects/projectes_3d/Pipeline/QueuerTests/QueuerTests.hiplc", 
                         "/obj/Destruction/cache_shell"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

data = {"hip_file":"D:/3D Objects/projectes_3d/Pipeline/QueuerTests/QueuerTests.hiplc", "node_path": "/obj/Destruction/cache_shell"}

data = json.dumps(data)+"\n"
subp.stdin.write(data.encode())	

while True:
    data = subp.stdout.readline()
    if data:
        print(data.decode("utf-8"))
    if subp.poll() is not None:
        break