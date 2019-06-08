# bootstrap笔记
 - 	<script type="text/javascript" src="{% static 'jquery-1.12.4.min.js' %}"></script>
 - <script type="text/javascript" src="{% static 'bootstrap-3.3.7/js/bootstrap.min.js' %}"></script>
 - 注意：
 	- `JQuery`的引用一定要在`Js`之前，这是一种依赖关系
 
 - 折叠插件（`collapse`）
 	- bootstrap的collapse默认折叠
 	
 - li 标签的 `active` 显示当前位置
 
 - 设计全局样式的CSS
 	`*{}`

 - CSS 选择器
 	- `div.blog:not(:last-child){}`不给最后一个class为blog的div添加样式

 - 首行缩进
 	- `text-indent:2em;`

 - 修改列表的样式（左边的那个点）
 	- `list-style-type:none;` (none为不显示)

 - `display：inline-block；`可以让元素具有块级元素和行内元素的特性：既可以设置长宽，可以让padding和margin生效，又可以和其他行内元素并排。是一个很实用的属性

 - 块级元素和行内元素区别
  	- 块级元素独自占一行且宽度会占满父元素宽度，行内元素不会独占一行，相邻行内元素可以排在同一行

 - 常见块级元素：div p form ul ol li 等；
 - 常见的行内元素：span strong em;
 
 - css的`overflow`属性
 	- 定义：overflow 属性规定了当内容溢出元素框时候发生的事情
 	- 常用属性：`overflow: scorll;` 
 	- `http://www.w3school.com.cn/tiy/t.asp?f=csse_overflow`

