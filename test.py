import pygame as pg
import zengl

import mymodule

mymodule.init()

pg.init()

pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

pg.display.set_mode((1280, 720), pg.OPENGL | pg.DOUBLEBUF)

ctx = zengl.context()

size = pg.display.get_window_size()
image = ctx.image(size, 'rgba8unorm', samples=4)
depth = ctx.image(size, 'depth24plus', samples=4)
image.clear_value = (1.0, 1.0, 1.0, 1.0)

vertex_buffer = ctx.buffer(size=23 * 12)
uniform_buffer = ctx.buffer(size=64)

lines = ctx.pipeline(
    vertex_shader='''
        #version 330

        layout (std140) uniform Common {
            mat4 mvp;
        };

        layout (location = 0) in vec3 in_vert;

        void main() {
            gl_Position = mvp * vec4(in_vert, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330

        layout (location = 0) out vec4 out_color;

        void main() {
            out_color = vec4(0.0, 0.0, 0.0, 1.0);
        }
    ''',
    layout=[
        {
            'name': 'Common',
            'binding': 0,
        },
    ],
    resources=[
        {
            'type': 'uniform_buffer',
            'binding': 0,
            'buffer': uniform_buffer,
        },
    ],
    framebuffer=[image, depth],
    topology='line_strip',
    vertex_buffers=zengl.bind(vertex_buffer, '3f', 0),
    vertex_count=vertex_buffer.size // 12,
)

camera = zengl.camera((3.0, 2.0, 2.0), (0.0, 0.0, 0.0), aspect=16.0 / 9.0, fov=45.0)
uniform_buffer.write(camera)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    mymodule.update()
    vertex_buffer.write(mymodule.state)

    image.clear()
    depth.clear()
    lines.render()
    image.blit()

    pg.display.flip()
    pg.time.wait(10)

pg.quit()
