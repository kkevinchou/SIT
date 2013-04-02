self.sprite_index = flynnRight
self.x += moveSpeed
self.image_index = self.image_index+moveSpeed*.1
self.facing = 'Right'
//alarm[0] = 0


if (moveSpeed > 0 && curCircle < self.hearingCircle) {
    curCircle+=5
} 
