var xx,yy,w,h,mx,my;

varx1=argument0;
vary1=argument1;
varx2=argument2;
vary2=argument3;
mx=mouse_x;
my=mouse_y;


if (mx>=varx1 && my>=vary1 && mx<=varx2 && my<vary2){  return 1;}
else { return 0;}
