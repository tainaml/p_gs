"use strict";

import Slideout from "slideout";
import input from "./components/customform/input.js";
import "./asyncModules";
import "./vendor/bootstrap/";
import "./modules/ideiaForm/";
import "./modules/ideiaAsyncSocialAction/";
import "./modules/ideiaAutocomplete/";
import "./modules/ideiaLoadAsync/";
import "./modules/ideiaFilter/";
import "./modules/ideiaLogin/";
import "./modules/ideiaNotification/";
import "./modules/ideiaRestrict/";
import "./modules/ideiaValidationField/";
import "./modules/ideiaEditor/";
import "./components";
import commitBox from "./components/commit-box";

$(function() {
  window.csrfSafeMethod = function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };

  window.getCookie = function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");

      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  };

  require("./modules");
  require("perfect-scrollbar/jquery")($);
  require("imports?$=jquery!jscroll");

  $('[data-toggle="custom-scroll"] > .float-notifcations').perfectScrollbar();

  // Modals
  $("[data-target=modal]").modal({ show: false });
  $("[data-toggle=modal]").on("click", function(event) {
    $(this)
      .parents("[data-target=modal]")
      .modal("hide");
  });

  // Tooltips
  $('[data-toggle="tooltip"]').tooltip();

  // Slideout
  var slideout = new Slideout({
    panel: document.getElementById("wrapper"),
    menu: document.getElementById("slideout-menu"),
    padding: 256,
    tolerance: 70,
    touch: false
  });
  $(document).on("click", ".toggle-slideout", function() {
    slideout.toggle();
  });
  $(document).on("click", ".slideout-menu--user-image", function() {
    slideout.toggle();
  });

  const toggleSearch = $("[data-toggle='search']");
  toggleSearch.on("click", event => {
    event.preventDefault();
    const currentTarget = $(event.currentTarget);
    if (window.innerWidth < 768) {
      currentTarget.animate(
        { width: window.innerWidth },
        {
          complete: () => {
            currentTarget.find("input").focus();
            currentTarget.find(".js-searchbar-icon").one("click", event => {
              event.stopPropagation();
              currentTarget.css({ width: 42 });
              toggleIconClass(
                ".js-searchbar-icon i",
                "gsticon-close",
                "gsticon-search"
              );
            });
            toggleIconClass(
              ".js-searchbar-icon i",
              "gsticon-search",
              "gsticon-close"
            );
          }
        }
      );
    }
  });

  const toggleIconClass = (target, oldClass, newClass) => {
    $(target)
      .removeClass(oldClass)
      .addClass(newClass);
  };

  input($('[data-toggle="input"]'));
  commitBox('[data-toggle="commit-box"]');

  // TODO: Move for a async load
  const showDeleStatus = event => {
    const deleteUrl = $(event.relatedTarget).data("deleteUrl");
    $('[data-target="to-delete"]').attr("href", deleteUrl);
    console.log($('[data-target="to-delete"]')[0]);
  };

  $("#modal-delete-status").on("show.bs.modal", showDeleStatus);
});

global.changeurls = (seletor, qsKey, qsValue) => {
  $.each(seletor, (index, element) => {
    let href = element.href.split("?")[0];

    element.href = `${href}?${qsKey}=${qsValue}`;
  });
};
