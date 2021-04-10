module.id='page_taxa';
var extend = require('util')._extend;
/**
* create(new) form view without jquery with simple attr and reset, submit functions.
* @constructs page_taxa
* @param {DOM} dom - DOM of this view
* @param {Object} args
* @returns {Object} this page_taxa object
*/
function page_taxa(dom,args){
	this.doms={body:dom};
	this.mod = {};
	this.args = extend({
		dl_files:['html','tsv']
	},args);
	this.var = {};
	this.init();
}
module.exports = page_taxa;
/**
* initiation
*/
page_taxa.prototype.init = function(){
	var self=this;
	// setup view
	this.doms.body.append_by_array([
		{name:'h4',child:['upload your table with taxonomy id and their count separate by tab']},
		{name:'form',attr:{name:'form_krona'}},
		{name:'div',attr:{name:'result_krona',style:'display:none'},child:[
			{name:'span',attr:{name:'krona_res_msg'}},
			{name:'div',attr:{name:'dl_krona'}}
		]}
	]);
	// get all name DOM
	Array.prototype.slice.apply(this.doms.body.querySelectorAll('[name]')).map(function(v){
		self.doms[v.getAttribute('name')] = v;
	});
	this.mod.form_krona = new this.args.tools.myform(this.doms.form_krona);
	this.mod.form_krona.add_inputs([
		{name:'input',attr:{name:'f_tax2count',type:'file',required:'required'},label:'Taxa Table'}
	]);
	// add download button in result
	this.args.dl_files.map(function(v){
		self.doms.dl_krona.append_by_array([
			{name:'button',attr:{class:v}}
		]);
	});
	// events
	this.doms.dl_krona.addEventListener('click',function(e){
		var t_class = e.target.classList[0];
		if(self.args.dl_files.indexOf(t_class)!=-1){
			saveAs(new Blob([self.var.krona_data[t_class]],{type: "text/plain;charset=utf-8"}),
				self.var.f_tax2count+'.'+t_class
			);
		}
	});
	this.mod.form_krona.submit_callback = function(e){
		// read table file
		self.var.f_tax2count = self.doms.form_krona.f_tax2count.files[0].name;
		var fdom = new FileReader(),
			tax2count;
		fdom.onload = function(e){
			tax2count = e.target.result.split('\n').reduce(function(a,b,ind){
				var t_b = b.split('\t');
				if(t_b.length > 1){
					a[t_b[0]]=t_b[1];
				}
				return a;
			},{});
			// ajax start
			self.args.tools.ajax.post(self.args.url.tax_krona,{tax2count:JSON.stringify(tax2count)},{
				success:function(data){
					self.doms.result_krona.style.display ='block';
					var p_data = JSON.parse(data);
					if(p_data.html.length){
						self.var.krona_data = p_data;
						self.doms.dl_krona.style.display = 'block';
						self.args.dl_files.map(function(v){
							self.doms.dl_krona.querySelector('.'+v).innerHTML = self.var.f_tax2count+'.'+v;
						});
						self.doms.krona_res_msg.innerHTML = p_data.ex_ids.length+' taxid can not find lineage';
					}else{
						self.doms.krona_res_msg.innerHTML = 'no taxid can find their lineage, please check again!';
						self.doms.dl_krona.style.display = 'none';
					}
				}
			});
		};
		fdom.readAsText(self.doms.form_krona.f_tax2count.files[0],"UTF-8");
	}
	return this;
}
/**
* render by history.state
*/
page_taxa.prototype.render = function(state){
	//this.doms.body.innerHTML = 'get taxa view';
}
