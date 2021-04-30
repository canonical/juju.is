var wrapper = document.querySelector('.js-comunity-top-posts');
var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
fetch("/discourse-top.json")
  .then(function(response) {
    return response.json();
  })
  .then(function(json) {
    var listMarkup = '';
    for (var i = 0; i < 4; i++ ) {
      var topic = json.topic_list.topics[i];
      var date = new Date(topic.last_posted_at);
      var prettyDate = date.getDate() + ' ' + months[date.getMonth()+1]+ ' ' + date.getFullYear();
      var topicData = {
        "likes": topic.like_count,
        "link": `https://discourse.charmhub.io/t/${topic.id}`,
        "title": topic.fancy_title,
        "poster": topic.last_poster_username,
        "date": prettyDate
      }
      listMarkup += createListItem(topicData);
    }
    wrapper.innerHTML = listMarkup;
  })
  .catch(function (error) {
    console.log("Request failed", error);
  });

  function createListItem(topic) {
    return `<li class="p-list__item">
      <h5 class="u-no-margin--bottom">
        <a href="${topic.link}">
          ${topic.title}
        </a>
      </h5>
      <div class="p-label--validated">${topic.likes} likes</div>
      <p class="u-text--muted u-no-margin--bottom">Last commented on by ${ topic.poster } <br />on ${ topic.date }</p>
    </li>`
  }