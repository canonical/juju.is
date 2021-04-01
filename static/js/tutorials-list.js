(function () {
  const selector = "tutorials-topic";
  const topicsFilter = document.getElementById(selector);
  if (topicsFilter) {
    topicsFilter.addEventListener("change", (e) => {
      window.location.search = `?topic=${e.target.value}`;
    });
  } else {
    throw new Error(`${selector} is not a valid element!`);
  }
})();
