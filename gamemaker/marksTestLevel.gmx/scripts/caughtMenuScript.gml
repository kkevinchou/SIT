instance_create(0, 0, flynnFailScreen)

//If the game is not paused, create the snapshot and pause the game, else delete the snapshot from memory and unpause the game.
if(flynnFailScreen.isPaused = 0)
{   
    //Take the snapshot and put it in a temporary variable. This is good enough, but let's make it more pretty.
    var tempspr;
    
    tempspr=sprite_create_from_screen(0,0,room_width,room_height,0,0,0,0)

    //Lets darken the image and blur it.
    var col; 
    col=make_color_rgb(180,180,180);
    draw_sprite_ext(tempspr,-1,0,0,1,1,0,col,0.8);
            
    //To save the extra changes we did to the temporary snapshot, we take another
    //snapshot of the canvas with the effects on it.
    flynnFailScreen.m_PauseSpr=sprite_create_from_screen(0,0,room_width,room_height,0,0,0,0);
    
    //Now that we took the final snapshot of the canvas, we can delete the temporary snapshot.
    sprite_delete(tempspr)
    
    //Deactivate everything except yourself and pause the game.
    instance_deactivate_all(false);
    instance_activate_object(flynnFailScreen);
    flynnFailScreen.isPaused = 1;
    

}
else
{
    sprite_delete(escapeMenu.m_PauseSpr);
    flynnFailScreen.m_PauseSpr=-100;
     
    //Activate everything and unpause the game
    instance_activate_all();
    flynnFailScreen.isPaused=0;
}
