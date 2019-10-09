var chart = Highcharts.chart('container',{
	chart: {
		// type: 'column'//图表类型 默认折线图，可以把这个改其他参数观察变化
		type: 'line'//图表类型 默认折线图，可以把这个改其他参数观察变化
		//这里可以设置回调函数完成后执行
	},

	title: {
		text: '月平均降雨量'
	},
	// subtitle: {
	// 	text: '数据来源: WorldClimate.com'
	// },
	xAxis: {
		categories: [//分类
			'一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'
		],
		crosshair: true//配置跟随鼠标或鼠标滑过点时的十字准星线
	},
	yAxis: {
		min: 0,
		title: {
			text: '降雨量 (mm)'
		}
	},/*数据提示框指的当鼠标悬停在某点上时，以框的形式提示该点的数据，比如该点的值，数据单位等。数据提示框内提示的信息完全可以通过格式化函数动态指定；通过设置 tooltip.enabled = false 即可不启用提示框。
	教程地址：https://www.hcharts.cn/docs/basic-tooltip*/
	tooltip: {
		// head + 每个 point + footer 拼接成完整的 table
		headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
		pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
		'<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
		footerFormat: '</table>',
		shared: true,
		useHTML: true
	},
	credits: {
		enabled: false,                    // 默认值，如果想去掉版权信息，设置为false即可
		text: 'www.hcharts.cn',             // 显示的文字
		href: 'http://www.hcharts.cn',      // 链接地址
		// position: {                         // 位置设置
		// 	align: 'left',
		// 	x: 400,
		// 	verticalAlign: 'bottom',
		// 	y: -100
		// },
		// style: {                            // 样式设置
		// 	cursor: 'pointer',
		// 	color: 'red',
		// 	fontSize: '30px'
		// }
	},
	/*
	数据列配置是针对所有数据列及某种数据列有效的通用配置。

	数据列的配置有三个级别：

	配置在 plotOptions.series，针对所有图表类型有效
	配置在 plotOptions.<数据列类型>，针对某种数据列有效
	配置在 series，针对某个数据列有效
	上述三个级别的配置精准度越来越高，也就是越精准的配置会覆盖前面的配置
	*/
	plotOptions: {
		column: {
			borderWidth: 0
		}
	},
	series: [{
		name: '东京',
		data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
	}, {
		name: '纽约',
		data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
	}, {
		name: '伦敦',
		data: [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6, 52.4, 65.2, 59.3, 51.2]
	}, {
		name: '柏林',
		data: [42.4, 33.2, 34.5, 39.7, 52.6, 75.5, 57.4, 60.4, 47.6, 39.1, 46.8, 51.1]
	}]
});