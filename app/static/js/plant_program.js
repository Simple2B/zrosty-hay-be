/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!******************************!*\
  !*** ./src/plant_program.ts ***!
  \******************************/
document.addEventListener('DOMContentLoaded', function () {
    var submitBtn = document.querySelector('#submit-program-form-btn');
    var stepsDiv = document.querySelector('#program-steps');
    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'childList') {
                //   showSlides(slideIndex);
                console.log('changed');
            }
        });
    });
    observer.observe(stepsDiv, { childList: true });
    // submitBtn.addEventListener('click', e => {
    //   e.preventDefault();
    //   console.log('click');
    // });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvcGxhbnRfcHJvZ3JhbS5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLFNBQVMsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLDBCQUEwQixDQUFDLENBQUM7SUFDckUsSUFBTSxRQUFRLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxnQkFBZ0IsQ0FBQyxDQUFDO0lBQzFELElBQU0sUUFBUSxHQUFHLElBQUksZ0JBQWdCLENBQUMsbUJBQVM7UUFDN0MsU0FBUyxDQUFDLE9BQU8sQ0FBQyxrQkFBUTtZQUN4QixJQUFJLFFBQVEsQ0FBQyxJQUFJLEtBQUssV0FBVyxFQUFFLENBQUM7Z0JBQ2xDLDRCQUE0QjtnQkFDNUIsT0FBTyxDQUFDLEdBQUcsQ0FBQyxTQUFTLENBQUMsQ0FBQztZQUN6QixDQUFDO1FBQ0gsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDLENBQUMsQ0FBQztJQUNILFFBQVEsQ0FBQyxPQUFPLENBQUMsUUFBUSxFQUFFLEVBQUMsU0FBUyxFQUFFLElBQUksRUFBQyxDQUFDLENBQUM7SUFFOUMsNkNBQTZDO0lBQzdDLHdCQUF3QjtJQUN4QiwwQkFBMEI7SUFDMUIsTUFBTTtBQUNSLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8venJvc3R5LWhheS8uL3NyYy9wbGFudF9wcm9ncmFtLnRzIl0sInNvdXJjZXNDb250ZW50IjpbImRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IHN1Ym1pdEJ0biA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNzdWJtaXQtcHJvZ3JhbS1mb3JtLWJ0bicpO1xuICBjb25zdCBzdGVwc0RpdiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNwcm9ncmFtLXN0ZXBzJyk7XG4gIGNvbnN0IG9ic2VydmVyID0gbmV3IE11dGF0aW9uT2JzZXJ2ZXIobXV0YXRpb25zID0+IHtcbiAgICBtdXRhdGlvbnMuZm9yRWFjaChtdXRhdGlvbiA9PiB7XG4gICAgICBpZiAobXV0YXRpb24udHlwZSA9PT0gJ2NoaWxkTGlzdCcpIHtcbiAgICAgICAgLy8gICBzaG93U2xpZGVzKHNsaWRlSW5kZXgpO1xuICAgICAgICBjb25zb2xlLmxvZygnY2hhbmdlZCcpO1xuICAgICAgfVxuICAgIH0pO1xuICB9KTtcbiAgb2JzZXJ2ZXIub2JzZXJ2ZShzdGVwc0Rpdiwge2NoaWxkTGlzdDogdHJ1ZX0pO1xuXG4gIC8vIHN1Ym1pdEJ0bi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGUgPT4ge1xuICAvLyAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgLy8gICBjb25zb2xlLmxvZygnY2xpY2snKTtcbiAgLy8gfSk7XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==