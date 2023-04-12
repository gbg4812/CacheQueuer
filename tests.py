import typing

from renderers import HouRenderer
from threading import Thread

task = {"name": "cache_vellum_cloth", "rop_path": "/obj/Sim_Test/cache_vellum_cloth", "state": 0, "hip_file": "D:/3D Objects/projects/PipelineDev/CacheQueuer/test_v1.hiplc"}
th1 = Thread(target=HouRenderer.renderTask, args=((task), ))
th2 = Thread(target=HouRenderer.getInfo, args=((task), ))

th1.start()

th2.start()
th1.join()


