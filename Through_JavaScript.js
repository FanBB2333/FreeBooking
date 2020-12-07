var url;
let this_href = window.location.href;
// url = "/api.php/activities/1620/application?mobile=xxxxxxxxxx"; // 骚操作
// url = "/api.php/activities/1620/application2?mobile=xxxxxxxxxx"; // 正常操作
let activityid = this_href.substr(40,4);
// let mobile = prompt("Plz input ur phone number","");
// activityid = prompt("Plz input activityid","");
url = "/api.php/activities/";
url += activityid;
url += "/application2?mobile=";
url += mobile;
let maxn = 100;
maxn = prompt("Plz input max number of attempts","");
for (let i = 0; i < maxn; i++) {  
    setTimeout(appoint(i),500*i);  
}
function appoint(a){
    return function(){
        console.log(a);
        if (!ska.username) {
            login();
        }
        jQuery.ajax({
            url:url,
            type:'GET',
            dateType:'json',
            data:{'id':activityid},
            complete: function(xhr, textStatus) {
                //called when complete
                },
            success: function(data, textStatus, xhr) {
            //var rooms = data.data.list;
            if(data.status){
                // alertDialog(data.msg,'success');
                console.log(data.msg);
                setTimeout(function () { window.location.reload(); }, 100);
            }else{
                // alertDialog(data.msg,'error');
                console.log("Failed");
                //window.location.reload();
            }
            
            },
            error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
            // alertDialog('网络错误，请重试','error');
            console.log("Error");
            //window.location.reload();
            }
        });
    }
}