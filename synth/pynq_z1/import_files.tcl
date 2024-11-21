set file_list [open "ファイルリストのパス" r]
while {[gets $file_list line] != -1} {
    # 空行やコメント行（# で始まる）をスキップ
    if {[string trim $line] eq "" || [string index $line 0] eq "#"} {
        continue
    }
    # ファイルをプロジェクトに追加
    add_files -norecurse $line
}
close $file_list