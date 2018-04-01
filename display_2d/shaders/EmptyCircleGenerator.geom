#version 330 core

#define MAX_VERTICES 101

layout(points) in;
layout(line_strip, max_vertices = MAX_VERTICES) out;

in vec3 geom_color[];
in float geom_radius[];

uniform mat4 model_view_projection;

out vec3 frag_color;

const float PI = 3.1415926;

void main()
{
    frag_color = geom_color[0];

    for (int i = 0; i < MAX_VERTICES; i++) {
        // Angle between each side in radians
        float ang = PI * 2.0 / (MAX_VERTICES - 1) * i;

        // place points around center
        vec4 offset = vec4(cos(ang) * geom_radius[0], -sin(ang) * geom_radius[0], 0.0, 0.0);
        gl_Position = model_view_projection * (gl_in[0].gl_Position + offset);

        EmitVertex();
    }

    EndPrimitive();
}