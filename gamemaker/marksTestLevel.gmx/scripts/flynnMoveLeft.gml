if (self.isChef == false) {
fynn.sprite_index = flynnLeft2
} else {
fynn.sprite_index = chefLeft
}
self.x -= moveSpeed
self.image_index = self.image_index+moveSpeed*.1
self.facing = 'Left'
//alarm[0] = 0


if (moveSpeed > 0 && curCircle < self.hearingCircle) {
    curCircle+=5
} 
