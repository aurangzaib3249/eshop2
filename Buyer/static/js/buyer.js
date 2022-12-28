
	$(document).ready(function(){
        $("#loadin_animation").hide()
    });
	function AddTOCart(id)
    {
        console.log(id)
        if (id)
		{
			$.ajax({
				type: 'get',
				url: "/buyer/addCart",
				data: {"id": id,
			},
			
				success: function (response) {
					console.log(response)
					if (response["status"]===200)
					{
						
                        showMessage("success",response["msg"],"Notification")
					}
					
					
				},
				error: function (response) {
					showMessage("error",response["msg"],"Notification")
				}
			})
			

		}
		
		

    }
	function AddTOWIshList(id)
    {
        console.log(id)
        if (id)
		{
			$.ajax({
				type: 'get',
				url: "/buyer/product_add_wishlist",
				data: {"id": id,
			},
			
				success: function (response) {
					console.log(response)
					if (response["status"]===200)
					{
						$("#wishlist"+id).removeAttr('style').css("color","green");
						$("#wishlist"+id).removeAttr('onclick').attr('onclick', "Remove_from_WishList("+id+")");
                        showMessage("success",response["msg"],"Notification")
					}
					
					
				},
				error: function (response) {
					showMessage("error",response["msg"],"Notification")
				}
			})
			

		}
		
		

    }
	function Remove_from_WishList(id)
    {
       console.log(id)
        if (id)
		{
			$.ajax({
				type: 'get',
				url: "wishlist_item_remove_ajax",
				data: {"id": id,
			},
			
				success: function (response) {
					console.log(response)
					if (response["status"]===200)
					{
						$("#wishlist"+id).removeAttr('style').css("color","red");
						$("#wishlist"+id).removeAttr('onclick').attr('onclick', "AddTOWIshList("+id+")");

                        showMessage("success",response["msg"],"Notification")
					}
					
					
				},
				error: function (response) {
					showMessage("error",response["msg"],"Notification")
				}
			})
			

		}
		
		

    }