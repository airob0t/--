$(function() {
	$V.controller.productDetail.start();
	$V.outtradeNo;
});

$V.controller.productDetail = function() {
	function start(){
		//$.get('/statistics/ajax_page_log?s=b_new-start-' + $V.key + '-' + $V.weixinId + '-' + $V.retailPrice + '-' + $V.balance);
		bindEvent();
	}	
	
	function bindEvent(){
		//$.get('/statistics/ajax_page_log?s=b_new-bindEvent-' + $V.key + '-' + $V.weixinId);
		
		var coupons   	= $('.coupon');
		var couponInfo 	= $('.couponInfo');
		
		var payBtn    	= $('.btnbox');				//支付按钮
		var realPay   	= $('.realpay');			//支付金额
		var jisuan      = $('.st2');             //计算过程
		
		var payMethod	= $('.pay_method_ubox');	//友宝余额支付方式
	  	var useCoupon	= $('.use_coupon');			//使用友宝优惠券
	  	var useDiscount	= $('.use_discount');		//使用友宝折扣
	  	var useFcard	= $('.use_fcard');			//使用微信朋友共享券
	  	var chooseFcard	= $('.choosefcard');		//选择微信朋友共享券
		
		var address 	= $('.address');			//售货机位置导航
	  	
	  	//售货机位置导航
		address.click(function() {
	      	var map 	= $(this);
	      	var vmlat	= map.attr('vm-lat');
	      	var vmlng	= map.attr('vm-lng');
	      	var vmname	= map.attr('vm-name');
	      	var vmaddress	= map.attr('vm-address');
	      	var vmurl	= map.attr('vm-url');
	      	 	
	      	if(Number(vmlat) > 0 && Number(vmlng) > 0) {
				wx.openLocation({
					latitude: Number(vmlat),
		      		longitude: Number(vmlng),
		      		name: String(vmname),
		      		address: String(vmaddress),
		      		scale: 14,
		      		infoUrl: String(vmurl)
		    	});      
	    	}
		});
		
		jisuan.click(function(){
			$V.MSG({'cancel' : true, 'sure' : false, 'body' : '友宝根据用户在1元有宝支付1元钱后，产生的微信交易单号计算。<br> 交易单号末10位数除以商品价格（以分为单位），如余数在0~99间，则为中奖。', 'canotClick' : false, 'title' : '计算过程'}, function(){});
    		return;
		})
		
		payMethod.click(function() {
			//alert('step: cookie111');
			  var Days = 365;
			  var exp = new Date();
			  exp.setTime(exp.getTime() + Days*24*60*60*1000);
			  document.cookie = 'isOn' + "="+ escape ('isOn') + ";expires=" + exp.toGMTString();
			  var isOn	= payMethod.hasClass('on');
			
			//支付效果切换
			if(isOn) {
				//当前已选中，点击后取消标识
			  exp.setTime(exp.getTime('-1'));
			  document.cookie = 'isOn' + "="+ escape ('') + ";expires=" + exp.toGMTString();
			  payMethod.removeClass('on');
			 
			} else {
				//当前未选中，选中后增加选中标识
			  			  
			  payMethod.addClass('on');
			}

		});
		
		 
		
		
		
	    //立即支付
	    payBtn.on('click', function() {
	    	/*
	    	alert(
	    			'is_android:'+$V.is_android+
					' discountType:'+$V.discountType+
					' weixinId:'+$V.weixinId+ 
					' uid:'+$V.uid+
					' key:'+$V.key+			
					' balance:'+$V.balance+			
					' retailPrice:'+$V.retailPrice+		
					' offeredPrice:'+$V.offeredPrice+		
					' bestCouponPrice:'+$V.bestCouponPrice+ 	
					' bestCouponId:'+$V.bestCouponId+
					' selectCouponHtml:'+$V.selectCouponHtml+	
					' qrId:'+$V.qrId+
					' cardSignInfo_cardSign:'+$V.cardSignInfo_cardSign+
					' cardSignInfo_timestamp:'+$V.cardSignInfo_timestamp+
					' cardSignInfo_nonceStr:'+$V.cardSignInfo_nonceStr+
					' cardSignInfo_shopId:'+$V.cardSignInfo_shopId+
					' cardSignInfo_cardType:'+$V.cardSignInfo_cardType+
					' cardSignInfo_cardId:'+$V.cardSignInfo_cardId
	    	);*/
	    	//step1	$V.weixinId
	    	//$.get('/statistics/ajax_page_log?s=b_new-payBtn_click-' + $V.key + '-' + $V.weixinId);
	    	
			var isOnUobx	= payMethod.hasClass('on');		//true: 当前ubox余额支付	false: 当前微信支付
			
			//支付金额	
			if(isOnUobx) {
				//当前处于选中，不做任何处理

			} else {
				//当前处于未选中，选中后修改支付金额
				$V.MSG({'cancel' : true, 'sure' : false, 'body' : '请先阅读并同意《服务协议》', 'canotClick' : false, 'title' : '用户协议条款'}, function(){});
	    		return;
			}

	    	//支付中...
	    	var btn = $(this);
	    	if(btn.hasClass('paying')) {
	    		//$.get('/statistics/ajax_page_log?s=b_new-payBtn_click_paying-' + $V.key + '-' + $V.weixinId);
	    		$V.MSG({'cancel' : true, 'sure' : false, 'body' : '正在进行支付，请稍候...', 'canotClick' : false, 'title' : '下单失败:('}, function(){});
	    		return;
	    	};
	    	btn.addClass('paying');
	    	
	    	//获取支付状态中...	点击确认跳转至支付结果页面
	    	$V.MSG({'cancel' : false,  'sure' : false, 'body' : '正在获取支付状态，请稍候...', 'canotClick' : true}, function() {
	    		//btn.html('正在获取支付状态，请稍候...');
	    		//延迟5秒显示
	    		setTimeout(function(){
        			payOK(1);
      			}, 	5000);
	    	});
	    	
	    	var self      	= $(this);
	    	// var price     	= $('.realpay');
	    	// var couponId  	= $V.bestCouponId;	//couponInfo.attr('coupon-id');
	    	// var qrId      	= $V.qrId;	//self.attr('data-qrid');
	    	// var newPrice  	= price.attr('real-price');
	    	// var oldPrice  	= price.attr('old-price');
	    	// var retail    	= price.attr('retail-price');
	    	//var pName 		= $('.detailwrapper .goods h1').html();
	      	var vmcode = $V.vmcode;
	      	var vmtype = $V.vmtype;
	      	var pid    = $V.pid;
	      	var pname = $V.pname;

	      	var postData = {
	          	'vmcode'   : vmcode,
	          	'vmtype' : vmtype,
	          	'pid' : pid,
	          	'pname' : pname
	       	}
	       	//创建支付订单
	       	var ajaxUrl	= '/win/ajax_pay_pars?' + Math.random();
	       
	       	$V.util.ajax({
	           	url       : ajaxUrl,
	           	type      : 'post',
	           	data      : postData,
	           	dataType  : 'json',
	           	success   : function(d){
	           		//step2
	           		//alert("ajax_pay_pars callback 2");
	           		//$.get('/statistics/ajax_page_log?s=b_new-ajax_pay_pars_callback-' + $V.key + '-' + $V.weixinId);
	           			

	           		//处理订单结果
	           		callWeixinPay(d)
	           	}
	       	});
	       	
	       	return false;
	    });
	}
	
	//处理订单结果
	
	function callWeixinPay(d) {
		//step3
		//alert("callWeixinPay enter 3");
		//$.get('/statistics/ajax_page_log?s=b_new-callWeixinPay_enter-' + $V.key + '-' + $V.weixinId);
		
		//ubox余额支付

	  
	  	//微信支付
	  	if(!d.code || d.code != 200){
	  		//step4
	  		//alert("callWeixinPay code exception 4");
	  		//$.get('/statistics/ajax_page_log?s=b_new-callWeixinPay_exception-' + $V.key + '-' + $V.weixinId);
	  		$('.btnbox').removeClass('paying'); //.html('立即购买');
      		$V.MSG({'cancel' : true, 'sure' : false, 'body' : d.err_msg || '系统繁忙，请稍后重试', 'canotClick' : false, 'title' : '下单失败 :('}, function(){});
	    	return;
	  	}
	  	$V.outtradeNo = d.out_trade_no;
	  	//调微信js api (发起支付)
	  	if(window.WeixinJSBridge && WeixinJSBridge.invoke){
	  		//step4
			//alert('callWeixinPay WeixinJSBrige enter 4');
	    	//$.get('/statistics/ajax_page_log?s=b_new-WeixinJSBridge_enter-' + $V.key + '-' + $V.weixinId + '-' + outTradeNo + '-' + encodeURI(d.data.package));
	    	
	    	//step5 唤起支付窗口
	    	//str = JSON.stringify(d);
	    	//alert(str);
	    	brandWindow(d.data, $V.outtradeNo);
	    	/*
	    	WeixinJSBridge.invoke("getBrandWCPayRequest", d.data, function(res){
	    		//step8 支付回调
	      		alert('callWeixinPay getBrandWCPayRequest 8');
	      		$.get('/statistics/ajax_page_log?s=call-weixin-end-for-' + outTradeNo + '-(' + JSON.stringify(res) + ')');
	 
	      		payCallback(res);
	      		WeixinJSBridge.log(res.err_msg);
	    	});
	    	*/
	    	
	    	//step6轮询
	    	//8秒后开始轮训后台，查看是否有支付成功通知
      		//payNotifyRotation(outTradeNo, function(success){
        		// $V.util.log("model.payNotifyRotation-callback-" + success + "<br>");
        		// window.location = "/win/getTradeInfo/" + outTradeNo + "/" + success;
      		 //});
 
	    	//payOK(1);
	    	//return;
	  	}else{
	    	//------test
      		//8秒后开始轮训后台，查看是否有支付成功通知
      		//$.get('/statistics/ajax_page_log?s=b_new-WeixinJSBridge_exception-' + $V.key + '-' + $V.weixinId + '-' + outTradeNo + '-' + encodeURI(d.data.package));
	    	$V.MSG("抱歉，网络出错啦！请再试一次，谢谢。");
	  	}
	}
	
	//唤起支付窗口
	function brandWindow(d, outTradeNo) {
		//step5
 		//alert("brandWindow 5 "+JSON.stringify(d));
 		//$.get('/statistics/ajax_page_log?s=b_new-brandWindow_enter-' + $V.key + '-' + $V.weixinId + '-' + outTradeNo + '-' + JSON.stringify(d));
 		
		WeixinJSBridge.invoke("getBrandWCPayRequest", d, function(res){
	    	//step8 支付回调
	      	//alert('brandWindow getBrandWCPayRequest 8');
	      	//$.get('/statistics/ajax_page_log?s=b_new-brandWindow_getBrandWCPayRequest-' + $V.key + '-' + $V.weixinId + '-' + outTradeNo + '-' + JSON.stringify(res));
	 
	      	payCallback(res);
	      	WeixinJSBridge.log(res.err_msg);
	    });
	}
	

// 	
	// //对微信支付回调的处理	
  	function payCallback(d){
  		//step9
 		//alert("payCallback 9 "+JSON.stringify(d));
 		//$.get('/statistics/ajax_page_log?s=b_new-payCallback_enter-' + $V.key + '-' + $V.weixinId + '-' + d.err_msg);
 		
    	if(d.err_msg && d.err_msg.indexOf('ok') >= 0){//支付成功，跳转到支付成功页
    		//支付成功，跳转到支付成功页		d.err_msg: "get_hrand_wcpay_request:ok"
    		//alert("payCallback 10 支付成功");
    		
      		payOK(1);
      		//delNotifyOut();
    	}else if(d.err_msg && d.err_msg.indexOf('cancel') >= 0){
    		//支付失败，d.err_msg: "get_hrand_wcpay_request:cancel"
    		//alert("payCallback 10 支付失败");
    		
      		//delNotifyOut();
      		cancelPay();
    	}else{
    		//非正常错误
   			//alert("payCallback 10 未知异常");
   			
      		setTimeout(function(){
        		//delNotifyOut();
      		}, 5000);
      		cancelPay();
    	}
  	}
  	//清除定时器
  	function delNotifyOut(){
  		//step11
  		//alert("delNotifyOut 11");
  		//$.get('/statistics/ajax_page_log?s=b_new-delNotifyOut-' + $V.key + '-' + $V.weixinId);
  		
    	notifyOut && clearTimeout(notifyOut);
  	}
//   	
  	//用户取消了支付
	function cancelPay(){
		//step12
		//alert("cancelPay 12 取消支付");	
		//$.get('/statistics/ajax_page_log?s=b_new-cancelPay-' + $V.key + '-' + $V.weixinId);
		
	  	//android，取消支付，页面为拿到焦点，无法修改ui~~直接刷页面
	  	if($V.is_android){
	    	window.location = window.location.href;
	  	}else{
	  		//按钮文字修改
  	  		$('.btnbox').removeClass('paying'); //.html('立即购买');
  	  		//隐藏弹框
  			//alert('您取消了支付！');

      		$V.MSG.clear();
	  	}
	}
  
  	//支付完成，跳到订单页  1.页面js返回支付成功  2.页面轮训返回支付成功
  	function payOK(success){
  		//var payMethod	= $('.btnbox');	//支付方式
  		//$.get('/statistics/ajax_page_log?s=b_new-payOK-' + $V.key + '-' + $V.weixinId + '-' + success);
  		//step12 
    	if(success){
    		//alert("payOK 12 支付成功");
    		//if(payMethod.hasClass('on')) {
    			// window.location = "winrepay?outTradeNo=" + $V.outtradeNo;
    			 window.location = "winrepaytest?outTradeNo=" + $V.outtradeNo +"&vmcode="+ $V.vmcode + "&vmtype="+ $V.vmtype + "&pid=" + $V.pid;
    			
    		//} else {
      			// window.location = "winrepay?outTradeNo=" + $V.outtradeNo;
    		//	 window.location = window.location.href;

      		//}
      		//window.location = "http://hongbao.ubox.cn/test/yaoyao/" + outTradeNo + "/" + success;
      		window.event.returnValue = false;
    	}else {
    		//alert("payOK 12 支付失败");
    		window.location = window.location.href;
    	}
  	}
  
	return {
		start : start
	};
}();