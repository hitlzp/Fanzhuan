function doSubmit()//选择课程
{
	Showmessage();
}

function Showmessage()
{
	var course = document.getElementsByName("selectcourse");
	for(var i =0; i < course.length;i++)
	{
		if(course[i].checked == true)
			courseid = course[i].value;
	}
	var post_data ={
	"courseid":courseid,
	};

	$.ajax({
		type : "POST", //要插入数据，所以是POST协议 
		url : "/teacher/talk/course/", //注意结尾的斜线，否则会出现500错误
		data : post_data, //JSON数据
		// data:"name=" + event,
		success: function(mydata){

			var printmes = "";
			for(var k = 1; k < mydata["num"]+1;k++)
			{
				printmes = printmes + '<table width="100%" border="0" cellspacing="0" cellpadding="0"'+
									  '<tr><td width="10%" height="21"><div align="center"><font size="2">'+k+
									  '</font></div></td><td width="50%" height="21"><div align="left" title ='+mydata["message"][k-1]+
									  '><font size="2"><img src="/static/img/arrow.gif" width="8" height="7">'+mydata["message"][k-1]+
									  '</font></div></td><td width="15%" height="21"><div align="center"><font'+'size="2">'+mydata["name"][k-1]+
									  '</font></div></td><td width="25%" height="21"><div align="center"><font'+'size="2">'+mydata["time"][0]+
									  '</font></div></td></tr></table>'+
									  '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr>'+
									  '<td width="10%" height="1" background="/static/img/dotted_line.gif">'+
									  '<div align="center"><img src="/static/img/dotted_line.gif" width="600" height="1"></div>'+
									  '</td></tr></table>';
									  
			}
			document.getElementById('test').innerHTML = printmes

		},
	});
	setTimeout("Showmessage()",1000);
}
function SendMess()//发送消息
{
	var course = document.getElementsByName("selectcourse");
	for(var i =0; i < course.length;i++)
	{
		if(course[i].checked == true)
			courseid = course[i].value;
	}
	var text = document.getElementById('messtostu').value;
	var post_data ={
	"courseid":courseid,
	"message":text,
	};
	
	$.ajax({
		type : "POST", //要插入数据，所以是POST协议 
		url : "/teacher/talk/sendmess/", //注意结尾的斜线，否则会出现500错误
		data : post_data, //JSON数据
		success: function(mydata){
			document.getElementById('messtostu').value = "";
		},
	});
}