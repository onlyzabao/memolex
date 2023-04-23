/**
* Template Name: Logis - v1.3.0
* Template URL: https://bootstrapmade.com/logis-bootstrap-logistics-website-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Sticky header on scroll
   */
  const selectHeader = document.querySelector('#header');
  if (selectHeader) {
    document.addEventListener('scroll', () => {
      window.scrollY > 100 ? selectHeader.classList.add('sticked') : selectHeader.classList.remove('sticked');
    });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    const togglescrollTop = function() {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
    window.addEventListener('load', togglescrollTop);
    document.addEventListener('scroll', togglescrollTop);
    scrollTop.addEventListener('click', window.scrollTo({
      top: 0,
      behavior: 'smooth'
    }));
  }

  /**
   * Mobile nav toggle
   */
  const mobileNavShow = document.querySelector('.mobile-nav-show');
  const mobileNavHide = document.querySelector('.mobile-nav-hide');

  document.querySelectorAll('.mobile-nav-toggle').forEach(el => {
    el.addEventListener('click', function(event) {
      event.preventDefault();
      mobileNavToogle();
    })
  });

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavShow.classList.toggle('d-none');
    mobileNavHide.classList.toggle('d-none');
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navbar a').forEach(navbarlink => {

    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll('.navbar .dropdown > a');

  navDropdowns.forEach(el => {
    el.addEventListener('click', function(event) {
      if (document.querySelector('.mobile-nav-active')) {
        event.preventDefault();
        this.classList.toggle('active');
        this.nextElementSibling.classList.toggle('dropdown-active');

        let dropDownIndicator = this.querySelector('.dropdown-indicator');
        dropDownIndicator.classList.toggle('bi-chevron-up');
        dropDownIndicator.classList.toggle('bi-chevron-down');
      }
    })
  });

  /**
   * Initiate pURE cOUNTER
   */
  new PureCounter();

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper('.slides-1', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

  /**
   * popup
   */
// Lấy các phần tử DOM cần thiết
const addButton = document.getElementById("add-to-playlist");
const popup = document.getElementById("playlist-popup");
const closePopupButton = document.querySelector(".close-popup");
const playlistCheckboxes = document.querySelectorAll('input[name="playlist"]');
const createPlaylistButton = document.getElementById("create-playlist");
const newPlaylistNameInput = document.getElementById("new-playlist-name");

// Khi bấm vào nút "Thêm vào danh sách phát"
addButton.addEventListener("click", function() {
  // Hiện popup
  popup.style.display = "block";
});

// Khi bấm vào nút đóng popup
closePopupButton.addEventListener("click", function() {
  // Ẩn popup
  popup.style.display = "none";
});

// Khi bấm vào nút tạo danh sách mới
createPlaylistButton.addEventListener("click", function() {
  // Lấy tên mới
  const newPlaylistName = newPlaylistNameInput.value;
  if (newPlaylistName === "") {
    alert("Please enter a list name");
    return;
  }
  

  // Tạo một thẻ label mới
  const label = document.createElement("label");

  // Tạo một checkbox mới
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.name = "playlist";
  checkbox.value = newPlaylistName;

  // Thêm checkbox vào label
  label.appendChild(checkbox);

  // Thêm tên danh sách vào label
  label.appendChild(document.createTextNode(newPlaylistName));

  // Thêm label vào popup
  popup.insertBefore(label, createPlaylistButton.parentNode);

  // Reset giá trị input tên mới
  newPlaylistNameInput.value = "";
});

// Lắng nghe sự kiện change cho các checkbox danh sách phát
playlistCheckboxes.forEach(function(checkbox) {
  checkbox.addEventListener("change", function() {
    if (!this.checked) {
      // Nếu checkbox không được chọn, hiển thị thông báo "Đã gỡ khỏi danh sách phát"
      let message = document.createElement("div");
      message.classList.add("popup-message", "fade-in");
      message.innerText = "Delete from list";
      document.body.appendChild(message);
      setTimeout(function() {
        // Sau 2 giây, xóa thông báo
        message.remove();
      }, 800);
    } else {
      let message = document.createElement("div");
      message.classList.add("popup-message", "fade-in");
      message.innerText = "Add to list";
      document.body.appendChild(message);
      setTimeout(function() {
        message.classList.add("fade-out");
        setTimeout(function() {
          message.remove(); // Xóa message khỏi DOM khi animation kết thúc
        }, 600); // Thời gian animation của fade-out là 0.6 giây
      }, 800);
    }
  });
});
});

  //Create new list
const createNewListButton = document.getElementById("create-new-list");
const popup = document.getElementById("popup");
const closePopupButton = document.querySelector(".close-popup");
const createListButton = document.getElementById("create-list");

createNewListButton.addEventListener("click", function() {
  popup.style.display = "block";
});

closePopupButton.addEventListener("click", function() {
  popup.style.display = "none";
});

createListButton.addEventListener("click", function() {
  const newListName = document.getElementById("new-list-name").value;
  
  if (newListName === "") {
    alert("Please enter a list name");
    return;
  }
  
  popup.style.display = "none";
  setTimeout(function() {
    alert("Done");
  });
  
  // Add the new list to your list of lists here
});
