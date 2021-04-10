library("RJSONIO")
args=(commandArgs (TRUE))
in_args <- fromJSON(args[1])
write(toJSON(in_args),args[2])
