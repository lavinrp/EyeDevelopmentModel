#version 330 core

#define MAX_VERTICES 101

layout(points) in;
layout(triangle_strip, max_vertices = MAX_VERTICES) out;

in vec3 geom_color[];
in float geom_radius[];

uniform mat4 model;

out vec3 frag_color;

const float PI = 3.1415926;

void main()
{
    frag_color = geom_color[0];
    const int half_max_vertices = MAX_VERTICES/2;

    for (int i = 0; i < half_max_vertices; i++) {
        // Angle between each side in radians
        float ang = PI * 2.0 / (half_max_vertices - 1) * i;

        // place on circle edge
        vec4 offset = vec4(cos(ang) * geom_radius[0], -sin(ang) * geom_radius[0], 0.0, 0.0);
        gl_Position = model * (gl_in[0].gl_Position + offset);

        EmitVertex();

        // add the center
        gl_Position = model * gl_in[0].gl_Position;
        EmitVertex();
    }

    EndPrimitive();
}