import subprocess
import hou

userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
subprocess.Popen(f"hython {userdir}/Scripts/CacheQueuer/main.py")