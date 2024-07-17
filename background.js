chrome.runtime.onInstalled.addEventListener(() => {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: {hostEquals: 'meet.google.com'},
                })
            ],
            actions: [new chrome.declarativeContent.ShowAction()]
        }]);
    });
});
