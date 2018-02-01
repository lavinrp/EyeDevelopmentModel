#version 330 core

layout(points) in;
layout(line_strip, max_vertices = 101) out;

const float PI = 3.1415926;

void main()
{
    for (int i = 0; i <= 100; i++) {
        // Angle between each side in radians
        float ang = PI * 2.0 / 101.0 * i;

        // Offset from center of point (0.3 to accomodate for aspect ratio).  This might be different for us - Brian
        vec4 offset = vec4(cos(ang) * 0.35, -sin(ang) * 0.4, 0.0, 0.0);
        gl_Position = gl_in[0].gl_Position + offset;

        EmitVertex();
    }

    EndPrimitive();
}