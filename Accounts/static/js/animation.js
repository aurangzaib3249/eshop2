(function($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        loadingCss: "",
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<style>@keyframes poofity {0% {transform: scale(1, 1) rotate(90deg);opacity: 0.1;}50% {transform: scale(4, 4) rotate(-360deg);opacity: 0;}}@keyframes poof {0% {transform: scale(1, 1) rotate(0deg);opacity: 0.2;}50% {transform: scale(4, 4) rotate(360deg);opacity: 0;}} .another {opacity: 0.1;transform: rotate(90deg);animation: poofity 5s infinite;animation-delay: 1s;}@keyframes loadEr {0% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 10.4% {border-top-color: rgba(44, 44, 44, 0.5);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);}    20.8% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);  border-left-color: rgba(33, 33, 33, 0);}  31.2% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0.5);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 41.6% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);transform: rotate(40deg);} 52% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0.5);border-left-color: rgba(33, 33, 33, 0);} 62.4% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 72.8% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0.5);}} .text {position: absolute;top: 95px;left: 8px;font-family: Arial;text-transform: uppercase;color: #888;animation: opaa 10s infinite;} @keyframes opaa {0% {opacity: 1;}10% {opacity: 0.5}15% {opacity: 1;}30% {opacity: 1;}65% {opacity: 0.3;}90% {opacity: 0.8;}}</style><div class="wrap" style="position: absolute;top: 40%;width: 100%;margin-left:40%"><div class="loader" style="position: absolute;top: 0;z-index: 10;width: 50px;height: 50px;border: 15px solid;border-radius: 50%;border-top-color: rgb(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);animation: loadEr 3s infinite;"></div><div class="loaderbefore" style="width: 50px;height: 50px;border: 15px solid #ddd;border-radius: 50%;position: absolute;top: 0;z-index: 9;"></div><div class="circular" style="position: absolute;top: -15px;left: -15px;width: 70px;height: 70px;border: 20px solid;border-radius: 50%;border-top-color: #333;border-left-color: #fff;border-bottom-color: #333;border-right-color: #fff;opacity: 0.2;animation: poof 5s infinite;"></div><div class="circular another" style="opacity: 0.1;transform: rotate(90deg);animation: poofity 5s infinite;animation-delay: 1s;"></div><div class="text">Loading</div></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: ['animation-duration', '-webkit-animation-duration'],
        overlay: false,
        overlayClass: 'animsition-overlay-slide',
        overlayParentElement: 'html',
        transition: function(url) { window.location.href = url; }
    });

   

})(jQuery);