'''OpenGL extension EXT.memory_object_fd

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.memory_object_fd to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/memory_object_fd.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.memory_object_fd import *
from OpenGL.raw.GL.EXT.memory_object_fd import _EXTENSION_NAME

def glInitMemoryObjectFdEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION