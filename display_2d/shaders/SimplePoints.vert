#version 330
in vec2 vert;
in vec3 vert_color;

uniform mat4 projection;
uniform mat4 model;

out vec3 geom_color;

void main() {
    gl_Position =  vec4(vert, 0.0, 1.0);
    geom_color = vert_color;
}