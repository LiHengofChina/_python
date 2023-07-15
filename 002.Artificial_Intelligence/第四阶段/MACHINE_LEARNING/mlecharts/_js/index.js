DIRS = {}
CURRDIR = []
BASEURL_STRING = ""

$(document).ready(function(){
	// 加载dirs.json
	$.getJSON('js/dirs.json?k='+Math.random(), function(data){
		DIRS = data
		// 加载json文件, 生成目录结构
		generator_breads()
		// 根据当前路径, 加载文件夹中的目录结构
		generator_files()
	})
})

/**
 * 生成 breads titles  
 * @param {Object} fulldir  
 * 		Documents,empty
 */

function generator_breads(fulldir){
	if(!fulldir){	// 并未传递目录路径, 把当前目录改为根目录, 加载当前目录
		CURRDIR = []
	}else{  	//传递了目录路径, 加载CURRDIR, 修改目录路径, 更新当前目录
		CURRDIR = fulldir.split(',')
	}
	//更新面包屑导航内容
	$(".breadcrumb").empty('')
	$(".breadcrumb").append('<li class="breadcrumb-item"><a href="javascript:cdroot()"> HOME </a></li>')
	titlepath = ''
	for(i=0; i<CURRDIR.length; i++){
		titlepath += titlepath ? ","+CURRDIR[i] : CURRDIR[i]
		$(".breadcrumb").append('<li class="breadcrumb-item"><a href="javascript:cdroot(\'' + titlepath + '\')">'+CURRDIR[i]+'</a></li>')
	}
}

// 根据当前路径位置, 更新文件列表, 按照文件夹-文件排序
function generator_files() {
	if (CURRDIR.length <= 0){ // 加载根目录内容
		BASEURL_STRING = "DIRS"
		renderlist()
	}else{ // 不是根目录, 根据当前路径加载子目录内容
		BASEURL_STRING = 'DIRS[\'' + CURRDIR.join('\'][\'') + '\']'
		renderlist()
	}
}

// 渲染文件及文件夹列表
function renderlist(){
	subfiles = Object.keys(eval(BASEURL_STRING))
	// 对子文件及文件夹排序, 先按类型排序(先显示文件夹,再显示文件), 类型相同再按名称排序
	subfiles = subfiles.sort(function(a, b){
		// 通过字符串, 获取文件类型
		atype = eval("(" + BASEURL_STRING + "['" + a + "'])")
		btype = eval("(" + BASEURL_STRING + "['" + b + "'])")
		if (typeof(atype) == typeof(btype)){	//二者类型相同,比较文件名
			return a.localeCompare(b)
		} else {   //二者类型不相同,文件夹在前
			return typeof(atype) == 'object' ? -1 : 1
		}
	})
	// 按照已经排序的subfiles, 更新页面元素
	$(".list-group").empty('')
	subfiles.forEach(function (filename) {
		// 判断当前目录是文件还是文件夹
		direc = eval("(" + BASEURL_STRING + "['" + filename + "'])")
		if (typeof(direc) == 'object'){
			$(".list-group").append(template_dir(filename))
		}else{
			$(".list-group").append(template_file(filename))
		}
	})
}

// 从根目录进入文件夹, 更新界面
function cdroot(rootpath){
	if (rootpath){
		generator_breads(rootpath)
	}else{
		generator_breads()
	}
	generator_files()
}

// 处理点击某个文件夹事件  进入文件夹, 更新界面
function cd(filename){
	CURRDIR.push(filename)
	generator_breads(CURRDIR.join(','))
	generator_files()
}



// 处理点击某个文件事件  下载文件
function download(filename){
	base = CURRDIR.length == 0 ? '/static' : '/static/'
	download_url = base + CURRDIR.join('/') + '/' + filename
	window.open(download_url)	
}


// 定义html文件夹列表模板
function template_dir(filename){
	return '<li class="list-group-item">' + 
		   '	<span class="glyphicon glyphicon-level-up" aria-hidden="true"></span>' + 
		   '	<a href="javascript:cd(\'' + filename + '\')">' + filename + '</a>' + 
		   '</li>'
}

// 定义html文件列表模板
function template_file(filename){
	return '<li class="list-group-item">' + 
		   '	<span class="glyphicon glyphicon-save-file" aria-hidden="true"></span>' + 
		   '	<a href="javascript:download(\'' + filename + '\')">' + filename + '</a>' + 
		   '</li>'
}