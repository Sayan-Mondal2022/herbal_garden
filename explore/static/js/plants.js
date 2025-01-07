document.addEventListener("DOMContentLoaded", function() {
    const imageContainers = document.querySelectorAll('.image-container');

    imageContainers.forEach(container => {
        const images = container.querySelectorAll('img');
        let currentIndex = 0;

        function showNextImage() {
            images[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % images.length;
            images[currentIndex].classList.add('active');
        }

        images[currentIndex].classList.add('active'); 
        setInterval(showNextImage, 10000); 
    });
});


// document.addEventListener("DOMContentLoaded", function() {
//     const features = document.querySelectorAll('.feature');
//     let currentFeatureIndex = 0;

//     function changeFeatureText() {
//         features.forEach((feature, index) => {
//             feature.style.opacity = 0;  // Hide all features
//             feature.style.transform = 'translateY(20px)';
//         });

//         // Show the current feature
//         features[currentFeatureIndex].style.opacity = 1;
//         features[currentFeatureIndex].style.transform = 'translateY(0)';

//         // Move to the next feature after 25 seconds
//         currentFeatureIndex = (currentFeatureIndex + 1) % features.length;
//     }

//     changeFeatureText();

//     setInterval(changeFeatureText, 5000); 
// });
