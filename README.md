# WebAutog

* 团队名称:一棵树有条河    
    
* 项目名:WebAutog 
* 项目介绍：使用python+taichi 实现一个简单的浏览器内核；能够解析html+css，实现简单的布局、渲染；以及页面元素的交互事件绑定等；   
* 目前已实现内容： html+css的解析，css选择器规则匹配等;block布局，及border，background-color样式的渲染；python文件作为script标签的src动态导入；
* 准备比赛中实现的内容：RenderTree的重排、重绘机制；inline布局，文字渲染，input标签渲染(尝试)，canvas标签；事件处理机制--键盘事件(特别是input的输入)，元素事件相关(解析绑定的鼠标事件：点击，hover)；次一级目标：定位（css的position属性），float布局等
* 其它：使用的第三方包：numpy、cssutils、freetype、HTMLParser