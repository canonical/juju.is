(function () {
  const selector = "tutorials-topic";
  const topicsFilter = document.getElementById(selector);
  if (topicsFilter) {
    topicsFilter.addEventListener("change", (e) => {
      window.location.search = `?topic=${e.target.value}`;
    });

    const params = new URLSearchParams(window.location.search);
    const topicFromUrl = params.get("topic");

    if (topicFromUrl) {
      topicsFilter.value = topicFromUrl;
    }
  } else {
    throw new Error(`${selector} is not a valid element!`);
  }
})();
