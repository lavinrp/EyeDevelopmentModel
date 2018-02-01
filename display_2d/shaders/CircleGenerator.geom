#version 330 core

#define MAX_VERTICES 101

layout(points) in;
layout(line_strip, max_vertices = MAX_VERTICES) out;

const float PI = 3.1415926;

void main()
{
    for (int i = 0; i < MAX_VERTICES; i++) {
        // Angle between each side in radians
        float ang = PI * 2.0 / (MAX_VERTICES - 1) * i;

        // Offset from center of point (to accomodate for aspect ratio)
        float aspect_ratio_offset_x = 1;
        float aspect_ratio_offset_y = 1;

        // place points around center
        vec4 offset = vec4(cos(ang) * aspect_ratio_offset_x, -sin(ang) * aspect_ratio_offset_y, 0.0, 0.0);
        gl_Position = gl_in[0].gl_Position + offset;

        EmitVertex();
    }

    EndPrimitive();
}