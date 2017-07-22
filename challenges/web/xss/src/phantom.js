var page = require('webpage').create();
var host = "127.0.0.1";
var url = "http://"+host+"/?f=FILE_NAME_TO_REPLACE";
var timeout = 2000;
 
phantom.addCookie({
    'name': 'Flag',
    'value': 'FLAG{PeJNJxB5eWoHXmLD0XmZsApNFK3rgDARAih6nMRgwRSepUHb7n}',
    'domain': host,
    'path': '/',
    'httponly': false
});
 
page.onNavigationRequested = function(url, type, willNavigate, main) {
    console.log("[URL] URL="+url);  
};
 
page.settings.resourceTimeout = timeout;
page.onResourceTimeout = function(e) {
    setTimeout(function(){
        console.log("[INFO] Timeout")
        phantom.exit();
    }, 1);
};
 
page.open(url, function(status) {
    console.log("[INFO] rendered page");
    setTimeout(function(){
        phantom.exit();
    }, 1);
});
