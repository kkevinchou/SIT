if (self.isChef == false) {
fynn.sprite_index = flynnRight
} else {
fynn.sprite_index = chefRight
}
self.x += moveSpeed
self.image_index = self.image_index+moveSpeed*.1
self.facing = 'Right'
//alarm[0] = 0


if (moveSpeed > 0 && curCircle < self.hearingCircle) {
    curCircle+=5
} 
