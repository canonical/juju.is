/**
  Updates the URL with the id of the target tab content
  while preventing the page from jumping around by
  manipulating the history object. Inspired by:
  // https://gist.github.com/pimterry/260841c2104f27cadc954a29b9873b96#file-disable-link-jump-with-workaround-js
  @param {HTMLElement} tab the triggered tab
  @param {Array} tabs an array of sibling tabs
*/
function handleTabInteraction(tab, tabs) {
  history.pushState({}, "", tab.href);
  history.pushState({}, "", tab.href);
  history.back();

  setActiveTab(tabs);
}

/**
  Attaches a number of events that each trigger
  the reveal of the chosen tab content
  @param {Array} tabs an array of tabs within a container
*/
function attachEvents(tabs) {
  tabs.forEach(function (tab) {
    tab.addEventListener("keyup", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        handleTabInteraction(tab, tabs);
      }
    });

    tab.addEventListener("click", function (e) {
      e.preventDefault();
      handleTabInteraction(tab, tabs);
    });
  });

  window.addEventListener(
    "hashchange",
    function () {
      setActiveTab(tabs);
    },
    false
  );
}

/**
  Checks the current URL hash and 
  sets the selected tab accordingly
  @param {Array} tabs an array of tabs within a container
*/
function setActiveTab(tabs) {
  var URLhash = window.location.hash;
  var tabHashes = tabs.map(function (tab) {
    return tab.getAttribute("href");
  });

  if (URLhash && tabHashes.includes(URLhash)) {
    var tabLink = document.querySelector("[href='" + URLhash + "']");
    tabs.forEach(function (tab) {
      if (tab === tabLink) {
        tab.setAttribute("aria-selected", true);
      } else {
        tab.setAttribute("aria-selected", false);
      }
    });
  }
}

/**
  Attaches events to tab links within a given parent element,
  and sets the active tab if the current hash matches the id
  of an element controlled by a tab link
  @param {String} selector class name of the element 
  containing the tabs we want to attach events to
*/
function initTabs(selector) {
  var tabContainers = [].slice.call(document.querySelectorAll(selector));

  tabContainers.forEach(function (tabContainer) {
    var tabs = [].slice.call(tabContainer.querySelectorAll("[aria-controls]"));
    attachEvents(tabs);
    setActiveTab(tabs);
  });
}
