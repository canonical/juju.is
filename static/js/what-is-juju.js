
let lastKnownScrollPosition = 0;
let ticking = false;
let stage = 0;
const animation = document.querySelector('.p-feature');
const title = document.querySelector('.p-feature__title');

function setStage(scrollPos) {
  const cache = stage;
  const vh = window.innerHeight;
  const stripPosition = animation.getBoundingClientRect();
  var bodyRect = document.body.getBoundingClientRect(),
    elemRect = animation.getBoundingClientRect(),
    offset   = elemRect.top - bodyRect.top;
  if (scrollPos >= offset) {
    scrollPos = scrollPos - offset;
    stage = Math.floor(scrollPos / vh);
    half = Math.round(scrollPos / vh);
    if (stage !== cache) {
      if (stage < cache) {
        animation.setAttribute("data-direction", "up");
      } else {
        animation.setAttribute("data-direction", "down");
      }
    }
    if (stage !== half) {
      animation.setAttribute("data-half", "true");
    } else {
      animation.setAttribute("data-half", "false");
    }
    animation.setAttribute("data-stage", stage);
  } else {
    animation.setAttribute("data-half", "false");
    animation.setAttribute("data-stage", "0");
  }
}

document.addEventListener('scroll', function(e) {
  lastKnownScrollPosition = window.scrollY;

  if (!ticking) {
    window.requestAnimationFrame(function() {
      setStage(lastKnownScrollPosition);
      ticking = false;
    });

    ticking = true;
  }
});