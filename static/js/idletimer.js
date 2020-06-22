var idleTimer = null;
var idleState = false;
var idleWait = 600000;
// var idleWait = 5000;

 monitorIdleState(true);
 bindListener();

function bindListener(){

    $('*').bind('mousemove keydown scroll click', function () {

        if(idleTimer != null){
            // console.log('Cancelling setTimeout');
             clearTimeout(idleTimer);
              idleTimer = null;
              idleState = !true; 
              monitorIdleState();
        }

        
    });

}

function idleThreshold(){
    // console.log('Idle State idleThreshold Met');
    //alert("<p>You've been idle for " + idleWait/1000 + " seconds.</p>");
    //endSession();
    displayNotificationMsgSession("Session Timeout.");
    window.location = "/admins/signout";
    // $("body").append("<p>You've been idle for " + idleWait/1000 + " seconds.</p>");
}

function monitorIdleState(start){
    if(!start){
        if(idleTimer != null){
            return;
     }

    }
    
    if(start){
        //console.log('Timeout Is Starting For The First Time');
    }
    
    //console.log('Monitoring Idle State');
    idleState = true;
    idleTimer = setTimeout(function () {    
                 //displayVerifyErrorMsg("Session Time Out");
                 $("#sessionmodal").modal('show');
                 $("#ajax-content").hide();
                 // $('*').bind('click', function (e) {
                 //  e.preventDefault();
                 //  $("#verifyPlaceHolder").html('');
                  idleThreshold();   
                // });   
            }, 
                idleWait
        );
        
}

function displaySessionErrorMsg(){

    $("#loginAlertPlaceHolder").html("<div class='alert alert-danger alert-dismissable fade in'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button><p class='text-left'>Session Timed Out</p></div>");
}

function displayVerifyErrorMsg(msg){

    $("#verifyPlaceHolder").html("<div class=''><p class='text-left'>"+msg+"</p></div>");
}
// (function ($) {

//     $(document).ready(function () {
    
//         $('*').bind('mousemove keydown scroll', function () {
        
//             clearTimeout(idleTimer);
                    
//             if (idleState == true) { 
                
//                 // Reactivated event
//                 $("body").append("<p>Welcome Back.</p>");            
//             }
            
//             idleState = false;
            
//             idleTimer = setTimeout(function () { 
                
//                 // Idle Event
//                 $("body").append("<p>You've been idle for " + idleWait/1000 + " seconds.</p>");

//                 idleState = true; }, idleWait);
//         });
        
//         $("body").trigger("mousemove");
    
//     });
// }) (jQuery)
