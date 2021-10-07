function handleRadioButtons() {
  var vendorRadioButtonsContainer = document.querySelector(".js-vendor-radios");
  var coffeeRadioButtonsContainer = document.querySelector(".js-coffee-radios");

  var vendorRadioButtons = Array.prototype.slice.call(
    vendorRadioButtonsContainer.querySelectorAll(".js-radio")
  );

  var coffeeRadioButtons = Array.prototype.slice.call(
    coffeeRadioButtonsContainer.querySelectorAll(".js-radio")
  );

  vendorRadioButtons.forEach(function (radioButton) {
    selectRadioButton(radioButton, vendorRadioButtonsContainer);
  });

  coffeeRadioButtons.forEach(function (radioButton) {
    selectRadioButton(radioButton, coffeeRadioButtonsContainer);
  });
}

function selectRadioButton(radioButton, radioButtonsContainer) {
  radioButton.addEventListener("click", function (event) {
    var previousOption = radioButtonsContainer.querySelector(".is-selected");

    if (previousOption) {
      previousOption.classList.remove("is-selected");
    }

    radioButton.closest(".p-radio-card").classList.add("is-selected");
  });
}

function setSavingState(isSaving) {
  var brewFormButton = document.querySelector(".js-brew-form-button");
  var brewFormLoadingIcon = brewFormButton.querySelector(".p-icon--spinner");

  brewFormButton.disabled = isSaving;

  if (isSaving) {
    brewFormLoadingIcon.classList.remove("u-hide");
  } else {
    brewFormLoadingIcon.classList.add("u-hide");
  }
}

function buildFormUrl(
  cloudVendor,
  coffee,
  firstName,
  lastName,
  email,
  company,
  title
) {
  return (
    "https://docs.google.com/forms/d/e/1FAIpQLSf1eFVXFfSJQABS2Aopao73NNOwLokVMSaV3pm0N9INt8U-tg/formResponse?usp=pp_url&entry.226591523=" +
    cloudVendor +
    "&entry.1935891743=" +
    coffee +
    "&entry.1739229526=" +
    firstName +
    "&entry.1136522365=" +
    lastName +
    "&entry.959962128=" +
    email +
    "&entry.1922056816=" +
    company +
    "&entry.1777593423=" +
    title +
    "&submit=Submit"
  );
}

function executeForm(form) {
  var formResponseFrame = document.getElementById("form-response");
  var cloudVendor = form.querySelector("[name=cloud-vendor]:checked").value;
  var coffee = form.querySelector("[name=coffee]:checked").value;
  var firstName = form.querySelector("[name=firstName]").value;
  var lastName = form.querySelector("[name=lastName]").value;
  var email = form.querySelector("[name=email]").value;
  var company = form.querySelector("[name=company]").value;
  var title = form.querySelector("[name=title]").value;
  var formId = form.querySelector("[name=formid]").value;
  var canonicalUpdatesOptIn = form.querySelector(
    "#canonicalUpdatesOptIn"
  ).checked;

  formResponseFrame.src = encodeURI(
    buildFormUrl(
      cloudVendor,
      coffee,
      firstName,
      lastName,
      email,
      company,
      title
    )
  );

  handleMarketoForm(
    firstName,
    lastName,
    email,
    company,
    title,
    canonicalUpdatesOptIn,
    formId
  );
}

function handleMarketoForm(
  firstName,
  lastName,
  email,
  company,
  title,
  canonicalUpdatesOptIn,
  formId
) {
  var data = new FormData();
  var liveFeedSection = document.getElementById("live-from-london");

  data.set("canonicalUpdatesOptIn", canonicalUpdatesOptIn);
  data.set("formid", formId);
  data.set("firstName", firstName);
  data.set("lastName", lastName);
  data.set("email", email);
  data.set("company", company);
  data.set("title", title);

  fetch("https://ubuntu.com/marketo/submit", {
    method: "POST",
    body: data,
    mode: "no-cors",
  }).then(function (response) {
    setTimeout(function () {
      liveFeedSection.scrollIntoView({ behavior: "smooth" });
      setSavingState(false);
    }, 500);
  });
}

function brewInit() {
  var brewForm = document.querySelector(".js-brew-form");

  handleRadioButtons();

  brewForm.addEventListener("submit", function (event) {
    event.preventDefault();
    setSavingState(true);
    executeForm(brewForm);
  });
}

brewInit();
