// popup.js - Flash card popup logic for Configurator and Start Here pages

// On page load, restore carried card popup if present
window.addEventListener('DOMContentLoaded', function() {
    const carried = localStorage.getItem('carriedFlashCard');
    if (carried) {
        try {
            const card = JSON.parse(carried);
            openFlashCardPopup(card);
        } catch(e) {}
    }
});

function openFlashCardPopup(card) {
    let popup = document.getElementById('flashCardPopup');
    if (popup) popup.remove();
    popup = document.createElement('div');
    popup.id = 'flashCardPopup';
    popup.style.position = 'fixed';
    popup.style.top = '80px';
    popup.style.right = '40px';
    popup.style.zIndex = '9999';
    popup.style.width = '350px';
    popup.style.background = '#fff';
    popup.style.border = '2px solid #007bff';
    popup.style.borderRadius = '8px';
    popup.style.boxShadow = '0 4px 16px rgba(0,0,0,0.15)';
    let html = '<div class="card shadow"><div class="card-body">';
    if (card.objective) html += `<h3 class="card-title">${card.objective}</h3>`;
    if (card.description) html += `<p class="card-text">${card.description}</p>`;
    if (card.keywords && card.keywords.length) html += `<div><strong>Recommended keywords:</strong> <code>${card.keywords.join(', ')}</code></div>`;
    if (card.instructions && card.instructions.length) {
        html += '<div class="mt-2"><strong>Instructions:</strong><ol>';
        for (let step of card.instructions) html += `<li>${step}</li>`;
        html += '</ol></div>';
    }
    if (card.related_settings && card.related_settings.length) html += `<div class="mt-2"><strong>Related settings:</strong> <code>${card.related_settings.join(', ')}</code></div>`;
    if (card.docs_link) html += `<div class="mt-2"><a href="${card.docs_link}" target="_blank" class="btn btn-link">Marlin Documentation</a></div>`;
    if (card.warnings) html += `<div class="mt-2 text-danger"><strong>Warning:</strong> ${card.warnings}</div>`;
    html += '<div class="mt-3"><button class="btn btn-sm btn-secondary" onclick="closeFlashCardPopup()">Close</button></div>';
    html += '</div></div>';
    popup.innerHTML = html;
    document.body.appendChild(popup);
    makeDraggable(popup);
}
function closeFlashCardPopup() {
    let popup = document.getElementById('flashCardPopup');
    if (popup) popup.remove();
    localStorage.removeItem('carriedFlashCard');
}
function makeDraggable(el) {
    let isMouseDown = false, offset = [0,0];
    el.addEventListener('mousedown', function(e) {
        isMouseDown = true;
        offset = [el.offsetLeft - e.clientX, el.offsetTop - e.clientY];
        el.style.cursor = 'move';
    });
    document.addEventListener('mouseup', function() {
        isMouseDown = false;
        el.style.cursor = 'default';
    });
    document.addEventListener('mousemove', function(e) {
        if (!isMouseDown) return;
        el.style.left = (e.clientX + offset[0]) + 'px';
        el.style.top = (e.clientY + offset[1]) + 'px';
    });
}
