#!/usr/bin/python                                                             
# vim: set fileencoding=utf-8 :
###########################################################################
#                                                                         #
#    .--~*teu.                                                  .uef^"    #
#  dF     988Nx    .xn!~%x.                                  :d88E        #
# d888b   `8888\  x888   888.         u                  .   `888E        #
# ?8888   98888F X8888   8888:     us888u.          .udR88N   888E .z8k   #
#  "**"  x88888~ 88888   X8888  .@88 "8888"        /888'888k  888E~?888L  #
#       d8888*`  88888   88888  9888  9888         9888 'Y"   888E  888E  #
#     z8**"`   : `8888  :88888X 9888  9888         9888       888E  888E  #
#   :?.....  ..F   `"**~ 88888' 9888  9888     .   9888       888E  888E  #
#  /""888888888~  .xx.   88888  9888  9888   .@8c  ?8888u../  888E  888E  #
#  8:  "888888*  '8888   8888~  "888*""888" '%888"  "8888P'  m888N= 888/  #
#  ""    "**"`    888"  :88%     ^Y"   ^Y'    ^*      "P'     `Y"   888   #
#                   ^"===""                                         J88"  #
#  glslmandelbrot.py                                     ,---.    ,@%     #
#  Description: renders the mandelbrot set on the gpu   |'o o'|           #
#  Author:  Jonas Wagner                              B=.| m |.=B         #
#  License: GNU GPL V3 or later                          `,-.´            #
#  Website: http://29a.ch/                            B=´     `=B         #
#                                                                         #
#  Usage:                                                                 #
#  You can move arround by dragging with the left mouse button            #
#  You can zoom in and out with your mouse wheel                          #
#  You can toggle the fullscreen mode with the F key                      #
#  You can toggle the fps display with the F1 key                         #
#  You can save a screenshot to a file called screenshot.png with F2      #
#  enjoy!                                                                 #
#                                                                         #
#  Legal Foo                                                              #
#                                                                         #
#  Copyright (C) 2008 Jonas Wagner                                        #
#  This program is free software; you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation; either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
###########################################################################

import ctypes as c

import pyglet
import pyglet.clock
import pyglet.window
from pyglet.window import key
from pyglet import gl

vertex_shader = """
uniform float real;
uniform float w;
uniform float imag;
uniform float h;

varying float xpos;
varying float ypos;

void main(void)
{
  xpos = clamp(gl_Vertex.x, 0.0,1.0)*w+real;
  ypos = clamp(gl_Vertex.y, 0.0,1.0)*h+imag;

  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

fragment_shader = """
varying float xpos;
varying float ypos;
varying float zpos;
void main (void)
{
    float iter = 0.0;
    float max_square = 3.0;
    float square = 0.0;
    float r = 0.0;
    float i = 0.0;
    float rt = 0.0;
    float it = 0.0;
    while(iter < 1.0 && square < max_square)
    {
        rt = (r*r) - (i*i) + xpos;
        it = (2.0 * r * i) + ypos;
        r = rt;
        i = it;
        square = (r*r)+(i*i);
        iter += 0.005;
    }
    gl_FragColor = vec4 (iter, iter, sin(iter*2.00), 1.0);
}
"""

class ShaderException(Exception):
    pass

class Shader(object):
    """Wrapper to create opengl 2.0 shader programms"""
    def __init__(self, vertex_source, fragment_source):
        self.program = gl.glCreateProgram()
        self.vertex_shader = self.create_shader(vertex_source,
                gl.GL_VERTEX_SHADER)
        self.fragment_shader = self.create_shader(fragment_source,
                gl.GL_FRAGMENT_SHADER)
        gl.glAttachShader(self.program, self.vertex_shader)
        gl.glAttachShader(self.program, self.fragment_shader)
        gl.glLinkProgram(self.program)
        message = self.get_program_log(self.program)
        if message:
            raise ShaderException(message)

    def create_shader(self, source, shadertype):
        # get a char[]
        sbuffer = c.create_string_buffer(source)
        # get a char **
        pointer = c.cast(c.pointer(c.pointer(sbuffer)),
                c.POINTER(c.POINTER(c.c_char)))
        # a long * NULL pointer
        nulll = c.POINTER(c.c_long)()
        shader = gl.glCreateShader(shadertype)
        gl.glShaderSource(shader, 1, pointer, None)
        gl.glCompileShader(shader)
        message = self.get_shader_log(shader)
        if message:
            raise ShaderException(message)
        return shader

    def set_uniform_f(self, name, value):
        location = gl.glGetUniformLocation(self.program, name)
        gl.glUniform1f(location, value)

    def __setitem__(self, name, value):
        """pass a variable to the shader"""
        if isinstance(value, float):
            self.set_uniform_f(name, value)
        else:
            raise TypeError("Only floats are supported so far")

    def use(self):
        gl.glUseProgram(self.program)

    def stop(self):
        gl.glUseProgram(0)

    def get_shader_log(self, shader):
        return self.get_log(shader, gl.glGetShaderInfoLog)

    def get_program_log(self, shader):
        return self.get_log(shader, gl.glGetProgramInfoLog)

    def get_log(self, obj, func):
        log_buffer = c.create_string_buffer(4096)
        buffer_pointer = c.cast(c.pointer(log_buffer), c.POINTER(c.c_char))
        written = c.c_int()
        func(obj, 4096, c.pointer(written), buffer_pointer)
        return log_buffer.value


class MainWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width=640, height=480,
                resizable=True)
        self.fps = pyglet.clock.ClockDisplay()
        self.shader = Shader(vertex_shader, fragment_shader)
        self.real = -2.0
        self.w = 3.0
        self.imag = -1.0
        self.h = 2.0
        self.show_fps = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.has_exit = True
        elif symbol == key.F:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == key.F1:
            self.show_fps = not self.show_fps
        elif symbol == key.F2:
            pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.real -= self.w / self.width * dx
        self.imag -= self.h / self.height * dy

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.real += (float(x) / self.width * self.w) - self.w * 0.25
            self.w *= 0.5
            self.imag += (float(y) / self.height * self.h) - self.h * 0.25
            self.h *= 0.5
        else:
            self.real += (float(x) / self.width * self.w) - self.w
            self.w *= 2.0
            self.imag += (float(y) / self.height * self.h) - self.h
            self.h *= 2.0

    def on_resize(self, width, height):
        ratio = float(width) / height
        self.w = ratio * self.h
        pyglet.window.Window.on_resize(self, width, height)

    def run(self):
        while not self.has_exit:
            pyglet.clock.tick()
            self.dispatch_events()
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glLoadIdentity()
            self.shader.use()
            self.shader["real"] = self.real
            self.shader["w"] = self.w
            self.shader["imag"] = self.imag
            self.shader["h"] = self.h
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex3f(0.0, 0.0, 0.0)
            gl.glVertex3f(0.0, self.height, 0.0)
            gl.glVertex3f(self.width, self.height, 0.0)
            gl.glVertex3f(self.width, 0.0, 0.0)
            gl.glEnd()
            self.shader.stop()
            if self.show_fps:
                self.fps.draw()
            self.flip()

def main():
    MainWindow().run()

if __name__ == "__main__":
    main()
