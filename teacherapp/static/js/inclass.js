function selectcourse()//下拉栏选择课程
		{
			   //需要实现控制可以加if() while()实现
			var t = document.getElementById("selectcourse");   
			var selectValue=t.options[t.selectedIndex].value;//获取select的值
			  //alert(selectValue);
			
			document.getElementById("sid").disabled= false;
			document.getElementById("randzu").disabled= false;
			
			
			var post_data ={
			"name":selectValue,
			};
			
			$.ajax({
			  type : "POST", //要插入数据，所以是POST协议 
			  url : "/teacher/classajax/", //注意结尾的斜线，否则会出现500错误
			  data : post_data, //JSON数据
			  // data:"name=" + event,
			  success: function(mydata){
				document.getElementById("a").innerHTML = mydata["coursemess"];
				Showtable(mydata)
				document.getElementById("thenext").innerHTML= 1;
				document.getElementById("m").innerHTML = mydata["segment"][1][1];
				document.getElementById("s").innerHTML = 0;
				m = mydata["segment"][1][1];
				s = 0;
			  },
			  // dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
			  // contentType : 'application/json',
			});
			
		}
		
		function Showtable(mydata)//打印学生列表
		{
			var row0 = document.getElementById('mytable').rows[0];  //给第一行换背景  
				row0.className = 'title'; 
				var tableObj = document.getElementById('mytable');  
				var rowNums = tableObj.rows.length;

				var length = tableObj.rows.length
				for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
				{
					document.getElementById('mytable').deleteRow(1);
				}
				
				for(var k = 0; k < mydata["stuname"].length;k++)
				{
					var tableObj = document.getElementById('mytable');  
				    var rowNums = tableObj.rows.length;
					var rowObj = tableObj.insertRow(rowNums);  //添加一行 
					
					var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
				    cellObj0.innerHTML = mydata["stuname"][k];  
					  
				    var cellObj1 = rowObj.insertCell(1);  //添加第二个单元格及其信息  
				    cellObj1.className = 'center';  
				    cellObj1.innerHTML = mydata["stugroup"][k]; 
						
					var cellObj2 = rowObj.insertCell(2);  //添加第三个单元格及其信息  
				    cellObj2.className = 'center';  
				    cellObj2.innerHTML = mydata["stugrade"][k]; 

				}
		}
		
		function Fenzu()//点击分组按钮分组
		{		
			var t = document.getElementById("selectcourse");   
			var selectValue=t.options[t.selectedIndex].value;//获取select的值
			var post_data ={
			"name":selectValue,
			};
			
			$.ajax({
			  type : "POST", //要插入数据，所以是POST协议 
			  url : "/teacher/fenzu/", //注意结尾的斜线，否则会出现500错误
			  data : post_data, //JSON数据
			  success: function(mydata){
				  Showtable(mydata);
				  
				  
			  },
			});
		}
		
		function Randstu()//随机选择学生
		{		
			var t = document.getElementById("selectcourse");   
			var selectValue=t.options[t.selectedIndex].value;//获取select的值
			var post_data ={
			"name":selectValue,
			};
			
			$.ajax({
			  type : "POST", //要插入数据，所以是POST协议 
			  url : "/teacher/randstu/", //注意结尾的斜线，否则会出现500错误
			  data : post_data, //JSON数据
			  success: function(mydata){
				  alert(mydata["cstu"]);
			  },
			});
		}
		
		function Randgroup()//随机选择小组
		{		
			var t = document.getElementById("selectcourse");   
			var selectValue=t.options[t.selectedIndex].value;//获取select的值
			var post_data ={
			"name":selectValue,
			};
			
			$.ajax({
			  type : "POST", //要插入数据，所以是POST协议 
			  url : "/teacher/randgroup/", //注意结尾的斜线，否则会出现500错误
			  data : post_data, //JSON数据
			  success: function(mydata){
				  alert(mydata["czu"]);
				  
				  
			  },
			});
		}
		
		function Nextseg()
		{
			document.getElementById("thenext").innerHTML++;
			document.getElementById("sid").disabled=false; 
			
			var t = document.getElementById("selectcourse");   
			var selectValue=t.options[t.selectedIndex].value;//获取select的值
			seg = document.getElementById("thenext").innerText;//获取当前环节数
				
			var post_data ={
			"name":selectValue,
			"seg":seg - 1,
			};
			$.ajax({
				 type : "POST", //要插入数据，所以是POST协议 
				url : "/teacher/nextsegment/", //注意结尾的斜线，否则会出现500错误
				traditional:true,  //加上此项可以传数组
				data : post_data, //JSON数据
				// data:"name=" + event,
				success: function(mydata){
					clearInterval(mytime)
					mytime=null;
					document.getElementById("m").innerHTML = mydata["time"];
					document.getElementById("s").innerHTML = 0;
					m = mydata["time"];
					s = 0;
					document.getElementById("nextseg").disabled=true;
				},
				// dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
				// contentType : 'application/json',
			});
			
			var post_data2 ={
			"command":"nextseg",
			"courseid":selectValue,
			};
			$.ajax({
				type : "POST", //要插入数据，所以是POST协议 
				url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
				data : post_data2, //JSON数据
				success: function(mydata3){
				},
				});
		}
		
		
		
		function showName(){  
		var index = Math.floor(Math.random()*mydata.length);  
		var name = mydata[index];  
		document.getElementById("showView").innerHTML = name;  
		idd=setTimeout("showName()",50);  
		}  
		var state = true;  
		var idd; 
		function sssss(){ 

			if(state){  
				showName();  
				state = false;  
			}  
			else{  
				clearTimeout(idd);  
				state = true;  
			}  
				  
		} 

		
		//倒计时
			var m = 0;
			var s = 0;
			//var m= document.getElementById("m").innerText;

            var mytime=null;  
            //开始倒计时  
            function doSubmit(){
				document.getElementById("randzu").disabled= true;
				document.getElementById("selectcourse").disabled= true;
				document.getElementById("stid").disabled= false;
				document.getElementById("sid").disabled=true; 
				document.getElementById("ping").disabled=false;
				document.getElementById("randstu").disabled=false;  	
				document.getElementById("randgroup").disabled=false;  
				
				var t = document.getElementById("selectcourse");   
				var selectValue=t.options[t.selectedIndex].value;//获取select的值
				seg = document.getElementById("thenext").innerText;//获取当前环节数
				
				var post_data ={
				"name":selectValue,
				"seg":seg,
				};
				$.ajax({
					 type : "POST", //要插入数据，所以是POST协议 
					url : "/teacher/startcourse/", //注意结尾的斜线，否则会出现500错误
					traditional:true,  //加上此项可以传数组
					data : post_data, //JSON数据
					// data:"name=" + event,
					success: function(mydata3){

					},
					// dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
					// contentType : 'application/json',
					});
                return false;  
            }  
			
			
			function timestart()
			{
				document.getElementById("stid").disabled=true;  
                document.getElementById("tid").disabled=false;  
                document.getElementById("gid").disabled=true;
				run(); 
				var t = document.getElementById("selectcourse");   
				var selectValue=t.options[t.selectedIndex].value;//获取select的值
				var post_data ={
				"command":"timestart",
				"courseid":selectValue,
				};
				$.ajax({
					type : "POST", //要插入数据，所以是POST协议 
					url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
					data : post_data, //JSON数据
					success: function(mydata3){
					},
					});
			}
              
            //执行倒计时  
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
                document.getElementById("tid").disabled=true;  
                document.getElementById("gid").disabled=false;  
				var t = document.getElementById("selectcourse");   
				var selectValue=t.options[t.selectedIndex].value;//获取select的值
				var post_data ={
				"command":"timestop",
				"courseid":selectValue,
				};
				$.ajax({
					type : "POST", //要插入数据，所以是POST协议 
					url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
					data : post_data, //JSON数据
					success: function(mydata3){
					},
					});
            }  
              
            //继续  
            function doGo(){  
                run();  
                document.getElementById("tid").disabled=false;  
                document.getElementById("gid").disabled=true;
				var t = document.getElementById("selectcourse");   
				var selectValue=t.options[t.selectedIndex].value;//获取select的值
				var post_data ={
				"command":"timecontinue",
				"courseid":selectValue,
				};
				$.ajax({
					type : "POST", //要插入数据，所以是POST协议 
					url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
					data : post_data, //JSON数据
					success: function(mydata3){
					},
					});	
					
            }
			
			function Grade()//评分
			{
				   //需要实现控制可以加if() while()实现
				var t = document.getElementById("selectcourse");   
				var selectValue=t.options[t.selectedIndex].value;//获取select的值
				//alert(selectValue);
				
				document.getElementById("randzu").disabled= true;
				document.getElementById("selectcourse").disabled= true;
				document.getElementById("commitgrade").disabled= false;

				document.getElementById("t2sb").disabled= false;
				document.getElementById("t2gb").disabled= false;
				
				var post_data ={
				"name":selectValue,
				};
				
				var post_data2 ={
				"command":"mark",
				"courseid":selectValue,
				};
				$.ajax({
					type : "POST", //要插入数据，所以是POST协议 
					url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
					data : post_data2, //JSON数据
					success: function(mydata3){
					},
					});	
				
				
				
				$.ajax({
				  type : "POST", //要插入数据，所以是POST协议 
				  url : "/teacher/gradeteacher/", //注意结尾的斜线，否则会出现500错误
				  data : post_data, //JSON数据
				  // data:"name=" + event,
				  success: function(mydata){
					document.getElementById("stumess").style.display="none";//隐藏
					document.getElementById("ping").disabled=true;
					
					seg = document.getElementById("thenext").innerText;//获取当前环节数
					
					var thegrade=new Array()
					for(var t = 1; t < mydata["course"][0] / mydata["course"][1] + 1; t++)//初始化数组为0
					{
						thegrade[t] = 0;
					}
					thegrade[0] = mydata["course"][0] / mydata["course"][1];
					var thegrade2=new Array()
					for(var t = 1; t < mydata["course"][0] + 1; t++)//初始化数组为0
					{
						thegrade2[t] = 0;
					}
					thegrade2[0] = mydata["course"][0];
					if(mydata["segment"][seg - 1][3][0] != 0)//这个if处理教师对小组的评价，成绩结果由thegrade返回，thegrade = [小组数，组1， 组2， 。。。。]
					{
						//alert("教师评价小组");
						document.getElementById("t2g").style.display="";//显
						
						var tableObj = document.getElementById('t2gmess');  
						var rowNums = tableObj.rows.length;
						var length = tableObj.rows.length
						for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
						{
							document.getElementById('t2gmess').deleteRow(1);
						}
						
						
						for(var k = 1; k < mydata["course"][0] / mydata["course"][1] + 1;k++)
						{
							var tableObj = document.getElementById('t2gmess');  
							var rowNums = tableObj.rows.length;
							var rowObj = tableObj.insertRow(rowNums);  //添加一行 
							
							var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
							cellObj0.innerHTML = k;  
							
							var theid = 't2g_input' + k.toString();
							rowObj.insertCell().innerHTML = '<input type="number" min = 0 max = 100 value = 0 id= "'+theid+ '" style="width:120px;border-width:0px;text-align:center;border-style:none">';
						}
					}
					
					
					if(mydata["segment"][seg - 1][3][1] != 0)//这个if处理教师对每位学生的评价，成绩结果由thegrade2返回，thegrade = [学生数，学生1成绩， 
					{										//学生2成绩， 。。。。]
						//alert("教师评价每位学生");
						document.getElementById("t2s").style.display="";//显
	
						var tableObj = document.getElementById('t2smess');  
						var rowNums = tableObj.rows.length;
						var length = tableObj.rows.length
						for(var i = 1; i < length;i++)//切换课程时清除之前打印的表
						{
							document.getElementById('t2smess').deleteRow(1);
						}
						
						
						for(var k = 1; k < mydata["course"][0] + 1;k++)
						{
							var tableObj = document.getElementById('t2smess');  
							var rowNums = tableObj.rows.length;
							var rowObj = tableObj.insertRow(rowNums);  //添加一行 
							
							var cellObj0 = rowObj.insertCell(0);  //添加第一个单元格及其信息  
							cellObj0.innerHTML = k; 
							
							var cellObj1 = rowObj.insertCell(1);  //添加第二个单元格及其信息  
							cellObj1.innerHTML = mydata["stuname"][k-1];  
							
							var cellObj2 = rowObj.insertCell(2);  //添加第三个单元格及其信息  
							cellObj2.innerHTML = mydata["stugroup"][k-1];  
							
							var theid = 't2s_input' + k.toString();
							rowObj.insertCell().innerHTML = '<input type="number" min = 0 max = 100 value = 0 id= "'+theid+ '" style="width:60px;border-width:0px;text-align:center;border-style:none">';
						}
						
						
					}
					
					//event.srcElement ? event.srcElement : event.target;
					document.onclick=function()//当教师点击提交按钮
					{ 
					var obj = event.srcElement;//这里火狐会报错
						if(obj.type == "button"){
							if(obj.id == "t2gb"){
								for(var w = 1; w < mydata["course"][0] / mydata["course"][1] + 1;w++)
								{
									thegrade[w] = document.getElementById("t2g_input"+w.toString()).value;
								}
								document.getElementById("t2gb").disabled= true;
								
							}
							if(obj.id == "t2sb"){
								for(var w = 1; w < mydata["course"][0] + 1;w++)
								{
									thegrade2[w] = document.getElementById("t2s_input"+w.toString()).value;
								}
								document.getElementById("t2sb").disabled= true;
								
							}
							if(obj.id == "commitgrade"){
								document.getElementById("commitgrade").disabled= true;
								var post_data ={
								"grade1":thegrade,
								"grade2":thegrade2,
								"courseid":selectValue,//课程id
								"segnum":seg-1,//环节编号，seg-1从0开始
								};
								alert(thegrade);
								alert(thegrade2);
								$.ajax({
								  type : "POST", //要插入数据，所以是POST协议 
								  url : "/teacher/gradefromteacher/", //注意结尾的斜线，否则会出现500错误
								  traditional:true,  //加上此项可以传数组
								  data : post_data, //JSON数据
								  // data:"name=" + event,
								  success: function(mydata3){
									Showtable(mydata3)
									document.getElementById("nextseg").disabled= false;
									if(mydata3["state"] == 1)
									{
										alert("课程结束!");
										
										var post_data ={
										"command":"over",
										"courseid":selectValue,
										};
										$.ajax({
											type : "POST", //要插入数据，所以是POST协议 
											url : "/teacher/command/", //注意结尾的斜线，否则会出现500错误
											data : post_data, //JSON数据
											success: function(mydata3){
											},
											});	
										document.getElementById("nextseg").disabled=true;
										document.getElementById("sid").disabled=true;
									}
								  },
								  // dataType : 'json', //在ie浏览器下我没有加dataTpye结果报错，所以建议加上
								  // contentType : 'application/json',
								});
								document.getElementById("stumess").style.display="";//显
								document.getElementById("t2s").style.display="none";//隐藏
								document.getElementById("t2g").style.display="none";//隐藏
							}
						}
					}
					
					
					if(mydata["segment"][seg - 1][3][0] == 0 && mydata["segment"][seg - 1][3][1] == 0)//教师不参与本环节评价
					{
						document.getElementById("remind").style.display="";//显
					}

				  },
				});
				
			}