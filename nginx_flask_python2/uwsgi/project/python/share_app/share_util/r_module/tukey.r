library("RJSONIO")
library(agricolae)

# get info from args
args=(commandArgs (TRUE))
in_args <- fromJSON(args[1])

# run tukey
res = list()
factor_l <- levels(factor(in_args$factor))
if(in_args$alpha){
	var_af = in_args$alpha
}else{
	var_af = 0.05
}

for(i in c(1:length(in_args$data))){
	s_mod <- aov(in_args$data[[i]] ~ in_args$factor)
	o_tukey = HSD.test(s_mod,'in_args$factor',alpha=var_af)
	rownames(o_tukey$group) <- o_tukey$group$trt
	t_res <- cbind(o_tukey$means[match(factor_l,rownames(o_tukey$means)),1:2],o_tukey$group[match(factor_l, rownames(o_tukey$group)),3])
	colnames(t_res) <- c("mean","std","mark")
	res[[i]] <- t_res
}
write(toJSON(list("result"=res,"factor"=factor_l),collapse =""),args[2])
