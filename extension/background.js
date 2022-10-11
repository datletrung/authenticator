chrome.webNavigation.onCompleted.addListener(function() {
    chrome.tabs.query({'active': true, 'lastFocusedWindow': true, 'currentWindow': true}, function (tabs) {
        var url = tabs[0].url;
        console.log(url);
        data = {
            "url": "http://google.com"
        }
        var response_code = fetch("http://localhost:7491/?url="+url)
                                .then(response => response.text())
                                .then(text => console.log(text))
                                .catch(error => console.log(error));
    });
}, {});
