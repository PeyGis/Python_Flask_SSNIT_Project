//document.addEventListener('contextmenu', event => event.preventDefault());

/**
*Handle enter key press event for username text field
*/

$('#txtUsername').on('keydown', function(e) {
    if (e.which == 13) {
        $('#passwordForm').show("slow");
        $('#forgotPasswordlink').show("slow");
        $('#txtPassword').focus();
    }else if(e.which == 9){
        $('#passwordForm').show("slow");
        $('#forgotPasswordlink').show("slow");
    }else if(e.which == 8 || e.which == 46){
        if ($('#txtUsername').val().length == 0){
            $('#passwordForm').hide("slow");
            $('#forgotPasswordlink').hide("slow");
            $('#txtUsername').removeAttr("border-bottom");
            $('#txtPassword').removeAttr("box-shadow");
            $('#txtUsername').focus();
        }
    }
    else if ($('#txtUsername').val().length <= 0){
        $('#passwordForm').hide("slow");
        $('#forgotPasswordlink').hide("slow");
        $('#txtUsername').removeAttr("border-bottom");
        $('#txtPassword').removeAttr("box-shadow");
        $('#txtUsername').focus();
    }
});
 
/**
*Handle enter key press event for password text field
*/
$('#txtPassword').on('keydown', function(e) {
    if (e.which == 13) {
        show_loader();
        var username = $('#txtUsername').val();
        var password = $('#txtPassword').val();

        valide1 = validate_text_feild(username, "#txtUsername");
        valide2 = validate_text_feild(password, "#txtPassword");

        if( valide1 && valide2 ){
            formData = {
                "username": username,
                "password": password
            }
            console.log(formData);
            $.postJSON("/admins/login", formData, function(data){
              // console.log(data);
              if (data.code == "00") {

                $('#txtUsername').val("");
                $('#txtPassword').val("");

                displaySucessMsg(data.msg);
                window.location = "/home/user";
              }

              else if(data.code == "01"){
                hide_loader();
                $('#txtPassword').val("");
                displayErrorMsg(data.msg); //display Error message
              }

              else if(data.code == "02"){
                hide_loader();
                $('#txtPassword').val("");
                displayErrorMsg(data.msg); //display Error message
              }

              else{
                hide_loader();
                $('#txtPassword').val("");
              }
            });
        }else{
          hide_loader();
        }

    }else if(e.which == 8 || e.which == 46){
        if ($('#txtPassword').val().length <= 0){
            $('#passwordForm').hide("slow");
            $('#forgotPasswordlink').hide("slow");
            $('#txtUsername').removeAttr("border-bottom");
            $('#txtPassword').removeAttr("box-shadow");
            $('#txtUsername').focus();
        }
    }
});


$("#btnForgetPassowrd").click(function(e){
  e.preventDefault();
  $("#loginForm").hide();
  $("#forgotPassForm").show();
});


$("#btnSendPassowrd").click(function(e){
  e.preventDefault();
  username = $("#txtUsernameforgot").val();
  
  var formData = {
        'username': username
    };

    // console.log(formData)
    show_loader();

    $.postJSON("/admins/forgotpass", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          $("#btnSendCancel").html('<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"> </span>Back to login');
          displaySucessMsg(data.msg);
        }

        else if(data.code == "01"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          $('#txtPassword').val("");
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
          $('#txtPassword').val("");
        }
      });
});


$('#theFile').change(function(){
    var file = this.files[0];
    var name = file.name;
    var size = file.size;
    var type = file.type;
    var path = file.path;
    console.log("File: " + file);
    console.log("Name: " + name);
    console.log("Size: " + size);
    console.log("Type: " + type);
    console.log("Path: " + path);

    $('#tblfileName').html(name);
    $('#tblfileSize').html(size);
    $('#tblfileType').html(type);

    $('#uploadTbl').show("slow");

});


function cancelUpload() {
    $('#theFile').val("");
    $('#uploadTbl').hide("slow");
}


//$( "#form1" ).submit(function( event ) {
    // $( "#theFileUploads" ).click(function( event ) {
    //   //event.preventDefault();
    //   //alert( "Handler for .submit() called." );
    //   console.log($('#form1').serialize());
    //   $.ajax({
    //         url: '/bulkpay/record',
    //         type: 'post',
    //         dataType: 'json',
    //         data: $('#form1').serialize(),
    //         success: function(data) {
    //           alert( "Done ooo" );
    //           window.location = "/bulkpay/";
    //         }
    //     });
    // });

$("#uploadBtn").click(function(e){
  e.preventDefault();
  $("#theFileUploads").click()
  //$( "#form1" ).submit();
});


function get_payment_details(bulk_id){
    var formData = {
        'bulk_id': bulk_id
    };

    // console.log(formData)
    show_loader();

    $.postJSON("/uploads/details", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_payment_modal(data.data[0], data.user);
        }

        else if(data.code == "01"){
          hide_loader();
          $('#txtPassword').val("");
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          $('#txtPassword').val("");
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
          $('#txtPassword').val("");
        }
      });

}


function load_payment_modal(detail, user){
    // get_institutions();

    console.log(detail)

    $('#txtBulkId').text(detail.bulk_id);
    $('#txtFamount').text(detail.amount);
    $('#txtFilename').text(detail.filename);
    $('#txtApprovalStatus').text(detail.approval_status);
    $('#txtProcesStatus').text(detail.filename);
    $('#txtBulkCharge').text(detail.xcharge_before_bulk_processing);

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.approval_data.length; i++) {
      if (detail.approval_data[i]['merchant_admin_approval_status'] == 1) {
        resp = "Approved";
      }else{
        resp = "Declined";
      }
      
      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                        '<td style="color: #FF6A13; font-weight: bolder">'+ detail.approval_data[i]['username'] +'</td>'+
                        '<td>'+ detail.approval_data[i]['user_type'] +'</td>'+
                        '<td>'+ resp +'</td>'+
                        '<td>'+ detail.approval_data[i]['merchant_admin_approval_date'] +'</td>'+
                        '<td>'+ detail.approval_data[i]['merchant_admin_approval_remarks'] +'</td>'+
                      '</tr>';
    }

    $('#appTblBody').html(tblBodyHtml);

    if(detail.can_approve.status == false){
      $("#btnDeclineFile").hide();
      $("#btnApproveFile").hide();
    }else{
      $("#btnDeclineFile").show();
      $("#btnApproveFile").show();
    }

    txt_val = '';
    details = JSON.parse(detail.bulk_upload_error_report);
    // details = detail.bulk_upload_error_report;

    if (details == null){
      $("#errordPanel").hide();
    }else{
      for (var i = 0; i < details.data.length; i++) {
        txt_val += 'Error on line ' + details.data[i].line + ': ' + details.data[i].details + '<br>';
      }
          
      $('#txtError_box').html("<pre>" +txt_val+ "</pre>");
      $("#errordPanel").show();
    }

    $("#paymentDetailsModal").modal("show");
}


function bulkUploadsNext(){

  nextpage = parseInt($("#page_id_bu").val());
  total_pages = parseInt($("#uploads_total_pages").val())

  if(nextpage < total_pages){
    var formData = {
        'page': nextpage,
        'fromdate': "",
        'todate': ""
    };

    console.log(formData)
    show_loader();

    $.postJSON("/vouchers/uploads", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_uploads_table(data.data, "plus");
        }
        else{
          hide_loader();
        }
      });
    }
}


function bulkUploadsPrev(){

  nextpage = parseInt($("#page_id_bu").val())

  if(nextpage > 1){
    if (nextpage > 1) {
      nextpage -= 1;
    }else{
      nextpage = 1;
    }

      var formData = {
          'page': nextpage - 1,
          'fromdate': "",
          'todate': ""
      };

      console.log(formData)

      // console.log(formData)
      show_loader();

      $.postJSON("/vouchers/uploads", formData, function(data){
          // console.log(data);
          if (data.code == "00") {
            hide_loader();
            load_uploads_table(data.data, "minus");
          }
          else{
            hide_loader();
          }
        });
    }
}

function bulkUploadsCurr(){

  nextpage = parseInt($("#page_id_bu").val())

  // if (nextpage > 1) {
  //   nextpage = nextpage;
  // }else{
  //   nextpage = 1;
  // }

    var formData = {
        'page': nextpage - 1,
        'fromdate': "",
        'todate': ""
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/uploads", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_uploads_table(data.data, "");
        }
        else{
          hide_loader();
        }
      });

}


function load_uploads_table(detail, operator, page){
    // get_institutions();

    console.log(detail)

    // if (detail.length == 0) {
    //   return;
    // }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      action_html = ""
      if( detail[i].approval_status == 'Not Approved' && detail[i].processing_status == 'Not Processed') {
        action_html = '<a onclick="approve_upload("' + detail[i].bulk_id + '")>Approve</a> | <a onclick="decline_upload("' + detail[i].bulk_id + '")">Decline</a> | <a onclick="window.open(\'/static/uploads/' + detail[i].bulk_id + '.csv\'">Download File</a>'
      }else if( detail[i].approval_status == 'Approved' ){
        action_html = '<a href="/vouchers/' + detail[i].bulk_id + '">Details</a> | <a onclick="window.open(\'/static/uploads/'+ detail[i].bulk_id +'.csv\')">Download File</a>'
      }else{
        action_html = '<a onclick="window.open(\'/static/uploads/'+ detail[i].bulk_id +'.csv\')">Download File</a>'
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                        '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].bulk_id +'</td>'+
                        '<td>'+ detail[i].filename +'</td>'+
                        '<td>'+ detail[i].approval_status +'</td>'+
                        '<td>'+ detail[i].uploaded_by +'</td>'+
                        '<td>'+ detail[i].upload_date +'</td>'+
                        '<td style="color: #108E53;">'+ action_html +'</td>'+
                      '</tr>';
    }

    $('#uploadsTblBody').html("");
    $('#uploadsTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id_bu").val());

    if (operator == "plus") {
      $("#page_id_bu").val(nextpage+1);
    }else if (operator == "minus"){
      if((nextpage -1 ) <= 0){
        $("#page_id_bu").val(1)
      }else{
        $("#page_id_bu").val((parseInt(nextpage)-1));
      }
    } else{
      //do nothing
    }
}


function customerReqsNext(){

  nextpage = parseInt($("#page_id_cr").val());

  fromdate = $("#reqfromdate").val();
  todate = $("#reqtodate").val();
  branch = $("#reqtxtBranch").val();
  type = $("#reqtxtType").val();

    if (nextpage == 1) {
      nextpage += 1 ;
    }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'branch': branch,
        'request_type': type
    };

    console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_requests_table(data.data, "plus");
        }
        else{
          hide_loader();
        }
      });

}


function customerReqsPrev(){

  nextpage = parseInt($("#page_id_cr").val())

  fromdate = $("#reqfromdate").val();
  todate = $("#reqtodate").val();
  branch = $("#reqtxtBranch").val();
  type = $("#reqtxtType").val();

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'branch': branch,
        'request_type': type
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_requests_table(data.data, "minus");
        }
        else{
          hide_loader();
        }
      });

}

function customerReqsCurr(){

  nextpage = parseInt($("#page_id_cr").val())

  fromdate = $("#reqfromdate").val();
  todate = $("#reqtodate").val();
  branch = $("#reqtxtBranch").val();
  type = $("#reqtxtType").val();

  if (nextpage > 1) {
    nextpage = nextpage;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'branch': branch,
        'request_type': type
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_requests_table(data.data, "");
        }
        else{
          hide_loader();
        }
      });

}


function filterUserRequests(){

  $("#page_id_cr").val(1)

  fromdate = $("#reqfromdate").val();
  todate = $("#reqtodate").val();
  branch = $("#reqtxtBranch").val();
  type = $("#reqtxtType").val();

  nextpage = parseInt($("#page_id_cr").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'branch': branch,
        'request_type': type
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_requests_table(data.data, "minus");
          $("#fileFilter").modal("hide");
        }

        else{
          hide_loader();
        }
      });

}


$('#btnFilterUserRequests').click(function(e) {
    e.preventDefault();   

  $("#page_id_cr").val(1)

  fromdate = $("#reqfromdate").val();
  todate = $("#reqtodate").val();
  // branch = $("#reqtxtBranch").val();
  type = $("#reqtxtType").val();

  nextpage = parseInt($("#page_id_cr").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        // 'branch': branch,
        'request_type': type
    };


    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_requests_table(data.data, "minus");
          $("#customerRequestFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});



$('#btnSerchUserRequests').click(function(e) {
    e.preventDefault();   

  $("#page_id_cr").val(1)

  accountno = $("#txtSearchcr").val();

  var formData = {
        'search_param': accountno
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/requests/search", formData, function(data){
        console.log(data);
        // if (data.code == "00") {
          load_requests_table(data, "");
          hide_loader();
          // $("#transFilter").modal("hide");
        // }

        // else{
        //   hide_loader();
        //   displayErrorMsg(data.msg); //display Error message
        // }
      });
    hide_loader();
});



function load_requests_table(detail, operator, page){
    // get_institutions();

    console.log(detail)

    // if (detail.length == 0) {
    //   hide_loader();
    //   displayErrorMsg("No data Found."); //display Error message
    //   return;
    // }

    role = $("#userAppoveRole").val()

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      req_type = ""
      if(detail[i].request_type == 0){
        req_type = "Registration";
      }else if(detail[i].request_type == 1){
        req_type = "Reset Pin";
      }else if(detail[i].request_type == 2){
        req_type = "Change Phone Number";
      }else if(detail[i].request_type == 3){
        req_type = "Change Account Number";
      }else if(detail[i].request_type == 4){
        req_type = "Deactivate Account Number";
      }else if(detail[i].request_type == 5){
        req_type = "Activate Account Number";
      }else if(detail[i].request_type == 6){
        req_type = "Add Account Number";
      }else if(detail[i].request_type == 7){
        req_type = "Block Customer";
      }else if(detail[i].request_type == 8){
        req_type = "Unblock Customer";
      }else{
        req_type = "Unknown";
      }

      action_html = ""
      if (role == 'I') {
        if(detail[i].request_type == 0){
        action_html = '<a title="Approve Request" onclick="approve_customer_request(\''+ detail[i].id +'\')">Approve</a> | <a title="Decline Request" onclick="decline_customer_request(\''+ detail[i].id +'\')">Decline</a> | <a title="Registration Detials" onclick="details_customer_request("'+ detail[i].id +'")">Details</a>';
        }else{
          action_html = '<a title="Approve Request" onclick="approve_customer_request(\''+ detail[i].id +'\')">Approve</a> | <a title="Decline Request" onclick="decline_customer_request(\''+ detail[i].id +'\')">Decline</a>'
        }
      }else{
        action_html = "No Action"
      }
      

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                        '<td style="color: #FF6A13; font-weight: bolder">'+ req_type +'</td>'+
                        '<td>'+ detail[i].customer_msisdn +'</td>'+
                        '<td>'+ detail[i].customer_account +'</td>'+
                        '<td>'+ detail[i].change_from +'</td>'+
                        '<td>'+ detail[i].change_to +'</td>'+
                        '<td>'+ detail[i].request_date +'</td>'+
                        '<td style="color: #108E53;">'+ action_html +'</td>'+
                      '</tr>';
    }

    $('#customerReqsTblBody').html("");
    $('#customerReqsTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id_cr").val());

    if (operator == "plus") {
      $("#page_id_cr").val(nextpage+1);
    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id_cr").val(1)
      }else{
        $("#page_id_cr").val((parseInt(nextpage)-1));
      }
    }
}


function transactionNext(){

  fromdate = $("#tfromdate").val();
  todate = $("#ttodate").val();
  branch = $("#ttxtBranch").val();
  destination = $("#ttxtDestination").val();
  type = $("#ttxtType").val();
  tag = $("#ttxtTag").val();
  status = $("#ttxtStatus").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

  maxpage = parseInt($("#total_pages").text());
  console.log(nextpage)
  console.log(maxpage)
  console.log(nextpage >= maxpage)

  if (nextpage > maxpage) {
    return;
  }

    var formData = {
        'page': nextpage,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch,
        'destination': destination,
        'type': type,
        'tag': tag
    };

    console.log(formData)
    show_loader();

    $.postJSON("/transactions/", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_transaction_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function transactionPrev(){

  fromdate = $("#tfromdate").val();
  todate = $("#ttodate").val();
  branch = $("#ttxtBranch").val();
  destination = $("#ttxtDestination").val();
  type = $("#ttxtType").val();
  tag = $("#ttxtTag").val();
  status = $("#ttxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch,
        'destination': destination,
        'type': type,
        'tag': tag
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/transactions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_transaction_table(data.data, "minus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function filterTransactions(){

  fromdate = $("#tfromdate").val();
  todate = $("#ttodate").val();
  branch = $("#ttxtBranch").val();
  destination = $("#ttxtDestination").val();
  type = $("#ttxtType").val();
  tag = $("#ttxtTag").val();
  status = $("#ttxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage = nextpage;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch,
        'destination': destination,
        'type': type,
        'tag': tag
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/transactions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_transaction_table(data.data, "");
          $("#transFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterTransactions').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tfromdate").val();
  todate = $("#ttodate").val();
  branch = $("#ttxtBranch").val();
  destination = $("#ttxtDestination").val();
  type = $("#ttxtType").val();
  tag = $("#ttxtTag").val();
  status = $("#ttxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch,
        'destination': destination,
        'type': type,
        'tag': tag
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/transactions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_transaction_table(data.data, "minus");
          $("#transFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});



$('#btnSerchTrans').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  accountno = $("#txtSearch").val();

  var formData = {
        'search_param': accountno
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/transactions/search", formData, function(data){
        console.log(data);
        // if (data.code == "00") {
          load_transaction_table(data, "");
          hide_loader();
          // $("#transFilter").modal("hide");
        // }

        // else{
        //   hide_loader();
        //   displayErrorMsg(data.msg); //display Error message
        // }
      });
    hide_loader();
});


$('#btnExportTransactions').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tfromdate").val();
  todate = $("#ttodate").val();
  branch = $("#ttxtBranch").val();
  destination = $("#ttxtDestination").val();
  type = $("#ttxtType").val();
  tag = $("#ttxtTag").val();
  status = $("#ttxtStatus").val();
  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch,
        'destination': destination,
        'type': type,
        'tag': tag
    };

    window.open("/transactions/export?page="+(nextpage).toString()+'&fromdate='+fromdate+'&todate='+todate+'&status='+status+'&branch='+branch+'&destination='+destination+'&type='+type+'&tag='+tag);

});


function load_transaction_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    tblBodyHtml = ""
    resp = ""

    if (detail[0].length == 0) {
      tblBodyHtml = '<tr style="background-color: #FEF9F3"> No records found </tr>';
      $('#transactionTblBody').html("");
      $('#transactionTblBody').html(tblBodyHtml);
      return;
    }
    for (var i = 0; i < detail[0].length; i++) {

      status = '';
      if (detail[0][i].msg_stat == "SUCCESSFUL") {
        status = '<i class="fa fa-circle trans_success" aria-hidden="true"></i>';
      }else if (detail[0][i].msg_stat == "PENDING") {
        status = '<i class="fa fa-circle trans_Initiated" aria-hidden="true"></i>';
      }else if (detail[0][i].msg_stat == "REVERSED") {
        status = '<i class="fa fa-circle trans_reversed" aria-hidden="true"></i>';
      }else{
        status = '<i class="fa fa-circle trans_failed" aria-hidden="true"></i>';
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[0][i].xref +'</td>'+
                  '<td>'+ detail[0][i].reference +'</td>'+
                  '<td>'+ detail[0][i].account_number +'</td>'+
                  '<td>'+ detail[0][i].account_branch +'</td>'+
                  '<td>'+ detail[0][i].des_act +'</td>'+
                  '<td>'+ detail[0][i].destination +'</td>'+
                  '<td>'+ detail[0][i].msisdn +'</td>'+
                  '<td>'+ detail[0][i].amount +'</td>'+
                  '<td>'+ detail[0][i].type +'</td>'+
                  '<td>'+ detail[0][i].fusion_tag +'</td>'+
                  '<td>'+ status +'</td>'+
                  '<td>'+ detail[0][i].request_time +'</td>'+
                  '<td>'+ detail[0][i].response_time +'</td>'+
              '</tr>';
    }

    $('#transactionTblBody').html("");
    $('#transactionTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else if(operator == ""){

    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    }
    

}

function getTransactionFilterOptions(){

    $.postJSON("/transactions/filteroptions", {}, function(data){
        console.log(data)
        branch_option = '<option value="">All</option>';
        for (var i = data.branches.length - 1; i >= 0; i--) {
          branch_option = branch_option + '<option value="'+data.branches[i]['account_branch']+'">'+data.branches[i]['account_branch']+'</option>'
        }
        $("#ttxtBranch").html(branch_option);

        des_option = '<option value="">All</option>';
        for (var i = data.destination.length - 1; i >= 0; i--) {
          des_option = des_option + '<option value="'+data.destination[i]['destination']+'">'+data.destination[i]['destination']+'</option>'
        }
        $("#ttxtDestination").html(des_option);

        type_option = '<option value="">All</option>';
        for (var i = data.type.length - 1; i >= 0; i--) {
          type_option = type_option + '<option value="'+ data.type[i]['type'] +'">'+data.type[i]['type']+'</option>'
        }
        $("#ttxtType").html(type_option);

        tag_option = '<option value="">All</option>';
        for (var i = data.tag.length - 1; i >= 0; i--) {
          tag_option = tag_option + '<option value="'+ data.tag[i]['fusion_tag'] +'">'+ data.tag[i]['fusion_tag'] +'</option>'
        }
        $("#ttxtTag").html(tag_option);

        st_option = '<option value="">All</option>';
        for (var i = data.status.length - 1; i >= 0; i--) {
          st_option = st_option + '<option value="' +data.status[i]['msg_stat']+ '">'+data.status[i]['msg_stat']+'</option>'
        }
        $("#ttxtStatus").html(st_option);
      });

}


function adminsNext(){

  fromdate = $("#afromdate").val();
  todate = $("#atodate").val();
  group = $("#txtAdminGroupFilter").val();
  branch = $("#txtBranchAdminFilter").val();
  active = $("#atxtStatus").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'user_right_id': group,
        'branch': branch,
        'active': active
    };

    console.log(formData)
    show_loader();

    $.postJSON("/admins/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_admins_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function adminsPrev(){

  fromdate = $("#afromdate").val();
  todate = $("#atodate").val();
  group = $("#txtAdminGroupFilter").val();
  branch = $("#txtBranchAdminFilter").val();
  active = $("#atxtStatus").val();
  
  nextpage = parseInt($("#page_id").val())
  if(nextpage > 1){
    if (nextpage > 1) {
      nextpage -= 1;
    }else{
      nextpage = 1;
    }

    var formData = {
          'page': nextpage - 1,
          'fromdate': fromdate,
          'todate': todate,
          'user_right_id': group,
          'branch': branch,
          'active': active
      };

      console.log(formData)

      // console.log(formData)
      show_loader();

      $.postJSON("/admins/", formData, function(data){
          // console.log(data);
          if (data.code == "00") {
            hide_loader();
            load_admins_table(data.data, "minus");
          }
          else{
            hide_loader();
            displayErrorMsg(data.msg); //display Error message
          }
        });
    }
}


function filterAdmins(){

  $("#page_id").val(1)

  fromdate = $("#afromdate").val();
  todate = $("#atodate").val();
  group = $("#txtAdminGroupFilter").val();
  branch = $("#txtBranchAdminFilter").val();
  active = $("#atxtStatus").val();
  
  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'user_right_id': group,
        'branch': branch,
        'active': active
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/admins/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_admins_table(data.data, "minus");
          $("#adminsFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterAdmins').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#afromdate").val();
  todate = $("#atodate").val();
  group = $("#txtAdminGroupFilter").val();
  branch = $("#txtBranchAdminFilter").val();
  active = $("#atxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }
  
  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'user_right_id': group,
        'branch': branch,
        'active': active
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/admins/", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_admins_table(data.data, "minus");
          $("#adminsFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnExportAdmins').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#afromdate").val();
  todate = $("#atodate").val();
  group = $("#txtAdminGroupFilter").val();
  branch = $("#txtBranchAdminFilter").val();
  active = $("#atxtStatus").val();
  
  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'user_right_id': group,
        'branch': branch,
        'active': active
    };

    window.open("/admins/export?page="+(nextpage-1).toString()+'&fromdate='+fromdate+'&todate='+todate+'&user_right_id='+group+'&active='+active);

});

$('#btnSerchAdmins').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  searc_text = $("#txtSearchad").val();

  var formData = {
        'search_param': searc_text
    };

    console.log(formData)

    // console.log(formData)
    if (searc_text !== ''){
      show_loader();

      $.postJSON("/admins/search", formData, function(data){
          console.log(data);
            hide_loader();
            load_admins_table(data, "");
      });
    }
});

function load_admins_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    if (detail.length == 0) {
      return;
    }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      status = '';
      if (detail[i].active == 1 || detail[i].active == '1' || detail[i].active == 'Active') {
        status = '<i class="fa fa-circle trans_success" aria-hidden="true"></i>';
      }
      else{
        status = '<i class="fa fa-circle trans_failed" aria-hidden="true"></i>';
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].username +'</td>'+
                  '<td>'+ detail[i].first_name +'</td>'+
                  '<td>'+ detail[i].last_name +'</td>'+
                  '<td>'+ detail[i].email +'</td>'+
                  '<td>'+ detail[i].msisdn +'</td>'+
                  '<td>'+ detail[i].branch_code +'</td>'+
                  '<td>'+ detail[i].name +'</td>'+
                  '<td>'+ status +'</td>'+
                  '<td>'+ detail[i].created +'</td>'+
                  '<td style="color: #108E53;"><a onclick="get_admin_details(\''+ detail[i].username +'\')">Details</a></td>'
              '</tr>';
    }

    $('#adminsTblBody').html("");
    $('#adminsTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else if (operator == "minus"){
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    } else{

    }
    
}

function load_serials_table(detail, operator){
  // get_institutions();

  console.log(detail);

  tblBodyHtml = ""
  resp = ""
  for (var i = 0; i < detail.length; i++) {

    tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].serial_id +'</td>'+
                '<td>'+ detail[i].date_approved +'</td>'+
                '<td>'+ detail[i].hashed_serial_number +'</td>'+
                '<td>'+ detail[i].expiry_date +'</td>'+
                '<td>'+ detail[i].branch_assigned +'</td>'+
                '<td>'+ detail[i].serial_status +'</td>'
            '</tr>';
  }

  $('#serialsTblBody').html("");
  $('#serialsTblBody').html(tblBodyHtml);

  nextpage = parseInt($("#page_id").val());

  if (operator == "plus") {
    $("#page_id").val(nextpage+4);
    document.getElementById("page_id").value = nextpage+4;
    console.log(nextpage);
  }else{
    if((nextpage -1 ) <= 0){
      $("#page_id").val(1);
    }else{
      $("#page_id").val((parseInt(nextpage)-1));
      document.getElementById("page_id").value = nextpage-1;

    }
  }
  
}

function InstNext(){

  fromdate = $("#ifromdate").val();
  todate = $("#itodate").val();
  status = $("#itxtStatus").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
    };

    console.log(formData)
    show_loader();

    $.postJSON("/institutions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_admins_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function InstPrev(){

  fromdate = $("#ifromdate").val();
  todate = $("#itodate").val();
  status = $("#itxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/institutions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_admins_table(data.data, "minus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function filterInst(){

  $("#page_id").val(1)

  fromdate = $("#ifromdate").val();
  todate = $("#itodate").val();
  status = $("#itxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/institutions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_Inst_table(data.data, "minus");
          $("#instsFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterInst').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#ifromdate").val();
  todate = $("#itodate").val();
  status = $("#itxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/institutions/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_Inst_table(data.data, "minus");
          $("#instsFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnExportInst').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#ifromdate").val();
  todate = $("#itodate").val();
  status = $("#itxtStatus").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status
    };

    show_loader_modal();
    window.open("/institutions/export?page="+(nextpage-1).toString()+'&fromdate='+fromdate+'&todate='+todate+'&status='+status);

});


function load_Inst_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    // if (detail.length == 0) {
    //   return;
    // }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      status = '';
      if (detail[i].status == "Active") {
        status = '<i class="fa fa-circle trans_success" aria-hidden="true"></i>';
      }
      else{
        status = '<i class="fa fa-circle trans_failed" aria-hidden="true"></i>';
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].name +'</td>'+
                  '<td>'+ detail[i].shortName +'</td>'+
                  '<td>'+ detail[i].description +'</td>'+
                  '<td>'+ detail[i].username +'</td>'+
                  '<td>'+ status +'</td>'+
                  '<td>'+ detail[i].registration_date +'</td>'+
                  '<td style="color: #108E53;"><a onclick="get_inst_details(\''+ detail[i].shortName +'\')">Details</a></td>'
              '</tr>';
    }

    $('#instTblBody').html("");
    $('#instTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    }
    

}


function customersNext(){

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch
    };

    console.log(formData)
    show_loader();

    $.postJSON("/vouchers/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_customers_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function customersPrev(){

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_customers_table(data.data, "minus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function customersCurr(){

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val())

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_customers_table(data.data, "");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function filterCustomers(){

  $("#page_id").val(1)

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        'branch': branch
      };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_customers_table(data.data, "minus");
          $("#customersFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterCustomers').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  // branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        // 'branch': branch
      };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_customers_table(data.data, "minus");
          $("#customersFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnExportCustomers').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();
  status = $("#mtxtStatus").val();
  // branch = $("#mtxtBranch").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
        'status': status,
        // 'branch': branch
      };

    // show_loader_modal();
    window.open("/vouchers/export?page="+(nextpage-1).toString()+'&fromdate='+fromdate+'&todate='+todate+'&status='+status);

});

$('#btnSerchCustomers').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  search_param = $("#txtSearchcs").val();

  var formData = {
        'search_param': search_param
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/search", formData, function(data){
        console.log(data);
        // if (data.code == "00") {
          hide_loader();
          load_customers_table(data, "");
          // $("#transFilter").modal("hide");
      //   }

      //   else{
      //     hide_loader();
      //     displayErrorMsg(data.msg); //display Error message
      //   }
      });

});


function load_customers_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    tblBodyHtml = ""
    resp = ""

    // if (detail.length == 0) {
    //   displayNotificationMsg("No data Found");
    //   return;
    // }

    
    for (var i = 0; i < detail.length; i++) {

      status = '';
      if (detail[i].status == "ACTIVE") {
        status = '<i class="fa fa-circle trans_success" aria-hidden="true"></i>';
      }
      else{
        status = '<i class="fa fa-circle trans_failed" aria-hidden="true"></i>';
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].id +'</td>'+
                  '<td>'+ detail[i].first_name +'</td>'+
                  '<td>'+ detail[i].last_name +'</td>'+
                  '<td>'+ detail[i].middle_name +'</td>'+
                  '<td>'+ detail[i].gender +'</td>'+
                  '<td>'+ status +'</td>'+
                  '<td>'+ detail[i].join_date +'</td>'+
                  '<td style="color: #108E53;"><a onclick="get_customer_details(\''+ detail[i].id +'\')">Details</a></td>'
              '</tr>';
    }

    $('#customersTblBody').html("");
    $('#customersTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else if(operator == ""){

    }
    else{
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    }
    

}


function get_customer_details(customer_id){
    // var formData = {
    //     'customer_id': customer_id
    // };

    // console.log(formData)
    show_loader();
    window.location = "/activities/details/"+customer_id;

    // $.postJSON("/vouchers/details", formData, function(data){
    //     // console.log(data);
    //     if (data.code == "00") {
    //       hide_loader();
    //       load_customers_modal(data.data);
    //     }

    //     else if(data.code == "01"){
    //       hide_loader();
    //       $('#txtPassword').val("");
    //       displayErrorMsg(data.msg); //display Error message
    //     }

    //     else if(data.code == "02"){
    //       hide_loader();
    //       $('#txtPassword').val("");
    //       displayErrorMsg(data.msg); //display Error message
    //     }

    //     else{
    //       hide_loader();
    //       $('#txtPassword').val("");
    //     }
    //   });

}


function load_customers_modal(detail){
    // get_institutions();

    console.log(detail)

    $('#detCusId').text(detail[0]['customer_id']);
    $('#detCusAccNumber').text(detail[0]['accountno']);
    $('#detCusProduct').text(detail[0]['product']);
    $('#detCusTagamt').text(detail[0]['target_amount']);
    $('#detCusTagdate').text(detail[0]['target_date']);
    $('#detCusWatNo').text(detail[0]['wallet']);
    $('#detCusWalMno').text(detail[0]['wallet_mno']);
    $('#detCusBaln').text(detail[0]['account_balance']);
    $('#txtCusFirstNameMod').val(detail[0]['fname']);
    $('#txtCusLastNameMod').val(detail[0]['lname']);
    $('#txtCusMiddleNameMod').val(detail[0]['mname']);
    $('#txtCusSexMod').val(detail[0]['sex']);
    $('#txtCusWithdStatusMod').val(detail[0]['withdrawal_status']);
    $('#txtCusDepositStatusMod').val(detail[0]['deposit_status']);
    $('#txtCusProductMod').val(detail[0]['product']);
    $('#txtCusStatusMod').val(detail[0]['status']);
    $('#txtCusIdMod').val(detail[0]['customer_id']);

    $("#modifyCustomersModal").modal("show");
}

//function showAddController() {
//  $("#btnModifyCustomer").show();
//}

//function hideAddController() {
//  $("#btnModifyCustomer").hide();
//}


/**
*Handle enter key press event for password text field
*/
$('#btnAddCustomers').click(function(e) {
    e.preventDefault();    
    var first_name = $('#txtCusFirstNameAdd').val();
    var last_name = $('#txtCusLastNameAdd').val();
    var middle_name = $('#txtCusMiddleNameAdd').val();
    var gender = $('#txtCusGenderAdd').val();
    var account = $('#txtCusAccountAdd').val();
    var msisdn = $('#txtCusMsisdnAdd').val();
    var dob = $('#txtCusDobAdd').val();
    var region = $('#txtCusRegionAdd').val();
    var city = $('#txtCusCityAdd').val();

    valide1 = validate_text_feild(first_name, "#txtCusFirstNameAdd", "name");
    valide2 = validate_text_feild(last_name, "#txtCusLastNameAdd", "name");
    //valide3 = validate_text_feild(middle_name, "#txtCusMiddleNameAdd", "name");
    valide4 = validate_text_feild(gender, "#txtCusGenderAdd");
    valide5 = validate_text_feild(account, "#txtCusAccountAdd");
    valide6 = validate_text_feild(msisdn, "#txtCusMsisdnAdd", "phone");
    valide7 = validate_text_feild(dob, "#txtCusDobAdd");
    valide8 = validate_text_feild(region, "#txtCusRegionAdd");
    valide9 = validate_text_feild(city, "#txtCusCityAdd");

    formData = {
          "customer_account": account,
          "customer_msisdn": msisdn,
          "new_fname": first_name,
          "new_lname": last_name,
          "new_mname": middle_name,
          "dob": dob,
          "new_gender": gender,
          "region": region,
          "city": city
      }
      console.log(formData);

    if( valide1 && valide2 && valide4 && valide5 && valide6 && valide7 && valide8 && valide9 ){
      show_loader_modal();
      $.postJSON("/vouchers/add", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtCusFirstNameAdd').val("");
          $('#txtCusLastNameAdd').val("");
          $('#txtCusMiddleNameAdd').val("");
          $('#txtCusGenderAdd').val("");
          $('#txtCusAccounrAdd').val("");

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            filterCustomers();
            $('#addCustomers').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnUpdateCustomer').click(function(e) {
    e.preventDefault();   
    // var org_msisdn = $('#txtOrgMsisdnMod').val();
    // var org_account = $('#txtOrgAccontMod').val();
    var customer_id = $('#txtCustomerIdMod').val();
    var first_name = $('#txtFirstNameMod').val();
    var last_name = $('#txtlastNameMod').val();
    var middle_name = $('#txtmiddleNameMod').val();
    var gender = $('#txtGenderMod').val();
    var msisdn = $('#txtMsisdnMod').val();
    var branch = $('#txtbranchMod').val();
    
    if (customer_id != msisdn) {
      $("#modifyPara").html(" Are you sure you want to update and change the customers phone number? A change phone number request will be sent. ")
    }else{
      $("#modifyPara").html(" Are you sure you want to update this customer's deatials? ")
    }

    $("#customersModifyModal").modal("show");

});


/**
*Handle enter key press event for password text field
*/
$('#btnModifyCustomer').click(function(e) {
    e.preventDefault();    
    // var org_msisdn = $('#txtOrgMsisdnMod').val();
    // var org_account = $('#txtOrgAccontMod').val();
    var customer_id = $('#txtCustomerIdMod').val();
    var first_name = $('#txtFirstNameMod').val();
    var last_name = $('#txtlastNameMod').val();
    var middle_name = $('#txtmiddleNameMod').val();
    var gender = $('#txtGenderMod').val();
    var msisdn = $('#txtMsisdnMod').val();
    var branch = $('#txtbranchMod').val();

    // valide1 = validate_text_feild(org_msisdn, "#txtCusFirstNameMod");
    // valide2 = validate_text_feild(org_account, "#txtCusLastNameMod");
    valide3 = validate_text_feild(customer_id, "#txtCusMiddleNameMod");
    valide4 = validate_text_feild(first_name, "#txtCusSexMod");
    valide5 = validate_text_feild(last_name, "#txtCusWithdStatusMod");
    //valide6 = validate_text_feild(middle_name, "#txtCusDepositStatusMod");
    valide7 = validate_text_feild(gender, "#txtCusProductMod");
    valide8 = validate_text_feild(msisdn, "#txtCusStatusMod");

    if( valide3 && valide4 && valide5 && valide7 && valide8 ){
      show_loader_modal();
      formData = {
          "id": customer_id,
          "first_name": first_name,
          "last_name": last_name,
          "middle_name": middle_name,
          "gender": gender,
          "msisdn": msisdn,
      }
      console.log(formData);
      $.postJSON("/vouchers/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // filterCustomers();
            // $('#modifyCustomersModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnBlockCustomersReq').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");

    if( valide1 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id
          // "msisdn": msisdn,
          // "account": account
      }
      console.log(formData);
      $.postJSON("/vouchers/block_customer", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnEnableCustomersReq').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");

    if( valide1 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id
          // "msisdn": msisdn,
          // "account": account
      }
      console.log(formData);
      $.postJSON("/vouchers/enable_customer", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnResetPinReq').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");

    if( valide1 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id
      }
      console.log(formData);
      $.postJSON("/vouchers/reset_pin", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function deactivate_customer_account(element_id) {

  var raw_data = $(element_id).html();

  var data = raw_data.split('|');

  console.log(data);

  $('#cusAccPlce').text(data[2]);
  $('#cusRequetsId').text(data[0]);

  $("#deactivatCustomersAccountModal").modal("show");
}

/**
*Handle enter key press event for password text field
*/
$('#btnDeactivateCustomerAccount').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();
    var account_req = $('#cusAccPlce').text();
    var account_id = $('#cusRequetsId').text();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");
    valide4 = validate_text_feild(account_req, "#cusAccPlce");
    valide5 = validate_text_feild(account_id, "#cusRequetsId");

    if( valide1 && valide4 && valide5 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id,
          // "msisdn": msisdn,
          // "account": account,
          "account_req": account_req,
          "account_id": account_id

      }
      console.log(formData);
      $.postJSON("/vouchers/deactivate_customer_account", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function activate_customer_account(element_id) {

  var raw_data = $(element_id).html();

  var data = raw_data.split('|');

  console.log(data);

  $('#cusAccPlce1').text(data[2]);
  $('#cusRequetsId1').text(data[0]);

  $("#activatCustomersAccountModal").modal("show");
}

/**
*Handle enter key press event for password text field
*/
$('#btnActivateCustomerAccount').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();
    var account_req = $('#cusAccPlce1').text();
    var account_id = $('#cusRequetsId1').text();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");
    valide4 = validate_text_feild(account_req, "#cusAccPlce1");
    valide5 = validate_text_feild(account_id, "#cusRequetsId1");

    if( valide1 && valide4 && valide5 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id,
          // "msisdn": msisdn,
          // "account": account,
          "account_req": account_req,
          "account_id": account_id

      }
      console.log(formData);
      $.postJSON("/vouchers/activate_customer_account", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function approve_customer_request(request_id) {

  $('#cusRequetsId2').text(request_id);

  $("#approveCustomersRequestModal").modal("show");
}

/**
*Handle enter key press event for password text field
*/
$('#btnApproveCustomerRequest').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();
    var request_id = $('#cusRequetsId2').text();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");
    valide4 = validate_text_feild(request_id, "#cusAccPlce2");

    if( valide4 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id,
          // "msisdn": msisdn,
          // "account": account,
          "request_id": request_id,
      }
      console.log(formData);
      $.postJSON("/vouchers/approve_customer_request", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function details_customer_request(request_id){
    var formData = {
        'request_id': request_id
    };

    console.log(formData)
    show_loader();

    $.postJSON("/vouchers/request/details", formData, function(data){
        console.log(data);
        // if (data.code == "00") {
          hide_loader();
          load_request_detail_modal(data);
        // }

        // else if(data.code == "01"){
        //   hide_loader();
        //   $('#txtPassword').val("");
        //   displayErrorMsg(data.msg); //display Error message
        // }

        // else if(data.code == "02"){
        //   hide_loader();
        //   $('#txtPassword').val("");
        //   displayErrorMsg(data.msg); //display Error message
        // }

        // else{
        //   hide_loader();
        //   $('#txtPassword').val("");
        // }
      });

}

function load_request_detail_modal(data) {

  // $('#cusRequetsId3').text(request_id);
$('#txtCusFirstNameDet').val(data['new_fname'])
$('#txtCusLastNameDet').val(data['new_lname'])
$('#txtCusMiddleNameDet').val(data['new_mname'])
$('#txtCusGenderDet').val(data['new_gender'])
$('#txtCusDobDet').val(data['dob'])
$('#txtCusRegionDet').val(data['region'])
$('#txtCusCityDet').val(data['city'])
$('#txtCusMsisdnDet').val(data['customer_msisdn'])
$('#txtCusAccountDet').val(data['customer_account'])

  $("#detailsCustomersRequestModal").modal("show");
}


function decline_customer_request(request_id) {

  $('#cusRequetsId3').text(request_id);

  $("#declineCustomersRequestModal").modal("show");
}

/**
*Handle enter key press event for password text field
*/
$('#btnDeclineCustomerRequest').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    var msisdn = $('#txtOrgMsisdnMod').val();
    var account = $('#txtOrgAccontMod').val();
    var request_id = $('#cusRequetsId3').text();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    valide3 = validate_text_feild(account, "#txtOrgAccontMod");
    valide4 = validate_text_feild(request_id, "#cusAccPlce3s");

    if( valide4 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id,
          "msisdn": msisdn,
          "account": account,
          "request_id": request_id,
      }
      console.log(formData);
      $.postJSON("/vouchers/decline_customer_request", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});

/**
*Handle enter key press event for password text field
*/
$('#btnAddCustomersAccountReq').click(function(e) {
    e.preventDefault();    
    var customer_id = $('#txtCustomerIdMod').val();
    // var msisdn = $('#txtOrgMsisdnMod').val();
    // var account = $('#txtOrgAccontMod').val();
    var new_account = $('#txtCusNewAccountNumber').val();

    valide1 = validate_text_feild(customer_id, "#txtCustomerIdMod");
    // valide2 = validate_text_feild(msisdn, "#txtOrgMsisdnMod");
    // valide3 = validate_text_feild(account, "#txtOrgAccontMod");
    valide4 = validate_text_feild(new_account, "#txtCusNewAccountNumber");

    if( valide1 && valide4 ){
      show_loader_modal();
      formData = {
          "customer_id": customer_id,
          // "msisdn": msisdn,
          // "account": account,
          "new_account": new_account,
      }
      console.log(formData);
      $.postJSON("/vouchers/add_customer_account", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            window.location.reload();
            // $('#customersBlockModal').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});

$('#txtSearchValidation').on('change keyup', function(e) {
  e.preventDefault();   

$("#validation_page_id").val(1)

search_param = $("#txtSearchValidation").val();
if(search_param != ""){
  var formData = {
    'search_param': search_param
  };

  console.log(formData)

  // console.log(formData)
  show_loader_modal();

  $.postJSON("/validators/validation/search", formData, function(data){
      console.log(data);
      hide_loader_modal();
      load_serials_validation_table(data, "");
    });
  }
});

$('#btnFilterSerialValidation').click(function(e) {
  e.preventDefault();   

$("#validation_page_id").val(1);

fromdate = $("#mfromdate").val();
todate = $("#mtodate").val();
branch = $("#mBranch").val();

nextpage = parseInt($("#validation_page_id").val())

if (nextpage > 1) {
  nextpage -= 1;
}else{
  nextpage = 1;
}

var formData = {
      'page': nextpage - 1,
      'fromdate': fromdate,
      'todate': todate,
      'user_branch': branch
    };

  console.log(formData)

  show_loader_modal();

  $.postJSON("/validators/validations", formData, function(data){
      console.log(data);
      $("#mfromdate").val("");
      $("#mtodate").val("");
      if (data.history != null) {
        hide_loader_modal();
        load_serials_validation_table(data.history, "");
        $("#serialValidationFilter").modal("hide");
      }

      else{
        hide_loader_modal();
        displayErrorMsg("Failed to Get data"); //display Error message
      }
    });

});

function paginateValidations(arrow){
    var nextpage = parseInt($("#validation_page_id").val());
    var total_pages = parseInt($("#validation_tot_pages").val());

    //NEXT PAGE
    if(arrow == "next"){
      if(nextpage < total_pages){
      //   var formData = {
      //     'page': nextpage,
      //     'status': "All",
      //     'fromdate': "",
      //     "todate": ""
      // };

      } else{
        return
      }

    } else if(arrow == "prev"){ //PREVIOUS PAGE
      if(nextpage > 1){
        nextpage -= 2;
        // if (nextpage > 1) {
        //   nextpage -= 2;
        // }else{
        //   nextpage = 1;
        // }
    
      //   var formData = {
      //     'page': nextpage -1,
      //     'status': "All",
      //     'fromdate': "",
      //     "todate": ""
      // };
    }else{
      return
    }

    } else{ //CURRENT PAGE

      nextpage -= 1
      // if (nextpage > 1) {
      //   nextpage = nextpage;
      // }else{
      //   nextpage = 1;
      // }
    
      //   var formData = {
      //       'page': nextpage - 1,
      //       'fromdate': "",
      //       'todate': "",
      //       'status': "All"
      //   };
      }

      var formData = {
        'page': nextpage,
        'user_branch': "Non",
        'fromdate': "",
        "todate": ""
    };
      console.log(formData)
  
      // console.log(formData)
      show_loader();
  
      $.postJSON("/validators/validations", formData, function(data){
        console.log(data);
        if (data.history != null) {
          hide_loader();
          load_serials_validation_table(data.history, arrow);
        }
  
        else{
          hide_loader();
        }
      });
    }

function load_serials_validation_table(detail, operator){
  console.log(detail)
    
      tblBodyHtml = ""
      resp = ""
      if(detail.length == 0){
        tblBodyHtml += 
        tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
        '<td style="color: #FF6A13; font-weight: bolder"></td>'+
        '<td></td>'+
        '<td></td>'+
        '<td>No Record Found</td>'+
        '<td></td>'+
        '<td></td>'
        '<td></td>'
    '</tr>';
      } 

      for (var i = 0; i < detail.length; i++) {
        
        tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                    '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].user_name +'</td>'+
                    '<td>'+ detail[i].user_msisdn+'</td>'+
                    '<td>'+ detail[i].user_branch+'</td>'+
                    '<td>'+ detail[i].serial_no+'</td>'+
                    '<td>'+ detail[i].status_details+'</td>'+
                    '<td>'+ detail[i].user_mno +'</td>'+
                    '<td>'+ detail[i].date_created.substring(0, (detail[i].date_created.length - 3)) +'</td>'
                '</tr>';
      }
    
      $('#serialValidationTblBody').html("");
      $('#serialValidationTblBody').html(tblBodyHtml);
    
      nextpage = parseInt($("#validation_page_id").val());
      total_pages = parseInt($("#validation_tot_pages").val());
    
      if (operator == "next") {
        if(nextpage >= total_pages){
        }else{ $("#validation_page_id").val(nextpage+1);
      }
      }else if(operator == "prev"){
        if((nextpage -1 ) <= 0){
          $("#validation_page_id").val(1);
        }else{
          $("#validation_page_id").val((parseInt(nextpage)-1));
    
        }
      } else{
    
      }
    }

function get_validator_details(email) {
  show_loader();

  formData = {
    "email": email,
  }
  console.log(formData);
  $.postJSON("/validators/getValidator", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtFirstnameAdminMod').val(data.data.first_name);
          $('#txtLastnameAdminMod').val(data.data.last_name);
          $('#txtPhoneAdminMod').val(data.data.msisdn);
          $('#txtEmailAdminMod').val(data.data.email);
          $('#txtBranchAdminMod').val(data.data.branch);

          hide_loader();
          $("#modifyValidator").modal("show");
        }

        else if(data.code == "01"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
        }
    });
}

$('#btnUpdateValidator').click(function(e) {
  e.preventDefault();    
  var firstname = $('#txtFirstnameAdminMod').val();
  var lastname = $('#txtLastnameAdminMod').val();
  var phone = $('#txtPhoneAdminMod').val();
  var email = $('#txtEmailAdminMod').val();
  var branch = $('#txtBranchAdminMod').val();

  valide1 = validate_text_feild(firstname, "#txtFirstnameAdminMod", "name");
  valide2 = validate_text_feild(lastname, "#txtLastnameAdminMod", "name");
  valide4 = validate_text_feild(phone, "#txtPhoneAdminMod", "phone");
  valide5 = validate_text_feild(email, "#txtEmailAdminMod", "email");
  valide6 = validate_text_feild(branch, "#txtBranchAdminMod");

  formData = {
        "first_name": firstname,
        "last_name": lastname,
        "msisdn": phone,
        "email": email,
        "branch": branch
    }
    console.log(formData);

  if( valide1 && valide2 && valide4 && valide5 && valide6){
    show_loader_modal();
    $.postJSON("/validators/update", formData, function(data){
      console.log(data);
      if (data.code == "00") {
        hide_loader_modal();
        displaySucessMsgModal(data.msg);
        setTimeout(function () {
          $("#modifyValidator").modal("hide");
        }, 4000);
        window.location.reload(true);
        
      }

      else if(data.code == "01"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else if(data.code == "02"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else{
        hide_loader_modal();
      }
    });
}
});

function delete_validator(request_id) {

  $('#validatorId').text(request_id);

  $("#deleteValidatorModal").modal("show");
}

/**
*Handle btn delete validator request
*/
$('#btnDeleteValidatorRequest').click(function(e) {
    e.preventDefault();    
    var validator_id = $('#validatorId').text();

    if( validator_id != "" || validator_id != undefined){
      show_loader_modal();
      formData = {
          "validator_id": validator_id,
      }
      console.log(formData);
      $.postJSON("/validators/delete", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            $('#deleteValidatorModal').modal("hide");
            window.location.reload(true)
          }, 3000)
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});

/**
*Handle enter key press event for add validator
*/
$('#btnAddValidator').click(function(e) {
  e.preventDefault();    
  var firstname = $('#txtFirstnameAdmin').val();
  var lastname = $('#txtLastnameAdmin').val();
  var phone = $('#txtPhoneAdmin').val();
  var email = $('#txtEmailAdmin').val();
  var branch = $('#txtBranchAdmin').val();

  valide1 = validate_text_feild(firstname, "#txtFirstnameAdmin", "name");
  valide2 = validate_text_feild(lastname, "#txtLastnameAdmin", "name");
  valide3 = validate_text_feild(phone, "#txtPhoneAdmin", "phone");
  valide4 = validate_text_feild(email, "#txtEmailAdmin", "email");
  valide5 = validate_text_feild(branch, "#txtBranchAdmin");

  if( valide1 && valide2 && valide3 && valide4){
    show_loader_modal();
    formData = {
        "first_name": firstname,
        "last_name": lastname,
        "msisdn": phone,
        "email": email,
        "branch": branch
    };
    console.log(formData);
    $.postJSON("/validators/add", formData, function(data){
      console.log(data);
      if (data.code == "00") {

        $('#txtFirstnameAdmin').val("");
        $('#txtLastnameAdmin').val("");
        $('#txtUsernameAdmin').val("");
        $('#txtPhoneAdmin').val("");
        $('#txtEmailAdmin').val("");

        hide_loader_modal();
        displaySucessMsgModal(data.msg);
        $('#addadmin').modal("hide");
        window.location.reload(true);

      }

      else if(data.code == "01"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else if(data.code == "02"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else{
        hide_loader_modal();
      }
    });
}
});

$('#btnFilterValidators').click(function(e) {
  e.preventDefault();   

$("#validators_page_id").val(1)

var branch = $("#mtxtBranchFilter").val();
var nextpage = parseInt($("#validators_page_id").val());

// MAKING SURE TO CLEAR INPUT
// $("#mtxtBranchFilter").val("");
// $("#mtxtSerialStatusFilter").val("");

if (nextpage > 1) {
  nextpage -= 1;
}else{
  nextpage = 1;
}

var formData = {
      'page': nextpage - 1,
      'branch': branch
};

  console.log(formData)

  // console.log(formData)
  show_loader_modal();

  $.postJSON("/validators/", formData, function(data){
      console.log(data);
      if (data.validators != null) {
        hide_loader_modal();
        load_validators_table(data.validators, "");
        $("#validatorsFilter").modal("hide");
      }

      else{
        hide_loader_modal();
        displayErrorMsg("No Record Found"); //display Error message
      }
    });

});

function load_validators_table(detail, operator){
  console.log(detail)
  // get_institutions();
  tblBodyHtml = ""
  resp = ""
if(detail.length == 0){
  tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                '<td></td>'+
                '<td></td>'+
                '<td></td>'+
                '<td>No Record Found</td>'+
                '<td></td>'+
                '<td></td>'+
                '<td></td>'+
            '</tr>';
}

  for (var i = 0; i < detail.length; i++) {

    tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].first_name +'</td>'+
                '<td>'+ detail[i].last_name +'</td>'+
                '<td>'+ detail[i].email +'</td>'+
                '<td>'+ detail[i].msisdn +'</td>'+
                '<td>'+ detail[i].branch +'</td>'+
                '<td>'+ detail[i].date_created +'</td>'+
                '<td style="color: #108E53;"><a onclick="get_validator_details(\''+ detail[i].email +'\')">Edit</a> | <a onclick="delete_validator('+detail[i].validator_id+')">Delete</a></td>'+
            '</tr>';
  }

  $('#validatorsTblBody').html("");
  $('#validatorsTblBody').html(tblBodyHtml);

  nextpage = parseInt($("#validators_page_id").val());
  total_pages = parseInt($("#validators_tot_pages").val());

  if (operator == "next") {
    if(nextpage >= total_pages){
    }else{ $("#validators_page_id").val(nextpage+1);
  }
  }else if(operator == "prev"){
    if((nextpage -1 ) <= 0){
      $("#validators_page_id").val(1);
    }else{
      $("#validators_page_id").val((parseInt(nextpage)-1));

    }
  } else{

  }
  
}

function paginateValidators(arrow){
  var nextpage = parseInt($("#validators_page_id").val());
  var total_pages = parseInt($("#validators_tot_pages").val());

  //NEXT PAGE
  if(arrow == "next"){
    if(nextpage < total_pages){

    } else{
      return
    }

  } else if(arrow == "prev"){ //PREVIOUS PAGE
    if(nextpage > 1){
      nextpage -= 2;
  }else{
    return
  }

  } else{ //CURRENT PAGE

    nextpage -= 1
    }

    var formData = {
      'page': nextpage,
      'branch': "None"
  };
    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/validators/", formData, function(data){
      console.log(data);
      if (data.validators != null) {
        hide_loader();
        load_validators_table(data.validators, arrow);
      }

      else{
        hide_loader();
      }
    });
  }
/* Handle assign serials to branch button click event
*/
$('#btnAssignSerialsToBranch').click(function(e) {
  e.preventDefault();    
  var min_range = $('#mtxtminRange').val();
  var max_range = $('#mtxtmaxRange').val();
  var branch = $('#mtxtBranch').val();
  var bulk_id = $('#mtxtbulkSerialId').val();
  var min = parseInt($('#mtxtmin').val(), 10);
  var max = parseInt($('#mtxtmax').val(), 10); 
  console.log(parseInt(min_range, 10) + "min " + min);

  if(parseInt(min_range, 10) < min || parseInt(min_range, 10) > max || parseInt(max_range, 10) > max || parseInt(max_range, 10) < min){
    displaySucessMsgModal("Oops invalid range selected");
  } else{
  valide1 = validate_text_feild(min_range, "#mtxtminRange", "number");
  valide2 = validate_text_feild(max_range, "#mtxtmaxRange", "number");
  //valide3 = validate_text_feild(branch, "#mtxtBranch", "alphanumeric");
  valide3 = validate_text_feild(bulk_id, "#mtxtbulkSerialId", "alphanumeric");

  formData = {
        "bulk_id": bulk_id,
        "minRange": min_range,
        "maxRange": max_range,
        "branch_assigned": branch
    }
    console.log(formData);

  if( valide1 && valide2 && valide3){
    show_loader_modal();
    $.postJSON("/vouchers/assign", formData, function(data){
      console.log(data);
      if (data.code == "00") {
        hide_loader_modal();
        displaySucessMsgModal(data.msg);
        setTimeout(function () {
          $("#assignBranchModal").modal("hide");
        }, 4000);
        //window.location.reload(true);
        serialsCurr();
        
      }

      else if(data.code == "01"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else if(data.code == "02"){
        hide_loader_modal();
        displayErrorMsgModal(data.msg); //display Error message
      }

      else{
        hide_loader_modal();
      }
    });
}
}
});

$('#btnFilterSerials').click(function(e) {
  e.preventDefault();   

$("#page_id").val(1)

var serial_status = $("#mtxtSerialStatusFilter").val();
var branch = $("#mtxtBranchFilter").val();
var bulk_id = $('#mtxtbulkSerialId').val();
var nextpage = parseInt($("#page_id").val());

// MAKING SURE TO CLEAR INPUT
// $("#mtxtBranchFilter").val("");
// $("#mtxtSerialStatusFilter").val("");

if (nextpage > 1) {
  nextpage -= 1;
}else{
  nextpage = 1;
}

var formData = {
      'page': nextpage - 1,
      'serial_status': serial_status,
      'branch_assigned': branch
  };

  console.log(formData)

  // console.log(formData)
  show_loader_modal();

  $.postJSON("/vouchers/" + bulk_id, formData, function(data){
      console.log(data);
      if (data.voucher_details != null) {
        hide_loader_modal();
        load_serials_table(data.voucher_details, "plus");
        $("#serialFilter").modal("hide");
      }

      else{
        hide_loader_modal();
        displayErrorMsg(data.msg); //display Error message
      }
    });

});

function serialsCurr(){

  var bulk_id = $('#mtxtbulkSerialId').val();
  var nextpage = parseInt($("#page_id").val());

  var formData = {
    'page': nextpage-1,
    'serial_status': "",
    'branch_assigned': ""
};

console.log(formData)

// console.log(formData)
show_loader();

$.postJSON("/vouchers/" + bulk_id, formData, function(data){
  console.log(data);
  if (data.voucher_details != null) {
    hide_loader();
    load_serials_table(data.voucher_details, "");
    $("#serialFilter").modal("hide");
  }

  else{
    hide_loader();
    displayErrorMsg(data.msg); //display Error message
  }
});

}

function serialsNext(){

  var bulk_id = $('#mtxtbulkSerialId').val();

  var nextpage = parseInt($("#page_id").val());
  var total_pages = parseInt($("#tot_pages").val());
  if(nextpage < total_pages){

  var formData = {
        'page': nextpage,
        'serial_status': "",
        'branch_assigned': ""
    };

    console.log(formData)

    // console.log(formData)
    show_loader_modal();

    $.postJSON("/vouchers/" + bulk_id, formData, function(data){
      console.log(data);
      if (data.voucher_details != null) {
        hide_loader_modal();
        load_serials_table(data.voucher_details, "plus");
        $("#serialFilter").modal("hide");
      }

      else{
        hide_loader_modal();
        displayErrorMsg(data.msg); //display Error message
      }
    });
  }
}

function serialsPrev(){

  var bulk_id = $('#mtxtbulkSerialId').val();

  var nextpage = parseInt($("#page_id").val());

  if(nextpage > 1){
    if (nextpage > 1) {
      nextpage -= 1;
    }else{
      nextpage = 1;
    }

    var formData = {
          'page': nextpage - 1,
          'serial_status': "",
          'branch_assigned': ""
      };

      console.log(formData)
      show_loader_modal();

      $.postJSON("/vouchers/" + bulk_id, formData, function(data){
        console.log(data);
        if (data.voucher_details != null) {
          hide_loader_modal();
          load_serials_table(data.voucher_details, "minus");
          $("#serialFilter").modal("hide");
        }

        else{
          hide_loader_modal();
          displayErrorMsg(data.msg); //display Error message
        }
      });
  }
}

function load_serials_table(detail, operator){

  console.log(detail);

  tblBodyHtml = ""
  resp = ""
  var len = detail.length;
  if(len > 0){
    console.log(detail[len-1].batch_id);
    $("#mtxtmaxRange").val(detail[len-1].batch_id);
    $("#mtxtminRange").attr('max', detail[len-1].batch_id)
    $("#mtxtmaxRange").attr('max', detail[len-1].batch_id)
    $("#mtxtmax").val(detail[len-1].batch_id);

  }
  for (var i = 0; i < detail.length; i++) {
    if(i == 0){
      $("#mtxtminRange").val(detail[i].batch_id)
      $("#mtxtminRange").attr('min', detail[i].batch_id)
      $("#mtxtmaxRange").attr('min', detail[i].batch_id)
      $("#mtxtmin").val(detail[i].batch_id)

    } 
    var expiry = "";
    if(detail[i].expiry_date == null){
      expiry = "Not Applicable"
    } else{
      expiry = detail[i].expiry_date;
    }

    tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].batch_id +'</td>'+
                '<td>'+ detail[i].date_approved.substring(0, (detail[i].date_approved.length - 3)) +'</td>'+
                '<td>'+ detail[i].hashed_serial_number +'</td>'+
                '<td>'+ expiry +'</td>'+
                '<td>'+ detail[i].branch_assigned +'</td>'+
                '<td>'+ detail[i].serial_status.toLowerCase() +'</td>'
            '</tr>';
  }

  $('#serialsTblBody').html("");
  $('#serialsTblBody').html(tblBodyHtml);

  nextpage = parseInt($("#page_id").val());
  total_pages = parseInt($("#total_pages").val());

  if (operator == "plus") {
    if(nextpage >= total_pages){
    }else{ $("#page_id").val(nextpage+1);
  }
  }else if (operator =="minus"){
    if((nextpage -1 ) <= 0){
      $("#page_id").val(1);
    }else{
      $("#page_id").val((parseInt(nextpage)-1));

    }
  }else{

  }
}
$('#txtSearchSerials').on('change keyup', function(e) {
  e.preventDefault();   

$("#page_id").val(1)

search_param = $("#txtSearchSerials").val();

var formData = {
      'search_param': search_param
  };

  console.log(formData)

  // console.log(formData)
  show_loader_modal();

  $.postJSON("/vouchers/verify/search", formData, function(data){
      console.log(data);
      hide_loader_modal();
      load_serials_verification_table(data, "");
    });

});

$('#btnFilterSerialVerification').click(function(e) {
  e.preventDefault();   

$("#verify_page_id").val(1);

fromdate = $("#mfromdate").val();
todate = $("#mtodate").val();
status = $("#mtxtStatus").val();

nextpage = parseInt($("#verify_page_id").val())

if (nextpage > 1) {
  nextpage -= 1;
}else{
  nextpage = 1;
}

var formData = {
      'page': nextpage - 1,
      'fromdate': fromdate,
      'todate': todate,
      'status': status
    };

  console.log(formData)

  show_loader_modal();

  $.postJSON("/vouchers/verification", formData, function(data){
      console.log(data);
      $("#mfromdate").val("");
      $("#mtodate").val("");
      if (data.history != null) {
        hide_loader_modal();
        load_serials_verification_table(data.history, "minus");
        $("#serialVerificationFilter").modal("hide");
      }

      else{
        hide_loader_modal();
        displayErrorMsg("Failed to Get data"); //display Error message
      }
    });

});

function load_serials_verification_table(detail, operator){
  // get_institutions();

  console.log(detail);

  tblBodyHtml = ""
  resp = ""
  if(detail.length == 0){
    tblBodyHtml += 
    tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
    '<td style="color: #FF6A13; font-weight: bolder"></td>'+
    '<td></td>'+
    '<td>No Record Found</td>'+
    '<td></td>'+
    '<td></td>'
'</tr>';
  }
  for (var i = 0; i < detail.length; i++) {
    
    tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].user_msisdn +'</td>'+
                '<td>'+ detail[i].serial_no+'</td>'+
                '<td>'+ detail[i].status.toLowerCase() +'</td>'+
                '<td>'+ detail[i].user_mno +'</td>'+
                '<td>'+ detail[i].date_created.substring(0, (detail[i].date_created.length - 3)) +'</td>'
            '</tr>';
  }

  $('#serialVerifyTblBody').html("");
  $('#serialVerifyTblBody').html(tblBodyHtml);

  nextpage = parseInt($("#verify_page_id").val());
  total_pages = parseInt($("#verify_total_pages").val());

  if (operator == "plus") {
    if(nextpage >= total_pages){
    }else{ $("#verify_page_id").val(nextpage+1);
  }
  }else if(operator == "minus"){
    if((nextpage -1 ) <= 0){
      $("#verify_page_id").val(1);
    }else{
      $("#verify_page_id").val((parseInt(nextpage)-1));

    }
  } else{

  }
}

function serialsVerifyCurr(){

  var nextpage = parseInt($("#verify_page_id").val());

  if (nextpage > 1) {
    nextpage = nextpage;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': "",
        'todate': "",
        'status': "All"
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/verification", formData, function(data){
      console.log(data);
      if (data.history != null) {
        hide_loader();
        load_serials_verification_table(data.history, "");
        $("#serialVerificationFilter").modal("hide");
      }

      else{
        hide_loader();
        displayErrorMsg(data.msg); //display Error message
      }
    });

}

function serialsVerifyNext(){
console.log("in serial verify next")
  var nextpage = parseInt($("#verify_page_id").val());
  var total_pages = parseInt($("#verify_total_pages").val());
  if(nextpage < total_pages){

  var formData = {
        'page': nextpage,
        'status': "All",
        'fromdate': "",
        "todate": ""
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/vouchers/verification", formData, function(data){
      console.log(data);
      if (data.history != null) {
        hide_loader();
        load_serials_verification_table(data.history, "plus");
        $("#serialVerificationFilter").modal("hide");
      }

      else{
        hide_loader();
        displayErrorMsg(data.msg); //display Error message
      }
    });
  }
}

function serialsVerifyPrev(){

  var nextpage = parseInt($("#verify_page_id").val());

  if(nextpage > 1){
    if (nextpage > 1) {
      nextpage -= 1;
    }else{
      nextpage = 1;
    }

    var formData = {
      'page': nextpage -1,
      'status': "All",
      'fromdate': "",
      "todate": ""
  };

  console.log(formData)
  show_loader();

      $.postJSON("/vouchers/verification", formData, function(data){
        console.log(data);
        if (data.history != null) {
          hide_loader();
          load_serials_verification_table(data.history, "minus");
          $("#serialVerificationFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });
  }
}
/**
*Handle enter key press event for add admin button
*/
$('#btnAddAdmin').click(function(e) {
    e.preventDefault();    
    var firstname = $('#txtFirstnameAdmin').val();
    var lastname = $('#txtLastnameAdmin').val();
    var username = $('#txtUsernameAdmin').val();
    var phone = $('#txtPhoneAdmin').val();
    var email = $('#txtEmailAdmin').val();
    var group = $('#txtGroupAdmin').val();
    var branch = $('#txtBranchAdmin').val();

    valide1 = validate_text_feild(firstname, "#txtFirstnameAdmin", "name");
    valide2 = validate_text_feild(lastname, "#txtLastnameAdmin", "name");
    valide3 = validate_text_feild(username, "#txtUsernameAdmin", "alphanumeric");
    valide4 = validate_text_feild(phone, "#txtPhoneAdmin", "phone");
    valide5 = validate_text_feild(email, "#txtEmailAdmin", "email");
    valide6 = validate_text_feild(group, "#txtGroupAdmin");
    valide7 = validate_text_feild(branch, "#txtBranchAdmin");

    if( valide1 && valide2 && valide3 && valide4 && valide5 && valide6 && valide7 ){
      show_loader_modal();
      formData = {
          "first_name": firstname,
          "last_name": lastname,
          "username": username,
          "msisdn": phone,
          "email": email,
          "user_right_id": group,
          "branch": branch
      }
      console.log(formData);
      $.postJSON("/admins/add", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtFirstnameAdmin').val("");
          $('#txtLastnameAdmin').val("");
          $('#txtUsernameAdmin').val("");
          $('#txtPhoneAdmin').val("");
          $('#txtEmailAdmin').val("");

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterAdmins();
          $('#addadmin').modal("hide");
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnUpdateAdmin').click(function(e) {
    e.preventDefault();    
    var firstname = $('#txtFirstnameAdminMod').val();
    var lastname = $('#txtLastnameAdminMod').val();
    var username = $('#txtUsernameAdminMod').val();
    var phone = $('#txtPhoneAdminMod').val();
    var email = $('#txtEmailAdminMod').val();
    var group = $('#txtGroupAdminMod').val();
    var branch = $('#txtBranchAdminMod').val();

    valide1 = validate_text_feild(firstname, "#txtFirstnameAdminMod", "name");
    valide2 = validate_text_feild(lastname, "#txtLastnameAdminMod", "name");
    valide3 = validate_text_feild(username, "#txtUsernameAdminMod");
    valide4 = validate_text_feild(phone, "#txtPhoneAdminMod", "phone");
    valide5 = validate_text_feild(email, "#txtEmailAdminMod", "email");
    valide6 = validate_text_feild(group, "#txtGroupAdminMod");
    valide7 = validate_text_feild(branch, "#txtBranchAdminMod");

    formData = {
          "first_name": firstname,
          "last_name": lastname,
          "username": username,
          "msisdn": phone,
          "email": email,
          "user_right_id": group,
          "branch": branch
      }
      console.log(formData);

    if( valide1 && valide2 && valide3 && valide4 && valide5 && valide6 && valide7 ){
      show_loader_modal();
      $.postJSON("/admins/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function () {
            $("#modifyadmin").modal("hide");
          }, 4000);
          filterAdmins();
          
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnActivateAdmin').click(function(e) {
    e.preventDefault();    
    var firstname = $('#txtFirstnameAdminMod').val();
    var lastname = $('#txtLastnameAdminMod').val();
    var username = $('#txtUsernameAdminMod').val();
    var phone = $('#txtPhoneAdminMod').val();
    var email = $('#txtEmailAdminMod').val();
    var group = $('#txtGroupAdminMod').val();
    var branch = $('#txtBranchAdminMod').val();

    valide1 = validate_text_feild(firstname, "#txtFirstnameAdminMod", "name");
    valide2 = validate_text_feild(lastname, "#txtLastnameAdminMod", "name");
    valide3 = validate_text_feild(username, "#txtUsernameAdminMod");
    valide4 = validate_text_feild(phone, "#txtPhoneAdminMod", "phone");
    valide5 = validate_text_feild(email, "#txtEmailAdminMod", "email");
    valide6 = validate_text_feild(group, "#txtGroupAdminMod");
    valide7 = validate_text_feild(branch, "#txtBranchAdminMod");

    formData = {
          "first_name": firstname,
          "last_name": lastname,
          "username": username,
          "msisdn": phone,
          "email": email,
          "user_right_id": group,
          "branch": branch,
          "active": "1"
      }
      console.log(formData);

    if( valide1 && valide2 && valide3 && valide4 && valide5 && valide6 && valide7 ){
      console.log(formData);
      $.postJSON("/admins/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterAdmins();
          setTimeout(function(){
              $("#modifyadmin").modal("hide");
          }, 4000);
          
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnDeactivateAdmin').click(function(e) {
    e.preventDefault();    
    var firstname = $('#txtFirstnameAdminMod').val();
    var lastname = $('#txtLastnameAdminMod').val();
    var username = $('#txtUsernameAdminMod').val();
    var phone = $('#txtPhoneAdminMod').val();
    var email = $('#txtEmailAdminMod').val();
    var group = $('#txtGroupAdminMod').val();
    var branch = $('#txtBranchAdminMod').val();

    valide1 = validate_text_feild(firstname, "#txtFirstnameAdminMod", "name");
    valide2 = validate_text_feild(lastname, "#txtLastnameAdminMod", "name");
    valide3 = validate_text_feild(username, "#txtUsernameAdminMod");
    valide4 = validate_text_feild(phone, "#txtPhoneAdminMod", "phone");
    valide5 = validate_text_feild(email, "#txtEmailAdminMod", "email");
    valide6 = validate_text_feild(group, "#txtGroupAdminMod");
    valide7 = validate_text_feild(branch, "#txtBranchAdminMod");

    formData = {
          "first_name": firstname,
          "last_name": lastname,
          "username": username,
          "msisdn": phone,
          "email": email,
          "user_right_id": group,
          "branch": branch,
          "active": "0"
      }
      console.log(formData);

    if( valide1 && valide2 && valide3 && valide4 && valide5 && valide6 && valide7 ){
      show_loader_modal();
      $.postJSON("/admins/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterAdmins();
          setTimeout(function(){
              $("#modifyadmin").modal("hide");
          }, 3000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          filterAdmins();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function get_admin_details(username) {
  show_loader();

  formData = {
    "username": username,
  }

  $.postJSON("/admins/getadmin", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtFirstnameAdminMod').val(data.data.first_name);
          $('#txtLastnameAdminMod').val(data.data.last_name);
          $('#txtUsernameAdminMod').val(data.data.username);
          $('#txtPhoneAdminMod').val(data.data.msisdn);
          $('#txtEmailAdminMod').val(data.data.email);
          $('#txtGroupAdminMod').val(data.data.user_right_id);
          $('#txtBranchAdminMod').val(data.data.branch_code);

          hide_loader();
          $("#modifyadmin").modal("show");
        }

        else if(data.code == "01"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
        }
    });
}


/**
*Handle enter key press event for password text field
*/
$('#btnAdminChangePass').click(function(e) {
    e.preventDefault();    
    var oldPassword = $('#txtOldPassword').val();
    var nePassword = $('#txtNewPassword').val();
    var newPasswordRep = $('#txtNewPasswordrep').val();

    valide1 = validate_text_feild(oldPassword, "#txtOldPassword");
    valide2 = validate_text_feild(nePassword, "#txtNewPassword");
    valide3 = validate_text_feild(newPasswordRep, "#txtNewPasswordrep");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "oldPassword": oldPassword,
          "newPassword": nePassword,
          "newPasswordRep": newPasswordRep,
      }
      console.log(formData);
      $.postJSON("/admins/changepassword", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtOldPassword').val("");
          $('#txtNewPassword').val("");
          $('#txtNewPasswordrep').val("");

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnNewChangePass').click(function(e) {
    e.preventDefault();    
    var oldPassword = $('#txtOldPassword').val();
    var nePassword = $('#txtNewPassword').val();
    var newPasswordRep = $('#txtNewPasswordrep').val();

    valide1 = validate_text_feild(oldPassword, "#txtOldPassword");
    valide2 = validate_text_feild(nePassword, "#txtNewPassword");
    valide3 = validate_text_feild(newPasswordRep, "#txtNewPasswordrep");

    if( valide1 && valide2 && valide3 ){
      show_loader();
      formData = {
          "oldPassword": oldPassword,
          "newPassword": nePassword,
          "newPasswordRep": newPasswordRep,
      }
      console.log(formData);
      $.postJSON("/admins/changepassword", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtOldPassword').val("");
          $('#txtNewPassword').val("");
          $('#txtNewPasswordrep').val("");

          //setTimeout(function () {
            displaySucessMsg(data.msg);
            window.location = "/home/user";
          //});
          
        }

        else if(data.code == "01"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnAddAdminGroup').click(function(e) {
    e.preventDefault();    
    var groupname = $('#txtGroupName').val();
    var description = $('#txtGroupDescription').val();
    var roles = '';

    valide1 = validate_text_feild(groupname, "#txtGroupName");
    valide2 = validate_text_feild(description, "#txtGroupDescription");

    if ( $('#adminsRchk').is(':checked') == true ) {
        roles = roles +'A';
    } 
    if ( $('#mngGrpRchk').is(':checked') == true ) {
        roles = roles +'G';
    } 
    if ( $('#branchRchk').is(':checked') == true ) {
        roles = roles +'B';
    } 
    if ( $('#logsRchk').is(':checked') == true ) {
        roles = roles +'L';
    } 
    if ( $('#serialsRchk').is(':checked') == true ) {
        roles = roles + 'S';
    } 
        if ( $('#serialsUploadRchk').is(':checked') == true ) {
        roles = roles +'U';
    } 
        if ( $('#serialsApproveRchk').is(':checked') == true ) {
        roles = roles +'P';
    } 
       
    if ($('#serialsRchk').is(':checked') == false && ($('#serialsApproveRchk').is(':checked') == true  ||  $('#serialsUploadRchk').is(':checked') == true) ){
        roles = roles +'S';
    }  
    
    // if ( $('#intCsReqRchk').is(':checked') == true ) {
    //     roles= roles +'H';
    // } 
    // if ( $('#appCsReqRchk').is(':checked') == true ) {
    //     roles= roles +'I';
    // } 

    console.log(roles);

    if( valide1 && valide2 ){
      show_loader_modal();
      formData = {
          "name": groupname,
          "value": "400",
          "details": roles,
          "description": description
      }
      console.log(formData);
      $.postJSON("/admins/group/add", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtGroupName').val("");
          $('#txtGroupDescription').val("");
          $('input:checkbox').prop('checked', false);


          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterAdmins();
          setTimeout(function() {
              window.location.reload();
          }, 3000);
          // $('#addgroup').modal("hide");
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnUpdateAdminGroup').click(function(e) {
    e.preventDefault();    
    var groupname = $('#txtGroupNameMod').val();
    var description = $('#txtGroupDescriptionMod').val();
    var id = $('#txtGroupIdMod').val();
    var roles = '';

    valide1 = validate_text_feild(groupname, "#txtGroupNameMod", "name");
    valide2 = validate_text_feild(description, "#txtGroupDescriptionMod", "name");
    valide3 = validate_text_feild(id, "#txtGroupIdMod");

  
    if ( $('#adminsRchkMod').is(':checked') == true ) {
        roles = roles +'A';
    } 
    if ( $('#mngGrpRchkMod').is(':checked') == true ) {
        roles = roles +'G';
    } 
    if ( $('#branchRchkMod').is(':checked') == true ) {
        roles = roles +'B';
    } 
    if ( $('#logsRchkMod').is(':checked') == true ) {
        roles = roles +'L';
    } 
    if ( $('#serialsRchkMod').is(':checked') == true ) {
        roles = roles + 'S';
    } 
        if ( $('#serialsUploadRchkMod').is(':checked') == true ) {
        roles = roles +'U';
    } 
        if ( $('#serialsApproveRchkMod').is(':checked') == true ) {
        roles = roles +'P';
    } 

       if ($('#serialsRchkMod').is(':checked') == false && ($('#serialsApproveRchkMod').is(':checked') == true  ||  $('#serialsUploadRchkMod').is(':checked') == true) ){
        roles = roles +'S';
    }  
    
    console.log(roles);
    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "name": groupname,
          "value": "400",
          "details": roles,
          "description": description,
          "id": id
      }
      console.log(formData);
      $.postJSON("/admins/group/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtGroupNameMod').val("");
          $('#txtGroupDescriptionMod').val("");
          $('input:checkbox').prop('checked', false);


          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterAdmins();
          setTimeout(function() {
              window.location.reload();
          }, 4000);
          // $('#addgroup').modal("hide");
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function get_role_details(element_id) {
  show_loader();

  var raw_data = $(element_id).html();

  var data = raw_data.split('|');

  console.log(data);

  $('input:checkbox').prop('checked', false);

  $('#txtGroupNameMod').val(data[0]);
  $('#txtGroupDescriptionMod').val(data[1]);
  $('#txtUsernameAdminMod').val(data[2][0]);
  $('#txtGroupIdMod').val(data[3]);

  for (var i = data[2].length - 1; i >= 0; i--) {
    if (data[2][i] != '' && data[2][i] == 'A' ) {
        console.log(data[2][i]);
        $('#adminsRchkMod').prop('checked', true);
    } 
     if (data[2][i] != '' && data[2][i] == 'G' ) {
        console.log(data[2][i]);
        $('#mngGrpRchkMod').prop('checked', true);
    }
    if (data[2][i] != '' && data[2][i] == 'B' ) {
        console.log(data[2][i]);
        $('#branchRchkMod').prop('checked', true);
    } 
    if (data[2][i] != '' && data[2][i] == 'L' ) {
        console.log(data[2][i]);
        $('#logsRchkMod').prop('checked', true);
    } 
    if (data[2][i] != '' && data[2][i] == 'S' ) {
        console.log(data[2][i]);
        $('#serialsRchkMod').prop('checked', true);
    } 
    if (data[2][i] != '' && data[2][i] == 'U' ) {
        console.log(data[2][i]);
        $('#serialsUploadRchkMod').prop('checked', true);
    } 
    if (data[2][i] != '' && data[2][i] == 'P' ) {
        console.log(data[2][i]);
        $('#serialsApprovalRchkMod').prop('checked', true);
    } 
     
  }

  hide_loader();
  $("#updategroup").modal("show");
}


function hideRemarksField() {
  $('#txtRespsRemarks').val("");
  $('#txtRemarksblk').hide();
}


function approve_upload(request_id) {

  $('#filebulkId0').text(request_id);

  $("#approveFileModal").modal("show");

}

function decline_upload(request_id) {

  $('#filebulkId1').text(request_id);

  $("#declineFileModal").modal("show");
}

/**
*Handle enter key press event for password text field
*/
$('#btnDeclineFileRequest').click(function(e) {
    e.preventDefault();    
    var bulk_id = $('#filebulkId1').text();

    if( bulk_id != "" || bulk_id != undefined){
      show_loader_modal();
      formData = {
          "bulk_id": bulk_id,
      }
      console.log(formData);
      $.postJSON("/vouchers/uploads/decline", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            $('#declineFileModal').modal("hide");
            window.location.reload()
          }, 3000)
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnApproveFileRequest').click(function(e) {
    e.preventDefault();    
    var bulk_id = $('#filebulkId0').text();

    if( bulk_id != "" || bulk_id != undefined){
      show_loader_modal();
      formData = {
          "bulk_id": bulk_id,
      }
      console.log(formData);
      $.postJSON("/vouchers/uploads/approve", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            $('#approveFileModal').modal("hide");
            window.location.reload()
          }, 3000)
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


$('#btnDownloadFile').click(function(e) {
    e.preventDefault();    
    var bulk_id = $('#txtBulkId').text();

    if( bulk_id != "" || bulk_id != undefined){
      show_loader_modal();
      window.open("/uploads/download/"+bulk_id);
    }

});


/**
*Handle enter key press event for password text field
*/
$('#btnAddInstitution').click(function(e) {
    e.preventDefault();    
    var institutionName = $('#txtInstitutionNameAdd').val();
    var institutionName = $('#txtInstitutionShortNameAdd').val();
    var institutionDesc = $('#txtInstitutionDescriptionAdd').val();
    var institutionType = $('#txtInstitutionTypeAdd').val();

    valide1 = validate_text_feild(institutionName, "#txtInstitutionNameAdd");
    valide2 = validate_text_feild(institutionName, "#txtInstitutionShortNameAdd");
    valide3 = validate_text_feild(institutionDesc, "#txtInstitutionDescriptionAdd");
    valide4 = validate_text_feild(institutionType, "#txtInstitutionTypeAdd");

    if( valide1 && valide2 && valide3 && valide4 ){
      show_loader_modal();
      formData = {
          "name": institutionName,
          "shortName": institutionName,
          "description": institutionDesc,
          "institution_type": institutionType,
      }
      console.log(formData);
      $.postJSON("/institutions/add", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtInstitutionNameAdd').val("");
          $('#txtInstitutionShortNameAdd').val("");
          $('#txtInstitutionDescriptionAdd').val("");
          $('#txtInstitutionTypeAdd').val("");

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterInst();
          $('#addInstitutionModal').modal('hide');
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


/**
*Handle enter key press event for password text field
*/
$('#btnModInstitution').click(function(e) {
    e.preventDefault();    
    var institutionName = $('#txtInstitutionNameMod').val();
    var institutionName = $('#txtInstitutionShortNameMod').val();
    var institutionDesc = $('#txtInstitutionDescriptionMod').val();
    var institutionType = $('#txtInstitutionTypeMod').val();

    valide1 = validate_text_feild(institutionName, "#txtInstitutionNameMod");
    valide2 = validate_text_feild(institutionName, "#txtInstitutionShortNameMod");
    valide3 = validate_text_feild(institutionDesc, "#txtInstitutionDescriptionMod");
    valide4 = validate_text_feild(institutionType, "#txtInstitutionTypeMod");

    if( valide1 && valide2 && valide3 && valide4 ){
      show_loader_modal();
      formData = {
          "name": institutionName,
          "shortName": institutionName,
          "description": institutionDesc,
          "institution_type": institutionType,
      }
      console.log(formData);
      $.postJSON("/institutions/update", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          filterInst();
          $('#modifyInstitutionModal').modal('hide');
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function get_inst_details(isnt_shortname){
    var formData = {
        'shortName': isnt_shortname
    };

    // console.log(formData)
    show_loader();

    $.postJSON("/institutions/details", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_institution_modal(data.data);
        }

        else if(data.code == "01"){
          hide_loader();
          $('#txtPassword').val("");
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          $('#txtPassword').val("");
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
          $('#txtPassword').val("");
        }
      });

}


function load_institution_modal(detail){
    // get_institutions();

    console.log(detail)

    $('#txtInstitutionNameMod').val(detail['name']);
    $('#txtInstitutionShortNameMod').val(detail['shortName']);
    $('#txtInstitutionDescriptionMod').val(detail['description']);
    $('#txtInstitutionTypeMod').val(detail['institution_type']);

    $("#modifyInstitutionModal").modal("show");
}




/**
*Handle enter key press event for password text field
*/
$('#btnAddBranch').click(function(e) {
    e.preventDefault();    
    var branch_id = $('#txtBranchCode').val();
    var branch_acronym = $('#txtBranchAcronym').val();
    var branch_name = $('#txtBranchName').val();

    valide1 = validate_text_feild(branch_id, "#txtBranchCode");
    valide2 = validate_text_feild(branch_acronym, "#txtBranchAcronym");
    valide3 = validate_text_feild(branch_name, "#txtBranchName");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();

      // branch_code = branch_id + "-" + branch_acronym;
      branch_code = branch_id;

      formData = {
            "branch_id": branch_id,
            "branch_code": branch_code,
            "acronym": branch_acronym,
            "branch_name": branch_name,
        }
      console.log(formData);

      $.postJSON("/admins/branches/add", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          $('#txtBranchCode').val("");
          $('#txtBranchAcronym').val("");
          $('#txtBranchName').val("");

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          setTimeout(function() {
            // filterBranches();
            window.location.href="/admins";
            $('#addbranch').modal('hide');
          }, 4000);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function remove_branch(branch_id) {
  show_loader();

  formData = {
    "branch_id": branch_id,
  }

  $.postJSON("/admins/branches/remove", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader_modal();
          displaySucessMsg(data.msg);
          setTimeout(function() {
            filterBranches();
          }, 4000);
          
        }

        else if(data.code == "01"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }

        else{
          hide_loader();
        }
    });
}



function branchesNext(){

  nextpage = parseInt($("#page_id_bc").val());

    if (nextpage >= 1) {
      nextpage += 1 ;
    }

  var formData = {
        'page': nextpage - 1
    };

    console.log(formData)
    show_loader();

    $.postJSON("/admins/branches", formData, function(data){
        console.log(data);
        hide_loader();
        load_branches_table(data, "plus");
      });
}


function branchesPrev(){

  nextpage = parseInt($("#page_id_bc").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1
    };

    console.log(formData)

    show_loader();

    $.postJSON("/admins/branches", formData, function(data){
        console.log(data);
        hide_loader();
        load_branches_table(data, "minus");
      });
}

function branchesCurr(){

  nextpage = parseInt($("#page_id_bc").val())

  var formData = {
        'page': nextpage - 1
    };

    console.log(formData)

    show_loader();

    $.postJSON("/admins/branches", formData, function(data){
        console.log(data);
        hide_loader();
        load_branches_table(data, "");
      });

}

function filterBranches(){

  $("#page_id_bc").val(1)
  
  nextpage = parseInt($("#page_id_bc").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/admins/branches", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_branches_table(data.data, "");
          $("#branchesFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterBranches').click(function(e) {
    e.preventDefault();   

  $("#page_id_bc").val(1)

  nextpage = parseInt($("#page_id_bc").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }
  
  var formData = {
        'page': nextpage - 1,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/admins/branches", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_branches_table(data.data, "");
          $("#branchesFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnSerchbranch').click(function(e) {
  e.preventDefault();   
  // alert("Hello");

  $("#page_id_bc").val(1)

  searc_text = $("#txtSearchbc").val();

  var formData = {
        'search_param': searc_text
    };

    console.log(formData)

    // console.log(formData)
    if (searc_text != ''){
      show_loader();

      $.postJSON("/admins/branches/search", formData, function(data){
          console.log(data);
            hide_loader();
            load_branches_table(data, "");
      });
    }
});

function load_branches_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    if (detail.length == 0) {
      return;
    }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13">'+ detail[i].acronym +'</td>'+
                  '<td>'+ detail[i].branch_name +'</td>'+
                  '<td>'+ detail[i].branch_code +'</td>'+
              '</tr>';
    }

    $('#branchesTblBody').html("");
    $('#branchesTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id_bc").val());

    if (operator == "plus") {
      $("#page_id_bc").val(nextpage+1);
    }else if (operator == "") {
      $("#page_id_bc").val(nextpage);
    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id_bc").val(1);
      }else{
        $("#page_id_bc").val((parseInt(nextpage)-1));
      }
    }
    

}

/**
*Handle enter key press event for password text field
*/
$('#btnTopupManilla').click(function(e) {
    e.preventDefault();    
    var fullname = $('#txtTopupfullNameMil').val();
    var email = $('#txtTopupfullEmailMil').val();
    var amount = $('#txtTopupAmountMil').val();

    valide1 = validate_text_feild(fullname, "#txtTopupfullNameMil");
    valide2 = validate_text_feild(email, "#txtTopupfullEmailMil");
    valide3 = validate_text_feild(amount, "#txtTopupAmountMil", "number");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "name": fullname,
          "email": email,
          "amount": amount,
      }
      console.log(formData);
      $.postJSON("/topup/manilla/initiate", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          console.log("Redirecting");
          redirect_to_manilla(data.data);
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function redirect_to_manilla(data){
  // alert("In manilla redirect");

  console.log(data);
  // console.log(campaign);

  //var return_url = 'http://localhost/store/success/';
  //var cancel_url = 'http://portals.nsano.com:9000/store/cancel/';
  var return_url = 'http://portals.nsano.com:5505/topup/manilla/callback';
  var cancel_url = 'http://portals.nsano.com:5505/topup/manilla/callback';
  //var checkout_url = 'https://manilla.nsano.com/checkout/';
  var checkout_url = '/topup/manilla';
  //var order_id = 'xxxxxxxxxxxxxx16CF'.replace(/[xy]/g, function(c) {var r = Math.random()*16|0,v=c=='x'?r:r&0x3|0x8;return v.toString(16);});
  //var order_id = data.manilla.order_id
  // var merchant_id = "300463693816"; // test for Bella shop
  // var merchant_id = "301152115708";

  itemInputs = '';
  itemInputs += '<input type="text" name="item_code[]" value="ITM-1" />' +
                '<input type="text" name="description[]" value="BulkPay Account Topup for ' + data.institution_shortName + '" />' +
                '<input type="text" name="cost[]" value="' + data.manilla.amount + '" />';

  var form = $('<form action="' + checkout_url + '" method="POST" style="display:none">' +

    //'<input type="text" name="merchant_id" value="300386016350"/>' +
    '<input type="text" name="merchant_id" value="'+ data.manilla.merchant_id +'" />' +
    //'<input type="text" name="merchant_id" value="300463693815" />' +
    //'<input type="text" name="order_id" value="ord-00234" />' +
    '<input type="text" name="order_id" value="'+ data.manilla.order_id +'" />' +
    '<input type="text" name="description" value="BulkPay Account Topup for ' + data.institution_shortName + '" />' +
    itemInputs +
    '<input type="text" name="cust_firstname" value="'+ data.first_name +'" />' +
    '<input type="text" name="cust_lastname" value="'+ data.last_name +'" />' +
    '<input type="text" name="cust_email" value="'+ data.email +'" />' +
    '<input type="text" name="cust_phone" value="'+ data.msisdn +'" />' +
    '<input type="text" name="cust_address" value="" />' +
    '<input type="text" name="cust_zip" value="" />' +
    '<input type="text" name="cust_city" value="" />' +
    '<input type="text" name="cust_country" value="" />' +
    '<input type="text" name="amount" value="'+ data.manilla.amount +'" />' +
    //'<input type="text" name="amount" value="500" />' +
    //'<input type="text" name="amount" value="' + $("#t_amount").html() + '" />' +
    '<input type="text" name="currency" value="GHS" />' +
    //'<input type="text" name="currency" value="FCFA" />' +
    '<input type="text" name="return_url" value="' + return_url + '" />' +
    '<input type="text" name="cancel_url" value="' + cancel_url + '" />' +

    //'<input type="text" name="checksum" value="75640IS67QU67af9c5871a6b328ec3494679db" />' +
    //'<input type="text" name="checksum" value="a016ceMzhvI743ae4f78fcfee4d3b616e470a2" />' +
    // '<input type="text" name="checksum" value="a841fiAHhhtadd0612ccbf0e5eeb08b1bebb21" />' +
    '<input type="text" name="checksum" value="'+ data.manilla.checksum +'" />' +
    //'<input type="text" name="service" value="mobile_money" />' +
    '<input type="submit" id="btnsub"/>' +
    '</form>');
    $('body').append(form);

    $("#btnsub").click();
}


function generateToken(){
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxX6xxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}


/**
*Handle enter key press event for password text field
*/
$('#btnTopupBank').click(function(e) {
    e.preventDefault();    
    var fullname = $('#txtTopupfullNameBk').val();
    var email = $('#txtTopupEmailBk').val();
    var token = $('#txtTopupTokenBk').val();
    var amount = $('#txtTopupAmountBk').val();
    var institution = $('#txtTopupInstitutionBk').val();
    var tpmode = $('#txtTopupModeBk').val();

    valide1 = validate_text_feild(fullname, "#txtTopupfullNameBk");
    valide2 = validate_text_feild(email, "#txtTopupEmailBk");
    valide3 = validate_text_feild(token, "#txtTopupTokenBk");
    valide4 = validate_text_feild(amount, "#txtTopupAmountBk", "number");
    valide5 = validate_text_feild(institution, "#txtTopupInstitutionBk");
    valide6 = validate_text_feild(tpmode, "#txtTopupModeBk");

    if( valide1 && valide2 && valide3 &&valide4 && valide5 && valide6 ){
      show_loader_modal();
      formData = {
          "fullname": fullname,
          "email": email,
          "token": token,
          "amount": amount,
          "institution": institution,
          "tpmode": tpmode,
      }
      console.log(formData);
      $.postJSON("/topup/bank/initiate", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          window.location = "/topup/requests/";
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
      });
  }
});


function approveTopupMod(token_id, institution){
  $("#txttypeText").text("approve");
  $("#txtxTpinstitution").text(institution);
  $("#txtToken_id").text(token_id);

  $("#btnApproveTopup").show();
  $("#btnDeclineTopup").hide();
  $("#btnConfirmTopup").hide();
  $("#btnCancelTopup").hide();

  $("#approveTopupModal").modal("show");
}

function confirmTopupMod(token_id, institution){
  $("#txttypeText").text("confirm");
  $("#txtxTpinstitution").text(institution);
  $("#txtToken_id").text(token_id);

  $("#btnApproveTopup").hide();
  $("#btnDeclineTopup").hide();
  $("#btnConfirmTopup").show();
  $("#btnCancelTopup").hide();

  $("#approveTopupModal").modal("show");
}

function declineTopupMod(token_id, institution){
  $("#txttypeText").text("decline");
  $("#txtxTpinstitution").text(institution);
  $("#txtToken_id").text(token_id);

  $("#btnApproveTopup").hide();
  $("#btnDeclineTopup").show();
  $("#btnConfirmTopup").hide();
  $("#btnCancelTopup").hide();

  $("#approveTopupModal").modal("show");
}

function cancelTopupMod(token_id, institution){
  $("#txttypeText").text("cancel");
  $("#txtxTpinstitution").text(institution);
  $("#txtToken_id").text(token_id);

  $("#btnApproveTopup").hide();
  $("#btnDeclineTopup").hide();
  $("#btnConfirmTopup").hide();
  $("#btnCancelTopup").show();

  $("#approveTopupModal").modal("show");
}


$("#btnApproveTopup").click(function(e) {
  e.preventDefault();
  var decision = $("#txttypeText").text();
  var institution = $("#txtxTpinstitution").text();
  var token_id = $("#txtToken_id").text();

  valide1 = validate_text_feild(decision, "#txttypeText");
  valide2 = validate_text_feild(institution, "#txtxTpinstitution");
  valide3 = validate_text_feild(token_id, "#txtToken_id");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "decision": decision,
          "institution": institution,
          "token_id": token_id,
      }
      console.log(formData);
      $.postJSON("/topup/response/approve", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          window.location = "/topup/requests/";
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
    });
  }
});


$("#btnDeclineTopup").click(function(e) {
  e.preventDefault();
  var decision = $("#txttypeText").text();
  var institution = $("#txtxTpinstitution").text();
  var token_id = $("#txtToken_id").text();

  valide1 = validate_text_feild(decision, "#txttypeText");
  valide2 = validate_text_feild(institution, "#txtxTpinstitution");
  valide3 = validate_text_feild(token_id, "#txtToken_id");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "decision": decision,
          "institution": institution,
          "token_id": token_id,
      }
      console.log(formData);
      $.postJSON("/topup/response/decline", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          window.location = "/topup/requests/";
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
    });
  }
});


$("#btnConfirmTopup").click(function(e) {
  e.preventDefault();
  var decision = $("#txttypeText").text();
  var institution = $("#txtxTpinstitution").text();
  var token_id = $("#txtToken_id").text();

  valide1 = validate_text_feild(decision, "#txttypeText");
  valide2 = validate_text_feild(institution, "#txtxTpinstitution");
  valide3 = validate_text_feild(token_id, "#txtToken_id");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "decision": decision,
          "institution": institution,
          "token_id": token_id,
      }
      console.log(formData);
      $.postJSON("/topup/response/confirm", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          window.location = "/topup/requests/";
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
    });
  }
});

$("#btnCancelTopup").click(function(e) {
  e.preventDefault();
  var decision = $("#txttypeText").text();
  var institution = $("#txtxTpinstitution").text();
  var token_id = $("#txtToken_id").text();

  valide1 = validate_text_feild(decision, "#txttypeText");
  valide2 = validate_text_feild(institution, "#txtxTpinstitution");
  valide3 = validate_text_feild(token_id, "#txtToken_id");

    if( valide1 && valide2 && valide3 ){
      show_loader_modal();
      formData = {
          "decision": decision,
          "institution": institution,
          "token_id": token_id,
      }
      console.log(formData);
      $.postJSON("/topup/response/cancel", formData, function(data){
        console.log(data);
        if (data.code == "00") {

          hide_loader_modal();
          displaySucessMsgModal(data.msg);
          window.location = "/topup/requests/";
        }

        else if(data.code == "01"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else if(data.code == "02"){
          hide_loader_modal();
          displayErrorMsgModal(data.msg); //display Error message
        }

        else{
          hide_loader_modal();
        }
    });
  }
});


$('#btnFilterDashboard').click(function(e) {
    e.preventDefault();   

  fromdate = $("#dfromdate").val();
  todate = $("#dtodate").val();

    // console.log(formData)
    show_loader();

    window.location = "/dashboard/filter?fromdate="+fromdate+'&todate='+todate;

});



$('#txtLanguage').on('change', function() {

  console.log("yeah");

  langua = $("#txtLanguage").val();
    var formData = {
        'language': langua,
    };

    console.log(formData)
    show_loader();

    $.postJSON("/admins/language", formData, function(data){
        console.log(data);
        if (data.code == "00") {
          hide_loader();
          window.location.reload();
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});



function topupNext(){

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)
    show_loader();

    $.postJSON("/topup/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_topup_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function topupPrev(){

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_topup_table(data.data, "minus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function filterTopup(){

  $("#page_id").val(1)

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_topup_table(data.data, "minus");
          $("#topupFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterTopup').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_topup_table(data.data, "minus");
          $("#topupFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnExportTopup').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    show_loader_modal();
    window.open("/topup/export?page="+(nextpage-1).toString()+'&fromdate='+fromdate+'&todate='+todate);

});


function load_topup_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    // if (detail.length == 0) {
    //   return;
    // }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      status = '';
      if (detail[i].status == "Active") {
        status = '<i class="fa fa-circle trans_success" aria-hidden="true"></i>';
      }
      else{
        status = '<i class="fa fa-circle trans_failed" aria-hidden="true"></i>';
      }

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].topupID +'</td>'+
                  '<td>'+ detail[i].username +'</td>'+
                  '<td>'+ detail[i].amount_topup +'</td>'+
                  '<td>'+ detail[i].amount_before_topup +'</td>'+
                  '<td>'+ detail[i].amount_after_topup +'</td>'+
                  '<td>'+ detail[i].description +'</td>'+
                  '<td>'+ detail[i].datetime_topup +'</td>'+
              '</tr>';
    }

    $('#topupTblBody').html("");
    $('#topupTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    }
    

}



function topupPendingNext(){

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val());

    if (nextpage == 1) {
      nextpage += 1 ;
    }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)
    show_loader();

    $.postJSON("/topup/requests/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_pending_topup_table(data.data, "plus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function topupPendingPrev(){

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/requests/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_pending_topup_table(data.data, "minus");
        }
        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


function filterPendingTopup(){

  $("#page_id").val(1)

  fromdate = $("#mfromdate").val();
  todate = $("#mtodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

    var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/requests/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_pending_topup_table(data.data, "minus");
          $("#topupPendingFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

}


$('#btnFilterPendingTopup').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    console.log(formData)

    // console.log(formData)
    show_loader();

    $.postJSON("/topup/requests/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          hide_loader();
          load_pending_topup_table(data.data, "minus");
          $("#topupPendingFilter").modal("hide");
        }

        else{
          hide_loader();
          displayErrorMsg(data.msg); //display Error message
        }
      });

});


$('#btnExportPendingTopup').click(function(e) {
    e.preventDefault();   

  $("#page_id").val(1)

  fromdate = $("#tpfromdate").val();
  todate = $("#tptodate").val();

  nextpage = parseInt($("#page_id").val())

  if (nextpage > 1) {
    nextpage -= 1;
  }else{
    nextpage = 1;
  }

  var formData = {
        'page': nextpage - 1,
        'fromdate': fromdate,
        'todate': todate,
    };

    show_loader_modal();
    window.open("/topup/requests/export?page="+(nextpage-1).toString()+'&fromdate='+fromdate+'&todate='+todate);

});


function load_pending_topup_table(detail, operator, page){
    // get_institutions();

    console.log(detail);

    // if (detail.length == 0) {
    //   return;
    // }

    tblBodyHtml = ""
    resp = ""
    for (var i = 0; i < detail.length; i++) {

      tblBodyHtml += '<tr style="background-color: #FEF9F3">'+
                  '<td style="color: #FF6A13; font-weight: bolder">'+ detail[i].token_id +'</td>'+
                  '<td>'+ detail[i].username +'</td>'+
                  '<td>'+ detail[i].topup_amount +'</td>'+
                  '<td>'+ detail[i].payment_mode +'</td>'+
                  '<td>'+ detail[i].institution +'</td>'+
                  '<td>'+ detail[i].approval_status +'</td>'+
                  '<td>'+ detail[i].approved_by +'</td>'+
                  '<td>'+ detail[i].topup_by +'</td>'+
                  '<td>'+ detail[i].request_date +'</td>'+
                  '<td>'+ detail[i].approved_by +'</td>'+
              '</tr>';
    }

    $('#topupTblBody').html("");
    $('#topupTblBody').html(tblBodyHtml);

    nextpage = parseInt($("#page_id").val());

    if (operator == "plus") {
      $("#page_id").val(nextpage+1);
    }else{
      if((nextpage -1 ) <= 0){
        $("#page_id").val(1);
      }else{
        $("#page_id").val((parseInt(nextpage)-1));
      }
    }
    

}


function getInstProfile() {
  var formData = {};

    console.log(formData)

    //show_loader();

    $.postJSON("/admins/inst_details/", formData, function(data){
        // console.log(data);
        if (data.code == "00") {
          //hide_loader();
          load_pending_topup_table(data.data, "minus");
          console.log(data.data['institution_data']['balance'])
          $("#inst_balance").html("GH&#x20b5; "+ data.data['institution_data']['balance']);
        }

        else{
          hide_loader();
          //1displayErrorMsg(data.msg); //display Error message
        }
      });
}



$('#btnGetLogs').click(function(e) {
  e.preventDefault();   

  log_typ = $("#txtLogType").val();
  log_date = $("#txtLogDate").val();

  valide1 = validate_text_feild(log_typ, "#txtLogType");
  valide2 = validate_text_feild(log_date, "#txtLogDate");
  if (valide1 && valide2) {
    show_loader();
    $.get( "/logs/"+ log_typ +"/"+ log_date, function( data ) {
      hide_loader();
      $( "#log_div" ).html( data );
    });
  }

});

$('#btnExportLogs').click(function(e) {
  e.preventDefault();   

  log_typ = $("#txtLogType").val();
  log_date = $("#txtLogDate").val();

  valide1 = validate_text_feild(log_typ, "#txtLogType");
  valide2 = validate_text_feild(log_date, "#txtLogDate");

  if (valide1 && valide2) {
    window.open("/logs/export/"+ log_typ +"/"+ log_date);
  }
});


function showToppuModal() {
  $("#topupmod").modal("show");
}

function showbank() {
  $('#btnTopupBank').show();
  $('#btnTopupManilla').hide();
  $("#txtTopupTokenBk").val(generateToken())
}


function showmil() {
  $('#btnTopupBank').hide();
  $('#btnTopupManilla').show();
}

function validate_text_feild(value, element, inputType){

  var regemail = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
  var regname = /^[a-zA-Z]+([\s\-]?[a-zA-Z])*$/;
  var regphone = /^233+\d{9}$/;
  var regph = /^0+\d{9}$/;
  var regnumeric = /^([0-9])+$/;
  var regalphanumeric = /^([0-9]|[a-zA-Z])+([0-9a-zA-Z]+)$/

  if (inputType == 'name'){
    res = regname.test(value);
  }
  else if (inputType == 'phone'){
    res = regphone.test(value) || regph.test(value);
  }
  else if (inputType == 'email'){
    res = regemail.test(value);
  }
  else if (inputType == 'alphanumeric'){
    res = regalphanumeric.test(value);
  }
  else if (inputType == 'number'){
    res = regnumeric.test(value);
  }
  else{
    res = true;
  }

  if((value == "" || value == undefined) || res == false){
    //if(!$(element).hasClass("has-error")){
        // $(element).removeClass("has-success");
        // $(element).toggleClass("has-error");
      //}
      if (inputType == 'empty'){
        return true;
      }

      $(element).removeAttr("border-bottom");
      $(element).removeAttr("box-shadow");
      $(element).css("border-bottom", "1px solid #FF0000");
      $(element).css("box-shadow", "0 1px 0 0 #FF0000");
      return false;
    }else{
      //if(!$(element).parent().hasClass("has-success")){
        // $(element).parent().removeClass("has-error");
        // $(element).parent().toggleClass("has-success");
      //}
      $(element).removeAttr("border-bottom");
      $(element).removeAttr("box-shadow");
      $(element).css("border-bottom", "1px solid #00E700");
      $(element).css("box-shadow", "0 1px 0 0 #00E700");
      return true;
    }
}

/**
* Post Handler
*/
$.postJSON = function(url, data, callback) {
  return jQuery.ajax({
      type: "POST",
      url: url,
      data: data,
      dataType: 'json',
      success: callback,
      error: onAjaxError,
      timeout: 50000,
      cache: false
  });
};


/**
*Show Loader Functions
*/
function show_loader(msg){
    if (msg == '' || msg == undefined){
      msg="Loading...";
    }
    $(".loader").html('<div align="center" style="margin:0 auto; margin-top:30px;" class="text-center">'+
                    '<div class="-spinner-ring -error-"></div>'+
                    '<h5>'+msg+'</h5>'+
                    '</div>')
    $(".loader").show("fast");
}
/**
*Hide Loader Functions
*/
function hide_loader(){
    $(".loader").html("")
    $(".loader").hide("fast");
}


/**
*Show Loader Functions
*/
function show_loader_modal(msg){
    if (msg == '' || msg == undefined){
      msg="";
    }
    $(".loader_modal").html('<div align="center" style="margin:0 auto; margin-top:30px;" class="text-center">'+
                    '<div class="-spinner-ring -error-"></div>'+
                    '<h5>'+msg+'</h5>'+
                    '</div>')
    $(".loader_modal").show("fast");
}
/**
*Hide Loader Functions
*/
function hide_loader_modal(){
    $(".loader_modal").html("")
    $(".loader_modal").hide("fast");
}


function onAjaxloginError(xhr, status, error){

    displayLoginErrorMsg(error);
}

function onAjaxError(xhr, status, error){
    hide_loader();
    displayErrorMsg(error);
    //msgAlertPlaceHoldermsgAlertPlaceHolder
}

function onAjaxNotification(xhr, status, error){

    displayErrorMsg(error);
}

function displaySucessMsg(msg){
  //hide loader
  //hide_loader();

  $(".msgAlertPlaceHolder").html("<div class='alert alert-success alert-dismissable fadeIn'><p class='text-left'>"+
        msg+"</p></div>");
  setTimeout(function() {
        $(".msgAlertPlaceHolder").html('');
    }, 5000);
}

function displayErrorMsg(msg){
  //hide loader
  //hide_loader();

    $(".msgAlertPlaceHolder").html("<div class='alert alert-danger alert-dismissable fade in'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".msgAlertPlaceHolder").html('');
    }, 5000);
}

function displayNotificationMsg(msg){
  //hide loader
  //hide_loader();

    $(".msgAlertPlaceHolder").html("<div class='alert alert-info alert-dismissable fade in'><p class='text-left'>"+ msg +"</p></div>");
    setTimeout(function() {
        $(".msgAlertPlaceHolder").html('');
    }, 5000);
}

function displayErrorMsgModal(msg){
    //hide loader
    //hide_loader();

    $(".modalAlertPlaceHolder").html("<div class='alert alert-danger alert-dismissable fade in'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".modalAlertPlaceHolder").html('');
    }, 5000);
}

function displaySucessMsgModal(msg){
    //hide loader
    //hide_loader();

    $(".modalAlertPlaceHolder").html("<div class='alert alert-success alert-dismissable fade in'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".modalAlertPlaceHolder").html('');
    }, 5000);
}

function displayNotificationMsgSession(msg){
    //hide loader
    //hide_loader();

    $(".msgAlertPlaceHolder").html("<div class='alert alert-success alert-dismissable fade in'><p class='text-left'>"+
        msg+"</p></div>");
}

function displayNotificationMsgModal(msg){
    //hide loader
    // hide_loader();

    $(".modalAlertPlaceHolder").html("<div class='alert alert-info alert-dismissable fade in'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".modalAlertPlaceHolder").html('');
    }, 5000);
}

function showSerialQuanty(){
  min = parseInt($("#mtxtminRange").val())
  max = parseInt($("#mtxtmaxRange").val())
  branch = $("#mtxtBranch").val()
  if(isNaN(min) || min <=0 || max <=0 || isNaN(max)){
    document.getElementById("qty").innerHTML = "Oops seems you've chosen an invalid range";
    return
  } 
  res = max - min 
  if(res <0){
    document.getElementById("qty").innerHTML = "Oops seems you've chosen an invalid range";
    return
  }
  document.getElementById("qty").innerHTML = "You are about to assign " + (res + 1) + " serials to " + branch;
}
//Initialize flatpickr date picker
  $("#mfromdate").flatpickr();
  $("#mtodate").flatpickr();
  $("#txtLogDate").flatpickr();

function updateChartView(which_chart){
  formData = {};
  chart_dv = "";
  if(which_chart == "verification"){
    filter_type = $("#mVerificationFilterBy").val()
    formData["user_type"] = "gen_public";
    formData["filter_type"] = filter_type;
    chart_dv = "verification_chartdiv";
  } else if(which_chart == "validation"){
    filter_type = $("#mValidationFilterBy").val()
    formData["user_type"] = "validator";
    formData["filter_type"] = filter_type;
    chart_dv = "validation_chartdiv";

  } else{
    return
  }
console.log(formData);

show_loader();

$.postJSON("/home/report", formData, function(data){

  if (data != null) {
    hide_loader();
    var chart_data = [];
    var day_hour = (formData.filter_type =="daily") ? "hour" : "day" ;
    var hint_text = (which_chart == "verification") ? "verification request(s)" : "validation request(s)" ;
    var convert_hour = ["12AM", "1AM", "2AM", "3AM", "4AM", "5AM", "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM", "11PM"];

    for(var i=0; i < data.length; i++){
      if(formData.filter_type == "daily"){
        var obj = { 
          week_days: convert_hour[data[i].days],
          count: parseInt(data[i].total)
         };
         chart_data.push(obj);

      } else{
        var obj = { 
          week_days: data[i].days,
          count: parseInt(data[i].total)
      };
      chart_data.push(obj);

      }


    }
    console.log(chart_data);
    var chart = AmCharts.makeChart(chart_dv, {
      type: "serial",
      backgroundAlpha: 1,
      depth3D: 1,
      dataProvider: chart_data,    
      categoryField: "week_days",
      startDuration: 1,
      startEffect: "easeOutSine",
      valueAxes: [{
          axisAlpha: 0.15,
          minimum: 0,
          dashLength: 3,
          axisTitleOffset: 20,
          gridCount: 5,
          title: which_chart + " count"
      }],
      graphs: [{
          valueField: "count",
          bullet: "circle",
          balloonText: "[[value]] " + hint_text + " per this " + day_hour
      }],
"export": {
"enabled": true,
"libs": {
"autoLoad": false
 }
}
});
   
  }

  else{
    hide_loader();
  }
});


}

