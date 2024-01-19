document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.querySelector('#submit-program-form-btn');
  const stepsDiv = document.querySelector('#program-steps');
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList') {
        //   showSlides(slideIndex);
        console.log('changed');
      }
    });
  });
  observer.observe(stepsDiv, {childList: true});

  // submitBtn.addEventListener('click', e => {
  //   e.preventDefault();
  //   console.log('click');
  // });
});
