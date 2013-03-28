var input_file = argument0
var return_text = ""

while(!file_text_eof(input_file)) {
    return_text = file_text_readln(input_file)

    // If special escape ``` is not used
    if( string_pos('```', return_text) == 0 ) {
        return return_text
    } else {
        // For special cases
        if( string_pos('bg_change:', return_text) != 0 ) {
            var pos = string_pos('bg_change:', return_text) + 10
            var bg_name = string_copy(return_text, pos, string_length(return_text) - pos -1);
            // Assign cut scene art by index
            background_index[0] = ds_map_find_value(cutscene_manager.background_map, real(bg_name))
        }       
    }
}
