
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
from .abstract_renderer import RendererInfo, AbstractRenderer

#renders a single task given a id
class HouRenderer(AbstractRenderer):   
    frame = 0
    frame_range = (0, 0, 0)
    rendering = False


    def renderTask(task: dict):
        import hou

        def render_event_handler(rop_node, event_type, time):
            if event_type == hou.ropRenderEventType.PreFrame:
                HouRenderer.frame += 1	
                f_range = HouRenderer.frame_range
                frame = HouRenderer.frame
                
                progress = frame - f_range[0]
                progress /= (f_range[1] - f_range[0]) * f_range[2]
                
                HouRenderer.progress_handler(progress)

                
        hou.hipFile.load(task.get("hip_file"))
        HouRenderer.rendering = True

        node = hou.node(task.get("rop_path"))

        HouRenderer.frame = 0
        HouRenderer.frame_range = (node.evalParm("f1"), node.evalParm("f2"), 1)

        if type(node) == hou.RopNode:
            try:
                node.addRenderEventCallback(render_event_handler)
                node.render()
            except hou.OperationFailed:
                return False
        elif type(node) == hou.SopNode:
            try:
                rop_node = node.node('render')
                rop_node.addRenderEventCallback(render_event_handler)
                rop_node.render()
            except hou.OperationFailed:
                return False
        else:    
            print('the node is not of the correct type')
    
        return True

    def getInfo(task: dict) -> RendererInfo:
        import hou
        try:
            hou.hipFile.load(task.get("hip_file"))
            node = hou.node(task.get("rop_path"))
            try:
                substeps = node.evalParm("substeps")
            except hou.OperationFailed:
                substeps = 1

            frame_range = (node.evalParm("f1"), node.evalParm("f2"), substeps)
            
            rop_path = task.get("rop_path")
            out_path = node.evalParm("sopoutput")
            
            info = RendererInfo(label1=rop_path, label2=out_path, frame_range=frame_range)

            return info

        except FileNotFoundError:
            return RendererInfo()
        
        
