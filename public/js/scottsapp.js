$(document).ready(start());

function start()
{
	$(function() { //DOM Ready
		ajaxLoad("scottsapp/", ajaxOnResult);
	});
}

function ajaxLoad(uri, callback)
{
	console.log(uri);
	var request = (window.XMLHttpRequest) ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
	request.onreadystatechange = callback;
	request.open("GET", uri);
	request.send(null);
}

function ajaxOnResult(evt)
{
	if ((evt.currentTarget.readyState == 4) && (evt.currentTarget.status == 200 || evt.currentTarget.status == 0))
	{
		var cityevents = JSON.parse(evt.currentTarget.responseText);
		console.log(cityevents);
		pprint( cityevents )
	}
	else
	{
		console.log("HTTP status: "+evt.currentTarget.status);
	}
}

function pprint( cityevents )
{
	cityeventjson = JSON.stringify(cityevents);
	$(".cityevent").html("<pre>"+cityeventjson+"</pre>");
}
