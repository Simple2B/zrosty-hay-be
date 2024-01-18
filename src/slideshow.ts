document.addEventListener('DOMContentLoaded', function () {
  let slideIndex = 0;

  const container = document.getElementById('slideshow-container');
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList') {
        showSlides(slideIndex);
      }
    });
  });

  observer.observe(container, {childList: true});

  showSlides(slideIndex);
  function plusSlides(n: number) {
    showSlides((slideIndex += n));
  }
  const prevButton = document.getElementById('prev-btn-slideshow');
  prevButton.addEventListener('click', function () {
    plusSlides(-1);
  });

  // Thumbnail image controls
  const nextButton = document.getElementById('next-btn-slideshow');
  nextButton.addEventListener('click', function () {
    plusSlides(1);
  });

  function showSlides(n: number) {
    const slides: NodeListOf<HTMLDivElement> =
      document.querySelectorAll('.my-slides');
    console.log('slides');
    const slidesLength = slides.length - 1;
    if (n > slidesLength) {
      slideIndex = 0;
    }
    if (n < 0) {
      slideIndex = slidesLength;
    }
    slides.forEach((slide, i) => {
      if (slideIndex === i) {
        slide.classList.remove('hidden');
      } else {
        if (!slide.classList.contains('hidden')) {
          slide.classList.add('hidden');
        }
      }
    });
  }
});
