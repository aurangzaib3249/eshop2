
var notificationid = $("#notificationid").val()
var notification_url = $("#notification_url").val()
var protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://';
var notifiction = new WebSocket(
    protocol+
    window.location.host +
    '/ws/notify/' +
    notificationid +
    '/'
);

// onmessage - An event listener to be called when a message is received from the server.
notifiction.onmessage = function(e) {
    // JSON.parse() converts the JSON object back into the original object,
    // then examine and act upon its contents.
    const data = JSON.parse(e.data);
    
    if (data.user_status!=undefined)
        {

            console.log()
            $("#user_status"+data.id).html(' <i class="fa fa-circle '+data.user_status+'"></i>'+data.user_status)
            $("#chat_with"+data.id).html(' <i class="fa fa-circle '+data.user_status+'"></i>'+data.user_status)
            
        }
        else{
            console.log(data)
            if (!(notification_url.includes("chat")))
            {
                
            
                showMessage("success", data.current, "Message Received From " + data.sender)
                
            }
            else{

            }
                    if(!(notification_url.includes(data.sender)))
                    {
                        
                        var user_id="#chat_with_id"+data.uid
                        var user=$(user_id).html()
                        if(!(user.includes("fa fa-circle")))
                        {
                            var newm=' <i class="fa fa-circle" style="color:red;font-size:10px;margin-left:5rem"></i> '
                            $(user_id).html(user+newm)
                            console.log($(user_id).html())
                        }
                        
                    }
                
                
               document.getElementById('mySound').play();
                
            
           
        }
   


};

// onclose - An event listener to be called when the connection is closed.
notifiction.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function removeTrailingSlash(str) {
    str = str.replace('/', '')
    console.log(str)
    return str
  }