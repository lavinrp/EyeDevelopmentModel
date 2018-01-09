#version 120

attribute vec4 position;
attribute vec4 color;

varying vec4 dstColor;

void main(){
 dstColor = color;
 gl_Position = position;
}
