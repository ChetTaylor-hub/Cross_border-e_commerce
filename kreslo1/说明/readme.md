<!--
 * @Author: TaoChen 2575394301qq.com
 * @Date: 2024-01-25 14:36:27
 * @LastEditors: TaoChen 2575394301qq.com
 * @LastEditTime: 2024-01-25 14:37:56
 * @FilePath: \kreslo1\说明\readme.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

# 使用说明

软件界面如图，包含五个任务：

* 催促收货
* 催促填写护照
* 投诉跟卖
* 取消促销
* 更新库存

每个任务下包含如下按钮，并只对当前任务有效

* 按键：
  * 开始：开始任务
  * 停止：暂停，停止任务
  * 确认：确认参数
* 输入框：输入任务执行频率，单位 s
* 显示框：显示任务执行成功与否
* 其他

操作步骤：

1. 输入密匙信息
2. 在指定任务下输入发送间隔。单位 s
3. 在指定任务下点击 确认 按钮
4. 在指定任务下点击 开始 按钮

# log说明

运行程序时会自动生成log，存放在log文件夹下里面记录着一些信息和错误记录

* passport.log：提醒护照
* pickup.log：提醒收货
* complaint.log：跟卖投诉
* promotional.log：取消促销
* update.log：更新库存

# 注意事项

1. 如果你的验证界面是黑色的话，将verfy_picture/黑色.jpg改为verfy_picture/template.jpg
2. 如果你的验证界面是白色的话，将verfy_picture/白色.jpg改为verfy_picture/template.jpg
3. 更新库存前，需要网站下载下来的库存模板，命名为stock-update-template.xlsx（我把样例放在文件夹里面了），文件位置和软件放在同一文件夹下
