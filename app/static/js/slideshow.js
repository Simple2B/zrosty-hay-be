/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**************************!*\
  !*** ./src/slideshow.ts ***!
  \**************************/
document.addEventListener('DOMContentLoaded', function () {
    var slideIndex = 0;
    var container = document.getElementById('slideshow-container');
    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'childList') {
                showSlides(slideIndex);
            }
        });
    });
    observer.observe(container, { childList: true });
    showSlides(slideIndex);
    function plusSlides(n) {
        showSlides((slideIndex += n));
    }
    var prevButton = document.getElementById('prev-btn-slideshow');
    prevButton.addEventListener('click', function () {
        plusSlides(-1);
    });
    // Thumbnail image controls
    var nextButton = document.getElementById('next-btn-slideshow');
    nextButton.addEventListener('click', function () {
        plusSlides(1);
    });
    function showSlides(n) {
        var slides = document.querySelectorAll('.my-slides');
        console.log('slides');
        var slidesLength = slides.length - 1;
        if (n > slidesLength) {
            slideIndex = 0;
        }
        if (n < 0) {
            slideIndex = slidesLength;
        }
        slides.forEach(function (slide, i) {
            if (slideIndex === i) {
                slide.classList.remove('hidden');
            }
            else {
                if (!slide.classList.contains('hidden')) {
                    slide.classList.add('hidden');
                }
            }
        });
    }
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvc2xpZGVzaG93LmpzIiwibWFwcGluZ3MiOiI7Ozs7O0FBQUEsUUFBUSxDQUFDLGdCQUFnQixDQUFDLGtCQUFrQixFQUFFO0lBQzVDLElBQUksVUFBVSxHQUFHLENBQUMsQ0FBQztJQUVuQixJQUFNLFNBQVMsR0FBRyxRQUFRLENBQUMsY0FBYyxDQUFDLHFCQUFxQixDQUFDLENBQUM7SUFDakUsSUFBTSxRQUFRLEdBQUcsSUFBSSxnQkFBZ0IsQ0FBQyxtQkFBUztRQUM3QyxTQUFTLENBQUMsT0FBTyxDQUFDLGtCQUFRO1lBQ3hCLElBQUksUUFBUSxDQUFDLElBQUksS0FBSyxXQUFXLEVBQUUsQ0FBQztnQkFDbEMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxDQUFDO1lBQ3pCLENBQUM7UUFDSCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLE9BQU8sQ0FBQyxTQUFTLEVBQUUsRUFBQyxTQUFTLEVBQUUsSUFBSSxFQUFDLENBQUMsQ0FBQztJQUUvQyxVQUFVLENBQUMsVUFBVSxDQUFDLENBQUM7SUFDdkIsU0FBUyxVQUFVLENBQUMsQ0FBUztRQUMzQixVQUFVLENBQUMsQ0FBQyxVQUFVLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQztJQUNoQyxDQUFDO0lBQ0QsSUFBTSxVQUFVLEdBQUcsUUFBUSxDQUFDLGNBQWMsQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO0lBQ2pFLFVBQVUsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDbkMsVUFBVSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7SUFDakIsQ0FBQyxDQUFDLENBQUM7SUFFSCwyQkFBMkI7SUFDM0IsSUFBTSxVQUFVLEdBQUcsUUFBUSxDQUFDLGNBQWMsQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO0lBQ2pFLFVBQVUsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDbkMsVUFBVSxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ2hCLENBQUMsQ0FBQyxDQUFDO0lBRUgsU0FBUyxVQUFVLENBQUMsQ0FBUztRQUMzQixJQUFNLE1BQU0sR0FDVixRQUFRLENBQUMsZ0JBQWdCLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDMUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUN0QixJQUFNLFlBQVksR0FBRyxNQUFNLENBQUMsTUFBTSxHQUFHLENBQUMsQ0FBQztRQUN2QyxJQUFJLENBQUMsR0FBRyxZQUFZLEVBQUUsQ0FBQztZQUNyQixVQUFVLEdBQUcsQ0FBQyxDQUFDO1FBQ2pCLENBQUM7UUFDRCxJQUFJLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQztZQUNWLFVBQVUsR0FBRyxZQUFZLENBQUM7UUFDNUIsQ0FBQztRQUNELE1BQU0sQ0FBQyxPQUFPLENBQUMsVUFBQyxLQUFLLEVBQUUsQ0FBQztZQUN0QixJQUFJLFVBQVUsS0FBSyxDQUFDLEVBQUUsQ0FBQztnQkFDckIsS0FBSyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7WUFDbkMsQ0FBQztpQkFBTSxDQUFDO2dCQUNOLElBQUksQ0FBQyxLQUFLLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxRQUFRLENBQUMsRUFBRSxDQUFDO29CQUN4QyxLQUFLLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztnQkFDaEMsQ0FBQztZQUNILENBQUM7UUFDSCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7QUFDSCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3pyb3N0eS1oYXkvLi9zcmMvc2xpZGVzaG93LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGxldCBzbGlkZUluZGV4ID0gMDtcblxuICBjb25zdCBjb250YWluZXIgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2xpZGVzaG93LWNvbnRhaW5lcicpO1xuICBjb25zdCBvYnNlcnZlciA9IG5ldyBNdXRhdGlvbk9ic2VydmVyKG11dGF0aW9ucyA9PiB7XG4gICAgbXV0YXRpb25zLmZvckVhY2gobXV0YXRpb24gPT4ge1xuICAgICAgaWYgKG11dGF0aW9uLnR5cGUgPT09ICdjaGlsZExpc3QnKSB7XG4gICAgICAgIHNob3dTbGlkZXMoc2xpZGVJbmRleCk7XG4gICAgICB9XG4gICAgfSk7XG4gIH0pO1xuXG4gIG9ic2VydmVyLm9ic2VydmUoY29udGFpbmVyLCB7Y2hpbGRMaXN0OiB0cnVlfSk7XG5cbiAgc2hvd1NsaWRlcyhzbGlkZUluZGV4KTtcbiAgZnVuY3Rpb24gcGx1c1NsaWRlcyhuOiBudW1iZXIpIHtcbiAgICBzaG93U2xpZGVzKChzbGlkZUluZGV4ICs9IG4pKTtcbiAgfVxuICBjb25zdCBwcmV2QnV0dG9uID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3ByZXYtYnRuLXNsaWRlc2hvdycpO1xuICBwcmV2QnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKCkge1xuICAgIHBsdXNTbGlkZXMoLTEpO1xuICB9KTtcblxuICAvLyBUaHVtYm5haWwgaW1hZ2UgY29udHJvbHNcbiAgY29uc3QgbmV4dEJ1dHRvbiA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCduZXh0LWJ0bi1zbGlkZXNob3cnKTtcbiAgbmV4dEJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcbiAgICBwbHVzU2xpZGVzKDEpO1xuICB9KTtcblxuICBmdW5jdGlvbiBzaG93U2xpZGVzKG46IG51bWJlcikge1xuICAgIGNvbnN0IHNsaWRlczogTm9kZUxpc3RPZjxIVE1MRGl2RWxlbWVudD4gPVxuICAgICAgZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLm15LXNsaWRlcycpO1xuICAgIGNvbnNvbGUubG9nKCdzbGlkZXMnKTtcbiAgICBjb25zdCBzbGlkZXNMZW5ndGggPSBzbGlkZXMubGVuZ3RoIC0gMTtcbiAgICBpZiAobiA+IHNsaWRlc0xlbmd0aCkge1xuICAgICAgc2xpZGVJbmRleCA9IDA7XG4gICAgfVxuICAgIGlmIChuIDwgMCkge1xuICAgICAgc2xpZGVJbmRleCA9IHNsaWRlc0xlbmd0aDtcbiAgICB9XG4gICAgc2xpZGVzLmZvckVhY2goKHNsaWRlLCBpKSA9PiB7XG4gICAgICBpZiAoc2xpZGVJbmRleCA9PT0gaSkge1xuICAgICAgICBzbGlkZS5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGlmICghc2xpZGUuY2xhc3NMaXN0LmNvbnRhaW5zKCdoaWRkZW4nKSkge1xuICAgICAgICAgIHNsaWRlLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9