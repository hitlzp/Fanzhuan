 $(function() {  
    start();
 });

function doSubmit()//选择将要参加的课程
{
	var course = document.getElementsByName("selectcourse");
	for(var i =0; i < course.length;i++)
	{
		if(course[i].checked == true)
			courseid = course[i].value;
	}
	var post_data ={
	"name":courseid,
	};

	$.ajax({
		type : "POST", //要插入数据，所以是POST协议 
		url : "/student/stuinclassajax/", //注意结尾的斜线，否则会出现500错误
		data : post_data, //JSON数据
		// data:"name=" + event,
		success: function(mydata){
			document.getElementById("cid").innerHTML = mydata["cname"];
			document.getElementById("courserecommend").innerHTML = mydata["courserecommend"];
			document.getElementById("m").innerHTML = 00;
			document.getElementById("s").innerHTML = 00;
		},
	// dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
	// contentType : 'application/json',
	});
}

function start()
{
	$.ajax({
		type : "POST", //要插入数据，所以是POST协议 
		url : "/teacher/startcourse/", //注意结尾的斜线，否则会出现500错误
		
		success: function(mydata){
			alert(mydata["yy"]);
		},
	// dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
	// contentType : 'application/json',
	});
	//setTimeout("start()",1000); 
}