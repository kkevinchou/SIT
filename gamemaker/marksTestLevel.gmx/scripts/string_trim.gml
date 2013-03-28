/*
This trims spaces from the start or end of a string
arg 0 - STRING - The string e.g "   hello   "
*/

var i,txt,len,str;

if !is_string(argument0) {return "";exit;}

if argument0="" {return "";exit;}
else
if string_count(" ",argument0)==string_length(argument0) {return "";exit;}

len=string_length(argument0);

for (i=1;i<=len;i+=1)
 {
 str=string_char_at(argument0,i);
 if str!=" " break
 }
 
txt=string_copy(argument0,i,(len-i)+1);

len=string_length(txt);

for (i=len;i>=1;i-=1)
 {
 str=string_char_at(txt,i);
 if str!=" " break
 }
 
i+=1;
txt=string_delete(txt,i,(len-i)+1);

return txt
