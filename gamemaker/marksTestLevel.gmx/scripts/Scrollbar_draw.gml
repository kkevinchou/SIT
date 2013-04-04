// Scrollbar_draw(x,y,width,height,Surface id)

var scroll_x, scroll_y, bar_y,  bar_min, bar_max, surw, surh, size, my;
size=15;

surwmax=surface_get_width(argument4);
surhmax=surface_get_height(argument4);
scroll_x=argument0;
scroll_y=argument1;
surw=argument2;
surh=argument3;


bar_y = scroll_y + surh + size;

bar_min=scroll_x+20;
bar_max=surw+scroll_x-20;


if (scrollbar.firstRun == true) {
    scrollbar.firstRun = false;
    part_yi=0;
    bar_x = bar_min + size;
    agganciato=false;
}

mx=mouse_x;
pageStep = 160;
smallStep = 80;

/***************************************************/

// Scroll up and down
if Mouse_enter(scroll_x,scroll_y,scroll_x+surw,scroll_y+surh+size){
  if (mouse_wheel_down()){
     if(bar_x < bar_max - size - smallStep){ bar_x += smallStep; }
     else {bar_x = bar_max - size;}
  }
  if (mouse_wheel_up()){
     if(bar_x > bar_min + size + smallStep){ bar_x -= smallStep; }
     else {bar_x = bar_min + size;}
  }
}

// If mouse clicks on scrolling bar, else if mouse is inside general bar
if Mouse_enter(bar_x-size,bar_y-size,bar_x+size,bar_y+size){
  if mouse_check_button_pressed(mb_left){
     agganciato=true;
  }
}
else{
 if Mouse_enter(bar_min,bar_y-size,bar_max,bar_y+size){
   if mouse_check_button_pressed(mb_left){   
     if(mx>bar_x){ 
         if(bar_x<bar_max-size-pageStep){ bar_x += pageStep; }
         else {bar_x=bar_max-size;}         
     }
     else if(mx<bar_x){ 
         if(bar_x>bar_min+size+pageStep){ bar_x -= pageStep; }
         else {bar_x=bar_min+size;}
     }     
  }
 }
}

if mouse_check_button_released(mb_left){  agganciato=false;  }

// If mouse dragging scrolling bar
if (agganciato==true){
  if (mx>bar_min+size && mx<bar_max-size){
    bar_x=mx;
  }
  else { 
    if (mx<bar_min+size){  bar_x=bar_min+size; }
    if (mx>bar_max-size){  bar_x=bar_max-size; }
  }
}   

// Click left arrow
if Mouse_enter(bar_min - 20, bar_y - size, bar_min - 1, bar_y + size){
  if mouse_check_button_pressed(mb_left){
    if(bar_x>bar_min+size+smallStep){ bar_x-=smallStep; }
    else {bar_x=bar_min+size;}
  }
}

// Click right arrow
if Mouse_enter(bar_max + 1, bar_y - size, bar_max + 21, bar_y + size) {
  if mouse_check_button_pressed(mb_left){
    if(bar_x<bar_max-size-smallStep){ bar_x+=smallStep; }
    else {bar_x=bar_max-size;}
  }
}


/*********************************************************************************/

part_xi= (  (surwmax-surw)* ((bar_x-size)-bar_min) / (bar_max-bar_min-(size*2) ) )

draw_surface_part(argument4,part_xi,part_yi,surw,surh,scroll_x,scroll_y);


//surface_set_target(argument4);

// Add rectangle on mouseover
for (i = 1; i <= 5; i++) {
    x1 = scrollbar.xStart + (i-1) * (scrollbar.xDelta + scrollbar.spriteWidth) - part_xi + scroll_x;
    y1 = scrollbar.yStart - part_yi + scroll_y;
    x2 = x1 + scrollbar.spriteWidth;
    y2 = y1 + scrollbar.spriteHeight;
    
    x1 = x1 + 5;
    y1 = y1 + 66;
    x2 = x2 - 10;
    y2 = y2 - 2;
    
    lineWidth = 6;
    
    if (x1 < scroll_x) x1 = scroll_x;
    if (x2 > 800 + scroll_x) x2 = 800 + scroll_x;
    
    if (Mouse_enter(x1, y1, x2, y2)) {
        
        draw_line_width_color(x1, y1, x2, y1, lineWidth, c_blue, c_silver);
        draw_line_width_color(x1, y2, x2, y2, lineWidth, c_silver, c_blue);
        
        if (x1 > scroll_x + 1) {
            draw_line_width_color(x1, y1 - 3, x1, y2 + 3, lineWidth, c_blue, c_silver);
        }
        if (x2 < 800 + scroll_x - 1) {
            draw_line_width_color(x2, y1 - 3, x2, y2 + 3, lineWidth, c_silver, c_blue);
        }       
        
        if (mouse_check_button_pressed(mb_left)) {
            switch(i) {
                case 1:
                case 2:
                case 3:
                    room_goto(room0);
                    break;
                // Bar level
                /*case 4:
                    cutscene_manager.current_room = 1
                    cutscene_manager.next_room = 2
                    room_goto(cutscreen)
                    break;*/
                // Final level
                case 4:
                    room_goto(Basement)
                    break;
            }
        }
    }
}

//surface_reset_target();


draw_set_color(c_gray);

// Draw entire general bar
draw_rectangle(bar_min - 20, bar_y - size, bar_max + 20, bar_y + size, 0);

// If mouse enters bar anywhere
if Mouse_enter(bar_min - 20, bar_y - size, bar_max + 20, bar_y + size) {
  if (mouse_check_button_pressed(mb_left)|| agganciato==true){ draw_set_color($000000);}
  else{ draw_set_color($777777);}
}
else { draw_set_color($555555);}

// Draw left triangle rectangle
draw_rectangle(bar_min - 20, bar_y-size, bar_min, bar_y+size,1);

// Draw right triangle rectangle
draw_rectangle(bar_max, bar_y-size, bar_max + 20, bar_y+size,1);



// If mouse hover over bar
if Mouse_enter(bar_x-size,bar_y-size,bar_x+size,bar_y+size){
  if (agganciato==true){ draw_set_color($110000);}
  else{ draw_set_color($bb2222);}
}
else{ draw_set_color($661111);}

// Draw scroll rectangle
draw_rectangle(bar_x-size,bar_y-size,bar_x+size,bar_y+size,0);




// If mouse hovers over left triangle
if Mouse_enter(bar_min - 20, bar_y-size,bar_min-1,bar_y+size,0){
 if mouse_check_button_pressed(mb_left){ draw_set_color($000000);}
 else{ draw_set_color($bb0000);}
}
else {draw_set_color($550000);}
draw_rectangle(bar_min - 20, bar_y-size,bar_min-1,bar_y+size,0);

// If mouse hovers over right triangle
if Mouse_enter(bar_max + 1, bar_y-size,bar_max+20,bar_y+size,0){
 if mouse_check_button_pressed(mb_left){
   draw_set_color($000000);}
   else{ draw_set_color($bb0000);}
}
else {draw_set_color($550000);}
draw_rectangle(bar_max, bar_y-size,bar_max+20,bar_y+size,0);



draw_set_color($ffffff);

// Draw left and right triangle
draw_triangle(bar_min - 4, bar_y-size+3, bar_min - 4, bar_y + size - 3, bar_min - 20, bar_y,0);
draw_triangle(bar_max + 4, bar_y-size+3, bar_max + 4, bar_y + size - 3, bar_max + 20, bar_y,0);

draw_set_color(c_black);
draw_rectangle(scroll_x - 1,scroll_y,scroll_x+surw,scroll_y+surh,1);





