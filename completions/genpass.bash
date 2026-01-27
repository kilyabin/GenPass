_genpass() {
    local cur opts
    cur="${COMP_WORDS[COMP_CWORD]}"
    opts="--help -l --length -n --count --lower --upper --digits --symbols --symbol-set --no-ensure"
    COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}
complete -F _genpass genpass
