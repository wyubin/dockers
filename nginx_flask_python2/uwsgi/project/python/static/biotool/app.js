"use strict"

require('../../../nodejs/lib/stdlib.HTMLElement.js');
var navi_bar = require('../../../nodejs/lib/navi_bar.js'),
	router = require('../../../nodejs/lib/Router.js'),
	model = {
		taxa:require('./page_taxa.js')
	},
	tools = {
		ajax:require('../../../nodejs/lib/my_ajax.js'),
		myform: require('../../../nodejs/static/myform/myform.js')
	},
	url = {
		tax_line:'../../taxa/lineage/',
		tax_krona:'../../taxa/krona/'
	};
module.id='spa';
/**
* create(new) object for handle SPA.
* @constructs spa
* @param {object} dom - dom of spa(usually is document.body)
* @returns {Object} this
*/
var spa = function(dom){
	this.doms = {body:dom};
	this.view = {};
	this.router = new router({default_hash:'all'});
	this.__init__();
}
/**
* initiation
*/
spa.prototype.__init__ = function(){
	// init dom structure
	var dom_js = [
		{name:'header',child:[{name:'nav'}]},
		{name:'main'},
		{name:'footer'}
	];
	var self = this;
	this.doms.body.append_by_array(dom_js);
	this.doms.main = this.doms.body.querySelector('main');
	this.view.nav = new navi_bar(this.doms.body.querySelector('nav'),{menu:[{'taxa':'TAXA'}]});
	// set all model instance
	for(var i in model){
		this.doms.main.append_by_array([{name:'div',attr:{name:i}}]);
		this.view[i]=new model[i](this.doms.main.querySelector('[name='+i+']'),{
			router:this.router,
			url:url,
			tools:tools
		});
	}
	// add router
	this.router.routes['all']=function(state){
		// hide all page
		Array.prototype.slice.apply(self.doms.main.querySelectorAll('main>div')).map(function(v){
			v.classList.add('hide');
		});
		if(!(state.hash in model)){
			state.hash='taxa';
		}
		self.view.nav.active(state.hash);
		// show assign page
		self.view[state.hash].doms.body.classList.remove('hide');
		self.view[state.hash].render(state);
	};
	// nav link
	this.view.nav.click_handler = function(page_name){
		self.router.goto({hash:page_name});
	}
}
// execute
module.exports = new spa(document.body);
window.onload = function(){module.exports.router.goto()};
