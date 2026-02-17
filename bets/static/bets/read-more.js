document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('read-more')) {
        const parentSpan = e.target.closest('.comment-content');
        const fullText = parentSpan.getAttribute('data-full-text');
        
        // Replace the paragraph content with the full text
        parentSpan.innerHTML = fullText + ' <a href="javascript:void(0);" class="read-less">Show Less</a>';
    }

    if (e.target && e.target.classList.contains('read-less')) {
        const parentSpan = e.target.closest('.comment-content');
        const fullText = parentSpan.getAttribute('data-full-text');
        const truncated = fullText.substring(0, 150) + '...';
        
        parentSpan.innerHTML = truncated + ' <a href="javascript:void(0);" class="read-more">Read More</a>';
    }
});