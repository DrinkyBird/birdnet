/**
 * @externs
 */

const CG = {};
CG.id = 0;
CG.title = "";
CG.sheet = "";

window.navbarClick = function() { }

google.charts = {};
/**
  * @param {string} a
  * @param {*} b
  */
google.charts.load = function(a, b) { };
google.charts.setOnLoadCallback = function(a) { };
google.visualization = {};
google.visualization.Query = class {
	/**
	  * @param {string} a
	  * @param {*} b
	  */
	constructor(a, b) { }
	send(a) { }
};
google.visualization.DataTable = class {
	constructor() { }
	/**
	  * @param {number} a
	  * @param {string} b
	  */
	setColumnLabel(a, b) { }
};
google.visualization.DataView = class {
	/**
	  * @param {google.visualization.DataTable} a
	  */
	constructor(a) { }
	/**
	  * @param {Array.<Number>} a
	  */
	setColumns(a) { }
};
google.visualization.LineChart = class {
	constructor(a) { }
	/**
	  * @param {google.visualization.DataView} a
	  * @param {*} b
	  */
	draw(a, b) { }
};
google.visualization.CallbackResponse = class {
	constructor() { }
	/** @return {boolean} */
	isError() { }
	/** @return {google.visualization.DataTable} */
	getDataTable() { }
	/** @return {string} */
	getMessage() { }
	/** @return {string} */
	getDetailedMessage() { }
};