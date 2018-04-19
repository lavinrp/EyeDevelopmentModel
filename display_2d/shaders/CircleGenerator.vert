#version 330 core
in vec2 vert;
in vec3 vert_color;
in float vert_radius;

uniform mat4 model_view_projection;

out vec3 geom_color;
out float geom_radius;

void main() {
    gl_Position =  vec4(vert, -1.0, 1.0);
    geom_color = vert_color;
    geom_radius = vert_radius;
}