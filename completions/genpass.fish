complete -c genpass -s h -l help -d "Show help message"
complete -c genpass -s l -l length -d "Password length" -r
complete -c genpass -s n -l count -d "Number of passwords" -r
complete -c genpass -l lower -d "Include lowercase letters"
complete -c genpass -l upper -d "Include uppercase letters"
complete -c genpass -l digits -d "Include digits"
complete -c genpass -l symbols -d "Include symbols"
complete -c genpass -l symbol-set -d "Custom symbol set" -r
complete -c genpass -l no-ensure -d "Disable ensure-each-type rule"
complete -c genpass -l no-ambiguous -d "Exclude ambiguous characters"
complete -c genpass -l entropy -d "Show password entropy"
complete -c genpass -s c -l clipboard -d "Copy to clipboard"
complete -c genpass -l format -d "Output format" -r -f -a "plain json delimited"
complete -c genpass -l config -d "Show current configuration"
complete -c genpass -l save-config -d "Save options as defaults"
