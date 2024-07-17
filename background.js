chrome.tabs.onUpdated.addEventListener((tabId, tab) => {
  if (tab.url && tab.url.includes("meet.google.com")) {
    const queryParameters = tab.url.split("/")[1];
    const urlParameters = new URLSearchParams(queryParameters);
  }
});