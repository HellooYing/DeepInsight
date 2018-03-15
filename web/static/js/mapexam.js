$.ajax({
    async: false,
    url:"/mapexam",
    success:function(result){
        Window.XZ=result.XZ;
    Window.SH=result.SH;
    Window.FJ=result.FJ;
    Window.GD=result.GD;
    Window.SX=result.SX;
    Window.YN=result.YN;
    Window.HAIN=result.HAIN;
    Window.LN=result.LN;
    Window.JL=result.JL;
    Window.JX=result.JX;
    Window.QH=result.QH;
    Window.NMG=result.NMG;
    Window.SHX=result.SHX;
    Window.CQ=result.CQ;
    Window.JS=result.JS;
    Window.BJ=result.BJ;
    Window.XJ=result.XJ;
    Window.ZJ=result.ZJ;
    Window.SD=result.SD;
    Window.GS=result.GS;
    Window.TJ=result.TJ;
    Window.HN=result.HN;
    Window.HLJ=result.HLJ;
    Window.HB=result.HB;
    Window.HUN=result.HUN;
    Window.AH=result.AH;
    Window.HUB=result.HUB;
    Window.SC=result.SC;
    Window.GZ=result.GZ;
    Window.GX=result.GX;
    Window.NX=result.NX;
    }});

    var myChart = echarts.init(document.getElementById('china-map'));
var data = [
    {name: '新疆', value: Window.XJ},
    {name: '浙江', value: Window.ZJ},
    {name: '山东', value: Window.SD},
    {name: '甘肃', value: Window.GS},
    {name: '天津', value: Window.TJ},
    {name: '河南', value: Window.HN},
    {name: '黑龙江', value:Window.HLJ},
    {name: '河北', value: Window.HB},
    {name: '湖南', value: Window.HUN},
    {name: '安徽', value: Window.AH},
    {name: '湖北', value: Window.HUB},
    {name: '四川', value: Window.SC},
    {name: '贵州', value: Window.GZ},
    {name: '广西', value: Window.GX},
    {name: '宁夏', value: Window.NX},
    {name: '西藏', value: Window.XZ},
    {name: '上海', value: Window.SH}, 
    {name: '福建', value: Window.FJ},
    {name: '广东', value: Window.GD},
    {name: '山西', value: Window.SHX},
    {name: '云南', value: Window.YN},
    {name: '海南', value: Window.HAIN},
    {name: '辽宁', value: Window.LN},
    {name: '吉林', value: Window.JL},
    {name: '江西', value: Window.JX},
    {name: '青海', value: Window.QH},
    {name: '内蒙古', value: Window.NMG},
    {name: '陕西', value: Window.SX},
    {name: '重庆', value: Window.CQ},
    {name: '江苏', value: Window.JS},
    {name: '北京', value: Window.BJ},
   ];
   var geoCoordMap = {
'西藏':[91.11,29.97], 
'上海':[121.48,31.22], 
'福建':[119.3,26.08], 
'广东':[113.23,23.16],
'山西':[112.53,37.87], 
'云南':[102.73,25.04],
'海南':[110.35,20.02],
'辽宁':[123.38,41.8], 
'吉林':[125.35,43.88],
'江西':[115.89,28.68], 
'青海':[101.74,36.56],
'内蒙古':[111.65,40.82],
'陕西':[108.95,34.27],
'重庆':[106.54,29.59],
'江苏':[118.78,32.04],
'北京':[116.46,39.92],
'新疆':[87.68,43.77],
'浙江':[120.19,30.26],
'山东':[117,36.65],
'甘肃':[103.73,36.03],
'天津':[117.2,39.13],
'河南':[113.65,34.76],
'黑龙江':[126.63,45.75],
'河北':[114.48,38.03],
'湖南':[113,28.21],
'安徽':[117.27,31.86],
'湖北':[114.31,30.52],
'四川':[104.06,30.67],
'贵州':[106.71,26.57],
'广西':[108.33,22.84],
'宁夏':[106.27,38.47]
};
var convertData = function (data) {
var res = [];
for (var i = 0; i < data.length; i++) {
    var geoCoord = geoCoordMap[data[i].name];
    if (geoCoord) {
        res.push({
            name: data[i].name,
            value: geoCoord.concat(data[i].value)
        });
    }
}
return res;
};
                        
                        var option = {
                            geo: {
      	                         map: 'china'
                                 },
                            tooltip: {
                              //show: false //不显示提示标签
                               formatter: '{b}', //提示标签格式
                               backgroundColor:"#ff7f50",//提示标签背景颜色
                               textStyle:{color:"#fff"} //提示标签字体颜色
                            },
                        //     series: [{
                        //         type: 'map',
                        //         mapType: 'china',
                        //         label: {
                        //             normal: {
                        //                 show: false,//显示省份标签
                        //                 textStyle:{color:"#c71585"}//省份标签字体颜色
                        //             },    
                        //             emphasis: {//对应的鼠标悬浮效果
                        //                 show: true,
                        //                 textStyle:{color:"#800080"}
                        //             } 
                        //         },
                        //         itemStyle: {
                        //             normal: {
                        //                 borderWidth: .5,//区域边框宽度
                        //                 borderColor: '#009fe8',//区域边框颜色
                        //                 areaColor:"#ffefd5",//区域颜色
                        //             },
                        //             emphasis: {
                        //                 borderWidth: .5,
                        //                 borderColor: '#4b0082',
                        //                 areaColor:"#ffdead",
                        //             }
                        //         },
                        //         data:[
                        //             {}//福建为选中状态
                        //         ]
                        //     }],
                        // };
    
    series : [
    {
        name: 'deepinsight',
        // type: 'scatter',
        // coordinateSystem: 'bmap',
        // type: 'map',
        type: 'scatter',
        coordinateSystem: 'geo',
        
                                label: {
                                    normal: {
                                        show: true,//显示省份标签
                                        textStyle:{color:"#c71585"}//省份标签字体颜色
                                    },    
                                    emphasis: {//对应的鼠标悬浮效果
                                        show: false,
                                        textStyle:{color:"#800080"}
                                    } 
                                },
                                itemStyle: {
                                    normal: {
                                        borderWidth: .5,//区域边框宽度
                                        borderColor: '#009fe8',//区域边框颜色
                                        areaColor:"#ffefd5",//区域颜色
                                    },
                                    emphasis: {
                                        borderWidth: .5,
                                        borderColor: '#4b0082',
                                        areaColor:"#ffdead",
                                    }
                                },
        data: convertData(data),
        symbolSize: function (val) {
            return val[2] / 10;
        },
        label: {
            normal: {
                formatter: '{b}',
                position: 'right',
                show: false
            },
            emphasis: {
                show: true
            }
        },
        itemStyle: {
            normal: {
                color: 'purple'
            }
        }
    },
    {
        name: 'Top 5',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: convertData(data.sort(function (a, b) {
            return b.value - a.value;
        }).slice(0, 6)),
        symbolSize: function (val) {
            return val[2] / 10;
        },
        showEffectOn: 'render',
        rippleEffect: {
            brushType: 'stroke'
        },
        hoverAnimation: true,
        label: {
            normal: {
                formatter: '{b}',
                position: 'right',
                show: true
            }
        },
        itemStyle: {
            normal: {
                color: 'purple',
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        zlevel: 1
    }
]
};
                        myChart.setOption(option);
                        // myChart.on('mouseover', function (params) {
                        //     var dataIndex = params.dataIndex;
                        //     console.log(params);
                        // });