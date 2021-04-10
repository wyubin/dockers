function model_analyze(view,args){
	this.args = $.extend({},args);
	this.jq = {body:$(view)};
}
model_analyze.prototype.render = function(){}
