#compdef genpass
_arguments \
  '-h[show help]' \
  '--help[show help]' \
  '-l[password length]:length:' \
  '--length[password length]:length:' \
  '-n[number of passwords]:count:' \
  '--count[number of passwords]:count:' \
  '--lower[include lowercase letters]' \
  '--upper[include uppercase letters]' \
  '--digits[include digits]' \
  '--symbols[include symbols]' \
  '--symbol-set[custom symbol set]:symbols:' \
  '--no-ensure[disable ensure-each-type rule]' \
  '--no-ambiguous[exclude ambiguous characters (l, 1, I, O, 0)]' \
  '--entropy[show password entropy]' \
  '-c[copy to clipboard]' \
  '--clipboard[copy to clipboard]' \
  '--format[output format]:format:(plain json delimited)' \
  '--config[show current configuration]' \
  '--save-config[save options as defaults]'
