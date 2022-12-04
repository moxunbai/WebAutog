# WebAutog

* 团队名称:一棵树有条河    
    
* 项目名:WebAutog 
* 项目介绍：使用python+taichi 实现一个简单的浏览器内核；能够解析html+css，实现简单的布局、渲染；以及页面元素的交互事件绑定等； 
* 灵感来源：虽然项目是在这次活动第一次直播宣讲后确定的，但是相关的想法以前就有，之前是想如何把太极的程序在一个浏览器的工具上跑起来，比如Electron之类的；浏览器的框架更善于做GUI的应用，而taichi更擅长高性能计算，GPU并行等；虽然太极也有一套GUI的API，但都是偏低层的，复杂的布局UI和交互就会很吃力；然后我本人这两年也主要在做web前端工作，趁这次比赛也深入了解学习一下浏览器的布局渲染、事件管理等深层的原理；
* 应用设想(期望达到的效果)：基于此项目，能够快速的使用html+css+python script 实现自己的好看的，交互丰富的GUI应用；并能和自己的太极程序轻松顺滑的整合，丰富自己太极程序的交互以及调试；  
* 浏览器概要：一个浏览器内核最基本的功能需要，解析html+css语法；并生成DOM树，Render树；以实现页面元素的布局、渲染；还要能支持页面元素的事件交互，如鼠标hover、点击、键盘输入等；对于交互后修改了页面元素样式后，还要触发页面的重排、重绘等；另外如果想要在此框架下将一个单独的taichi程序渲染的结果展示到页面中，还需要实现相应的canvas元素，来负责taichi的渲染输出；
* 实现方案：html+css的解析不是本次重点，直接先用第三方库实现；浏览器的布局算法相关的css样式有很多，比如display、position、float、flex等，此次先只优先实现display:block/inline 布局；渲染算法是易于并行化的，此次渲染部分使用taichi kernel来做，布局算法暂时还是在python作用域；另外和渲染相关的css样式中，优先实现border，background，文字相关等；对于页面脚本(script标签)，和真正的浏览器不同用js实现的，那这里天然就用python做页面脚本；
* 目前已实现内容： html+css的解析，css选择器规则匹配等;block布局，及border，background-color样式的渲染；python文件作为script标签的src动态导入；
* 难点：1、数据的组织，模版文件解析后生成的渲染树、布局数据、渲染样式数据、字体数据等如何对应组织写入taichi field(交互过程中以上数据要增删改);2、布局；inline布局及文字排版难道了，放弃；3、文字渲染，此次实现了ttf格式字体文件的渲染，最开始想解析ttf文件后，在kernel中画轮廓并填充，后面感觉太花时间，降级为在python作用于用freetype画好位图，传给kennel渲染；4、事件管理，将taichi GUI的event解析为类浏览器的一套API，模版脚本的动态导入绑定等
* 准备比赛中实现的内容：RenderTree的重排、重绘机制；文字渲染，float布局，canvas标签；事件处理机制，元素事件相关(解析绑定的鼠标事件：点击，hover)；
* 其它：使用的第三方包：numpy、cssutils、freetype、HTMLParser

# 运行步骤
## 安装依赖
*  pip install -r requirements.txt
## 运行DEMO
* python main 01.html
* python main 02.html