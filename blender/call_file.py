import bpy
import os

dir, name = os.path.split(bpy.data.filepath)
filename = os.path.join(dir, "main.py")
exec(compile(open(filename).read(), filename, 'exec'))
