if (self.isChef == false) {
fynn.sprite_index = flynnTop
} else {
fynn.sprite_index = chefBack
}
fynn.y -= moveSpeed
fynn.image_index = fynn.image_index+(moveSpeed*.1)
fynn.facing = 'Back'
//fynn.alarm[0] = 0


if (moveSpeed > 0 && curCircle < self.hearingCircle) {
    curCircle+=5
} 
