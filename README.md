# WebAutog

* 团队名称:一棵树有条河    
    
* 项目名:WebAutog 
* 项目介绍：使用python+taichi 实现一个简单的浏览器内核；能够解析html+css，实现简单的布局、渲染；以及页面元素的交互事件绑定等； 
* 应用设想(期望达到的效果)：基于此项目，能够快速的使用html+css+python script 实现自己的好看的，交互丰富的GUI应用；并能和自己的太极程序轻松顺滑的整合，丰富自己太极程序的交互以及调试；  
* 浏览器概要：一个浏览器内核最基本的功能需要，解析html+css语法；并生成DOM 树，Render树；以实现页面元素的布局、渲染；还要能支持页面元素的事件交互，如鼠标hover、点击、键盘输入等；对于交互后修改了页面元素样式后，还要触发页面的重排、重绘等；另外如果想要在此框架下将一个单独的taichi程序渲染的结果展示到页面中，还需要实现相应的canvas元素，来负责taichi的渲染输出；
* 实现方案：html+css的解析不是本次重点，直接先用第三方库实现；浏览器的布局算法相关的css样式有很多，比如display、position、float、flex等，此次先只优先实现display:block/inline 布局；渲染算法是易于并行化的，此次渲染部分使用taichi kernel来做，布局算法暂时还是在python作用域；另外和渲染相关的css样式中，优先实现border，background，文字相关等；对于页面脚本(script标签)，和真正的浏览器不同用js实现的，那这里天然就用python做页面脚本；
* 目前已实现内容： html+css的解析，css选择器规则匹配等;block布局，及border，background-color样式的渲染；python文件作为script标签的src动态导入；
* 准备比赛中实现的内容：RenderTree的重排、重绘机制；inline布局，文字渲染，input标签渲染(尝试)，canvas标签；事件处理机制--键盘事件(特别是input的输入)，元素事件相关(解析绑定的鼠标事件：点击，hover)；次一级目标：定位（css的position属性），float布局等
* 其它：使用的第三方包：numpy、cssutils、freetype、HTMLParser