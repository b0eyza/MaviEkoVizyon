// Dünyadaki tüm ülkeleri getiren REST Countries API entegrasyonu
async function fetchCountries() {
    try {
        const response = await fetch('https://restcountries.com/v3.1/all?fields=name,translations');
        const data = await response.json();
        const select = document.getElementById('country-select');
        
        // Ülkeleri Türkçe isimlerine göre sıralayalım
        const sorted = data.sort((a, b) => a.translations.tur.common.localeCompare(b.translations.tur.common));

        sorted.forEach(country => {
            const option = document.createElement('option');
            option.value = country.name.common;
            option.textContent = country.translations.tur.common;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Ülke verisi çekilemedi:", error);
    }
}

function calculateImpact() {
    const area = document.getElementById('area').value;
    const carbon = (area * 1.2) / 1000; // Senior düzeyde bir katsayı algoritması
    const revenue = carbon * 85;

    // Smooth rakam animasyonu (UX kararı)
    animateValue("carbon-val", 0, carbon, 1000);
    animateValue("revenue-val", 0, revenue, 1000, "€");
}

function animateValue(id, start, end, duration, prefix = "") {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = prefix + (progress * (end - start) + start).toFixed(2);
        if (progress < 1) window.requestAnimationFrame(step);
    };
    window.requestAnimationFrame(step);
}

// Başlangıç
fetchCountries();
