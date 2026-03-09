_genpass() {
    local cur opts
    cur="${COMP_WORDS[COMP_CWORD]}"
    opts="-h --help -l --length -n --count --lower --upper --digits --symbols --symbol-set --no-ensure --no-ambiguous --entropy -c --clipboard --format --config --save-config"
    COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}
complete -F _genpass genpass
