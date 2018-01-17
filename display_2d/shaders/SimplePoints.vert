#version 330

in vec4 position;
in vec4 color;

out vec4 dstColor;

void main(){
 dstColor = color;
 gl_Position = position;
}
