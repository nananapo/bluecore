set file_list [open "ファイルリストのパス" r]
while {[gets $file_list line] != -1} {
    # skip blank or comment line
    if {[string trim $line] eq "" || [string index $line 0] eq "#"} {
        continue
    }
    # add file to project
    add_files -force -norecurse $line
}
close $file_list