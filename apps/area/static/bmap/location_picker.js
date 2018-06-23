(function($) {
  var map;
  var prev_el_selector = '.form-row.field-longitude';
  var lat_input_selector = '#id_latitude';
  var lon_input_selector = '#id_longitude';
  var name_input_search = '#id_name';

  function bmapinit(){
    console.log("加载bmap了");
    var $prevEl = $(prev_el_selector);
    if ($prevEl.length === 0) {
      // Can't find where to put the map.
      return;
    };
    $prevEl.after( $('<div id="setloc-bmap"></div>') );
    // 百度地图API功能
    map = new BMap.Map("setloc-bmap");

    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
    var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件

    // 标尺控件
    map.addControl(top_left_control);
    map.addControl(top_left_navigation);

    map.centerAndZoom("福州", 11);


    $lat = $(lat_input_selector);
    $lon = $(lon_input_selector);

    var has_initial_loc = ($lat.val() && $lon.val());

    if (has_initial_loc) {
      // There is lat/lon in the fields, so centre the map on that.
      initial_lat = parseFloat($lat.val());
      initial_lon = parseFloat($lon.val());

      var point = new BMap.Point(initial_lon, initial_lat);
      setPoint(point);

    }

  }

  //定位
  function setPlace(value) {
      var local, point, marker = null;
      local = new BMap.LocalSearch(map, { //智能搜索
          onSearchComplete: fn
      });

      local.search(value);

      function fn() {
          //如果搜索的有结果
          if(local.getResults() != undefined) {
  			      console.log(local.getResults());
              if(local.getResults().getPoi(0)) {
                  point = local.getResults().getPoi(0).point; //获取第一个智能搜索的结果
                  setPoint(point);
                  $(lat_input_selector).val(point.lat);
                  $(lon_input_selector).val(point.lng);
              }
          }
      }
  }

  // 设置点
  function setPoint(point){
    map.clearOverlays(); //清除地图上所有覆盖物
    map.centerAndZoom(point, 15);
    var marker = new BMap.Marker(point); // 创建标注
    map.addOverlay(marker); // 将标注添加到地图中
    marker.enableDragging(); // 可拖拽
  }

  $(document).ready(function(){
    // initMap();
    bmapinit();
    $(name_input_search).bind('input propertychange', function() {
      setPlace($(name_input_search).val());
    });
  });

})(django.jQuery);
