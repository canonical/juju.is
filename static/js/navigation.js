function toggleDropdown(toggle, open) {
  const parentElement = toggle.parentNode;
  const dropdown = document.getElementById(
    toggle.getAttribute("aria-controls")
  );
  dropdown.setAttribute("aria-hidden", !open);

  if (open) {
    parentElement.classList.add("is-active", "is-selected");
  } else {
    parentElement.classList.remove("is-active", "is-selected");
  }
}

function closeAllDropdowns(toggles) {
  toggles.forEach((toggle) => {
    toggleDropdown(toggle, false);
  });
}

function handleClickOutside(toggles, containerClass) {
  document.addEventListener("click", (event) => {
    const target = event.target;

    if (target.closest) {
      if (!target.closest(containerClass)) {
        closeAllDropdowns(toggles);
      }
    }
  });
}

function initNavDropdowns(containerClass) {
  const toggles = [].slice.call(
    document.querySelectorAll(containerClass + " [aria-controls]")
  );

  handleClickOutside(toggles, containerClass);

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", (e) => {
      e.preventDefault();

      const isOpen = e.target.parentNode.classList.contains("is-active");

      closeAllDropdowns(toggles);
      toggleDropdown(toggle, !isOpen);
    });
  });
}

function initNavigationSearch(element) {
  const searchButtons = element.querySelectorAll(".js-search-button");

  searchButtons.forEach((searchButton) => {
    searchButton.addEventListener("click", toggleSearch);
  });

  const overlay = element.querySelector(".p-navigation__search-overlay");
  if (overlay) {
    overlay.addEventListener("click", closeSearch);
  }

  function toggleSearch(e) {
    e.preventDefault();

    const navigation = e.target.closest(".p-navigation");
    if (navigation.classList.contains("has-search-open")) {
      closeSearch();
    } else {
      openSearch(e);
    }
  }

  function openSearch(e) {
    e.preventDefault();
    const navigation = e.target.closest(".p-navigation");
    const searchInput = navigation.querySelector(".p-search-box__input");
    const buttons = document.querySelectorAll(".js-search-button");

    buttons.forEach((searchButton) => {
      searchButton.setAttribute("aria-pressed", true);
    });

    navigation.classList.add("has-search-open");
    searchInput.focus();
    document.addEventListener("keyup", keyPressHandler);
  }

  function closeSearch() {
    const navigation = document.querySelector(".p-navigation");
    const buttons = document.querySelectorAll(".js-search-button");

    buttons.forEach((searchButton) => {
      searchButton.removeAttribute("aria-pressed");
    });

    navigation.classList.remove("has-search-open");
    document.removeEventListener("keyup", keyPressHandler);
  }

  function keyPressHandler(e) {
    if (e.key === "Escape") {
      closeSearch();
    }
  }
}

const navigation = document.querySelector("#navigation");
initNavigationSearch(navigation);
