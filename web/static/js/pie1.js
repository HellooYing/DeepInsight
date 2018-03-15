$.ajax({
    async: false,
    url:"/pie",
    success:function(result){
    Window.name1=result.name1
    Window.name2=result.name2
    Window.name3=result.name3
    Window.name4=result.name4
    Window.name5=result.name5
    Window.name6=result.name6
    Window.vue1=result.vue1
    Window.vue2=result.vue2
    Window.vue3=result.vue3
    Window.vue4=result.vue4
    Window.vue5=result.vue5
    Window.vue6=result.vue6
    }});
var myecharts=echarts.init(document.getElementById("pie1"));
option = {
    title : {
        text: '科室',
        subtext: ' ',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    // legend: {
    //     orient: 'vertical',
    //     left: 'left',
    //     data: [Window.name1,Window.name2,Window.name3,Window.name4,Window.name5,Window.name6]
    // },
    series : [
        {
            name: '科室',
            type: 'pie',
            radius : '75%',
            center: ['50%', '60%'],
            data:[
            {value:Window.vue1, name:Window.name1},
            {value:Window.vue2, name:Window.name2},
            {value:Window.vue3, name:Window.name3},
            {value:Window.vue4, name:Window.name4},
            {value:Window.vue5, name:Window.name5},
            {value:Window.vue6, name:Window.name6}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
myecharts.setOption(option);