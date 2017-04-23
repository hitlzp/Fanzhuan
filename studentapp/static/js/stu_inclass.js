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
			document.getElementById("m").innerHTML = m;
			document.getElementById("s").innerHTML = s;
			command();
			document.getElementById("courseset").disabled= true;
		},
	// dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
	// contentType : 'application/json',
	});
}

startbutton = 0; // 状态1
starttimebutton = 0; // 状态2
stoptimebutton = 0;
coutinuetimebutton = 0;
markbutton = 0;
nextsegbutton = 0
function command()
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
		url : "/student/command/", //注意结尾的斜线，否则会出现500错误
		data : post_data, //JSON数据
		success: function(mydata){
			if (mydata["command"][0] == "start0" && startbutton == 0)//教师第一次点击开始按钮
			{
				document.getElementById("cseg").style.display="none";//隐藏
				document.getElementById("cseg2").innerHTML = "环节:";
				document.getElementById("cseg3").innerHTML = 1;
				document.getElementById("m").innerHTML = mydata["segtime"][0];
				m = mydata["segtime"][0];
				document.getElementById("courseorseg").style.display="none";//隐藏
				document.getElementById("courseorseg2").style.display="";//显
				huanjie = document.getElementById("cseg3").innerText;
				document.getElementById("courserecommend").innerHTML = mydata["segintroduce"][huanjie - 1];
				startbutton = 1;
			}
			if (mydata["command"][0] == "start" && startbutton == 0)//教师非第一次点击开始按钮
			{
				startbutton = 1;
				markbutton = 0;
				document.getElementById("g2g").style.display="none";//隐藏
				document.getElementById("gig").style.display="none";//隐藏
				document.getElementById("self").style.display="none";//隐藏
			}
			
			if(
			mydata["command"][0] == "timestart" && starttimebutton == 0)//教师点击计时按钮
			{
				starttimebutton = 1;
				run();
			}
			if(mydata["command"][0] == "timestop" && stoptimebutton == 0)//教师点击暂停按钮
			{
				stoptimebutton = 1;
				coutinuetimebutton = 0;
				doPause();
			}
			if(mydata["command"][0] == "timecontinue" && coutinuetimebutton == 0)//教师点击继续按钮
			{
				coutinuetimebutton = 1;
				stoptimebutton = 0;
				doGo();
			}
			if(mydata["command"][0] == "mark" && markbutton == 0)//教师点击评分按钮
			{
				nextsegbutton = 0;
				markbutton = 1;
				huanjie = document.getElementById("cseg3").innerText;
				
				
				var course = document.getElementsByName("selectcourse");
				
				for(var i =0; i < course.length;i++)
				{
					if(course[i].checked == true)
						courseid = course[i].value;
				}
				var post_data ={
				"courseid":courseid,
				"segment":huanjie,
				};

				$.ajax({
					type : "POST", //要插入数据，所以是POST协议 
					url : "/student/grades/", //注意结尾的斜线，否则会出现500错误
					data : post_data, //JSON数据
					success: function(mydata){
						var g2ggrade=new Array()
						g2ggrade[0] = mydata["groupnum"];
						for(var t = 1; t < mydata["groupnum"] + 1; t++)//初始化数组为0
						{
							g2ggrade[t] = 0;
						}
						
						var giggrade=new Array()
						giggrade[0] = mydata["groupsum"] - 1;
						for(var t = 1; t < mydata["groupsum"] + 1; t++)//初始化数组为0
						{
							giggrade[t] = 0;
						}
						
						var selfgrade= 0;
						
						if (mydata["choice"][2] != 0)//组间互评
						{
							document.getElementById("g2g").style.display="";//显
							document.getElementById("commitgrade").style.display="";//显
							
							var tableObj = document.getElementById('g2gmess');  
							var rowNums = tableObj.rows.length;
							var length = tableObj.rows.length
							for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
							{
								document.getElementById('g2gmess').deleteRow(1);
							}
							
							for(var k = 1; k < mydata["groupnum"] + 1;k++)
							{
								if (mydata["mygroup"] == k)
								{
									continue;
								}
								var tableObj = document.getElementById('g2gmess');  
								var rowNums = tableObj.rows.length;
								var rowObj = tableObj.insertRow(rowNums);  //添加一行 
								
								var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
								cellObj0.innerHTML = k;  
								
								var theid = 'g2g_input' + k.toString();
								rowObj.insertCell().innerHTML = '<input type="number" min = 0 max = 100 value = 0 id= "'+theid+ '" style="width:90px;border-width:0px;text-align:center;border-style:none">';
							}
						}
						if (mydata["choice"][3] != 0)//组内互评
						{
							document.getElementById("gig").style.display="";//显
							document.getElementById("commitgrade").style.display="";//显
							
							var tableObj = document.getElementById('gigmess');  
							var rowNums = tableObj.rows.length;
							var length = tableObj.rows.length
							for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
							{
								document.getElementById('gigmess').deleteRow(1);
							}
							for(var k = 1; k < mydata["groupsum"] + 1;k++)
							{
								if (mydata["idingroup"][mydata["mygroup"]-1][k-1] == mydata["stuid"])
								{
									continue;
								}
								var tableObj = document.getElementById('gigmess');  
								var rowNums = tableObj.rows.length;
								var rowObj = tableObj.insertRow(rowNums);  //添加一行 
								
								var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
								cellObj0.innerHTML = mydata["idingroup"][mydata["mygroup"]-1][k-1];  
								
								var cellObj1 = rowObj.insertCell(1);  //添加第一个单元格及其信息  
								cellObj1.innerHTML = mydata["nameingroup"][mydata["mygroup"]-1][k-1];  
								
								var theid = 'gig_input' + k.toString();
								rowObj.insertCell().innerHTML = '<input type="number" min = 0 max = 100 value = 0 id= "'+theid+ '" style="width:65px;border-width:0px;text-align:center;border-style:none">';
							}
						}
						if (mydata["choice"][4] != 0)//自评
						{
							document.getElementById("self").style.display="";//显
							document.getElementById("commitgrade").style.display="";//显
							
							var tableObj = document.getElementById('selfmess');  
							var rowNums = tableObj.rows.length;
							var length = tableObj.rows.length
							for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
							{
								document.getElementById('selfmess').deleteRow(1);
							}

							var tableObj = document.getElementById('selfmess');  
							var rowNums = tableObj.rows.length;
							var rowObj = tableObj.insertRow(rowNums);  //添加一行 
								
							var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
							cellObj0.innerHTML = mydata["stuid"];  
								
							var cellObj1 = rowObj.insertCell(1);  //添加第一个单元格及其信息  
							cellObj1.innerHTML = mydata["stuname"];  
								
							var theid = 'self_input';
							rowObj.insertCell().innerHTML = '<input type="number" min = 0 max = 100 value = 0 id= "'+theid+ '" style="width:65px;border-width:0px;text-align:center;border-style:none">';

						}	
						
					document.onclick=function()//当教师点击提交按钮
					{ 
					var obj = event.srcElement;//这里火狐会报错
						if(obj.type == "button"){
							if(obj.id == "commitgrade"){
								if(mydata["choice"][2] != 0)
								{
									for(var w = 1; w < mydata["groupnum"] + 1;w++)
									{
										if(mydata["mygroup"] == w)
										{
											g2ggrade[w] = 0;
										}
										else{
										g2ggrade[w] = document.getElementById("g2g_input"+w.toString()).value;}
									}
								}
								
								if(mydata["choice"][3] != 0)
								{
									for(var w = 1; w < mydata["groupsum"]+1;w++)
									{
										if(mydata["idingroup"][mydata["mygroup"]-1][w-1] == mydata["stuid"])
										{
											giggrade[w] = 0;
										}
										else{
										giggrade[w] = document.getElementById("gig_input"+w.toString()).value;}
									}
								}
								if(mydata["choice"][4] != 0)
								{
									selfgrade = document.getElementById("self_input").value;
									document.getElementById("commitgrade").disabled= true;
								}
								
								var post_data2 ={
									"g2ggrade":g2ggrade,
									"giggrade":giggrade,
									"selfgrade":selfgrade,
									"segment":huanjie,
									"courseid":courseid,
									"stugroup":mydata["mygroup"],
									"groupsum":mydata["groupsum"],
									};
									$.ajax({
									  type : "POST", //要插入数据，所以是POST协议 
									  url : "/student/savegrade/", //注意结尾的斜线，否则会出现500错误
									  traditional:true,  //加上此项可以传数组
									  data : post_data2, //JSON数据
									  success: function(mydata3){
									  },
									});
								document.getElementById("close").click();
							}
						}
					}

					},
				});
				document.getElementById("mark").click();
			}
			if(mydata["command"][0] == "nextseg" && nextsegbutton == 0)//教师点击下一环节
			{
				nextsegbutton  = 1;
				startbutton = 0;
				document.getElementById("cseg3").innerHTML++;
				huanjie = document.getElementById("cseg3").innerText;
				document.getElementById("courserecommend").innerHTML = mydata["segintroduce"][huanjie - 1];
				document.getElementById("commitgrade").disabled= false;
			}
			if(mydata["command"][0] == "over")//课程结束
			{
				alert("课程结束！");
			}
			
			
		},
	});
	setTimeout("command()",1000); 
}

var m = 0;
var s = 0;
var mytime=null;  
//开始倒计时 
function run(){  
                //输出
                document.getElementById('m').innerHTML = m;
				document.getElementById('s').innerHTML = s;;  
                s--;  
                if(s<0){  
                    s=59;  
                    m--;  
                    if(m<0){  
                        alert('时间到！');  
                            return;  
                    }  
                }  
                mytime = setTimeout("run()",1000);  
            } 
//暂停  
function doPause(){  
                if(mytime!=null){  
                    clearTimeout(mytime);  
                    mytime=null;  
                }  
            } 

            //继续  
function doGo(){  
                run();   
            }			