const quotes = [
    "It is not that we have a short time to live, but that we waste a lot of it. - Seneca",
    "Knowing yourself is the beginning of all wisdom. - Aristotle",
    "Happiness is the meaning and the purpose of life, the whole aim and end of human existence. - Aristotle",
    "Luck is what happens when preparation meets opportunity. - Seneca",
    "You have power over your mind, not outside events. Realize this, and you will find strength. - Marcus Aurelius"
];

document.getElementById('generate-button').addEventListener('click', async function () {
    const quotes = [
        "It is not that we have a short time to live, but that we waste a lot of it. - Seneca",
        "Knowing yourself is the beginning of all wisdom. - Aristotle",
        "Happiness is the meaning and the purpose of life, the whole aim and end of human existence. - Aristotle",
        "Luck is what happens when preparation meets opportunity. - Seneca",
        "You have power over your mind, not outside events. Realize this, and you will find strength. - Marcus Aurelius"
    ];

    const randomIndex = Math.floor(Math.random() * quotes.length);
    const selectedQuote = quotes[randomIndex];

    const quoteDisplay = document.getElementById('quote-display');
    quoteDisplay.innerText = selectedQuote;

    // const apiKey = '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';  // Replace this with your actual OpenAI API key

    const prompt = `Based on this quote: "${selectedQuote}", provide a relevant learning technique.`;

    try {
        const response = await fetch('https://api.openai.com/v1/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: "gpt-4",
                prompt: prompt,
                max_tokens: 150
            })
        });

        const data = await response.json();

        if (data.choices && data.choices.length > 0) {
            const technique = data.choices[0].text.trim();
            displayLearningTechniques(technique);
        } else {
            console.error('No choices returned by GPT');
            document.getElementById('learning-techniques').innerText = 'Failed to fetch learning technique.';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('learning-techniques').innerText = 'Failed to fetch learning technique.';
    }
});

function displayLearningTechniques(technique) {
    const cardContainer = document.getElementById('learning-techniques');
    cardContainer.innerHTML = '';  

    const card = document.createElement('div');
    card.classList.add('card');

    const cardTitle = document.createElement('h3');
    cardTitle.innerText = "Learning Technique";

    const cardContent = document.createElement('p');
    cardContent.innerText = technique;

    card.appendChild(cardTitle);
    card.appendChild(cardContent);
    cardContainer.appendChild(card);
}
