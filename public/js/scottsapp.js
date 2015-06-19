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
	for( i=0; i<cityevents.length; i++ )
	{
		cityevent = cityevents[i];
		var evt = $("<div />", {"class":"cityevent",id:cityevent["id"]});
		var title = $("<div />", {"class":"cityevent_title",text:cityevent["title"]});
		var description = $("<span />", {"class":"cityevent_description",text:cityevent["description"]});
		var l = cityevent["roadevents"].length;
		if( l > 1 )
		{
			var closures = $("<ul />", {"class":"cityevent_closures"});
			for( j=0; j<cityevent["roadevents"].length; j++ )
			{
				var roadevent = cityevent["roadevents"][j];
				//var closure = $("<li />", {"class":"cityevent_closure",html:"<b><u>"+roadevent["description"]+"</u></b> from "+roadevent["schedule"]});
				var closure = $("<li />", {"class":"cityevent_closure",html:"<b><u>"+roadevent["description"]+"</u></b>"});
				var schedule = $("<div />", {"class":"cityevent_schedule",html:"<i>"+roadevent["schedule"]+"</i>."});
				closure.append(schedule);
				closures.append(closure);
			}
			evt.append(description);
			evt.append(closures);
		}
		else
		{
			var roadevent = cityevent["roadevents"][0];
			var closure = $("<div />", {"class":"cityevent_closure",html:"<b><u>"+roadevent["description"]+"</u></b>"});
			evt.append(closure);
			var schedule = $("<div />", {"class":"cityevent_schedule",html:"<i>"+roadevent["schedule"]+"</i>."});
			evt.append(schedule);
			evt.append(description);
		}
		if( cityevent["contact"] != "" )
		{
			evt.append($("<div />", {"class":"cityevent_contact",text:cityevent["contact"]}));
		}
		if( cityevent["url"] != "" )
		{
			var url = $("<a />", {href:cityevent["url"],text:cityevent["url"]});
			evt.append(url);
		}
		$("#cityevents").append(evt);
	}
}
