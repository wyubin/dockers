function model_home(view,args){
	this.args = $.extend({},args);
	this.jq = {body:$(view)};
}
model_home.prototype.render = function(){}
