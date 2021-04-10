/**
* create ms scan view of result
* @constructor
* @version 0.0.1
* @param {DOM} view - view container(div)
* @param {object.<string, number>} args - arguments for view
*/
function msscan_res_view(dom,args){
	var self = this;
	this.doms = {body:dom}
	// setup default value
	this.args = {
		view_json:[
			{name:'h3',child:['Statistic']},
			{name:'p',html:'Find <span class="pep_num"></span> peptide segments from the spectrums associated with <span class="prot_num"></span> proteins in database'},
			{name:'div',attr:{class:'table_view'}}
		]
	};
	if(args){
		Object.keys(args).map(function(v){self.args[v]=args[v]});
	}
	this.data={},this.mods={};
	this.init();
	return this;
}
/**
* initiate base DOM structure of view
*/
msscan_res_view.prototype.init = function(){
	var self = this;
	// create view
	this.doms.body.append_by_array(this.args.view_json);
	// register doms
	var id2dom = {'pep_num':'span.pep_num','prot_num':'span.prot_num','res_table':'div.table_view'};
	Object.keys(id2dom).map(function(v){
		self.doms[v] = self.doms.body.querySelector(id2dom[v]);
	});
}
/**
* calculate some data after input
* @param {Object} data - ms_json from render
* @return {Object} return this.data.ms_json
*/
msscan_res_view.prototype.ms_enrich = function(data){
	// count peptide cover range of proteins(prot2pep_cover)
	var t_ranges,res={};
	Object.keys(data.prot2pep_ranges).map(function(v){
		t_ranges = data.prot2pep_ranges[v].transpose().slice(1,3).transpose();
		res[v] = t_ranges.range_merge();
	});
	data.prot2pep_cover = res;
	return data;
}
/**
* generate data and colnames for simple table view
* @param {Object} data - this.data.ms_json
* @return {Object} data and colnames for simple table view
*/
msscan_res_view.prototype.ms_oview_data = function(data){
	// count peptide cover range of proteins(prot2pep_cover)
	var t_len,res={
		colnames:['Protein','Peptide','AA number','coverage%']
	};
	res.data = Object.keys(data.prot2pep_ranges).map(function(v){
		// count peptide cover aa num
		t_len=data.prot2pep_cover[v].map(function(v_1){return v_1[1]-v_1[0]}).sum();
		return [v, data.prot2pep_ranges[v].length, t_len, Math.round(100*t_len/data.prot2len[v])];
	});
	return res;
}
/**
* load data and render the view
* @param {DOM} view - view container(div)
* @return {Object} return this
*/
msscan_res_view.prototype.render = function(data){
	this.data.ms_json = this.ms_enrich(data);
	// simple Statistic
	this.doms.pep_num.innerHTML = Object.keys(data.pep2scan_scores).length;
	this.doms.prot_num.innerHTML = Object.keys(data.prot2len).length;
	// table_view
	this.mods.ms_table = new mytable(this.doms.res_table);
	this.mods.ms_table.render(this.ms_oview_data(this.data.ms_json));
}
