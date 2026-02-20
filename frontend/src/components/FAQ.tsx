import React, { useState } from 'react';

interface FAQItem {
    question: string;
    answer: string;
}

const faqs: FAQItem[] = [
    {
        question: "How to download YouTube videos for free?",
        answer: "Simply paste the YouTube video URL into the search box above, click 'Fetch Video', choose your quality (MP4, MP3, 1080p, 4K), and click 'Download'. Done!"
    },
    {
        question: "What video formats does InfinityGrab support?",
        answer: "InfinityGrab supports MP4 video downloads up to 4K/2160p, 1080p, 720p, 480p, 360p, and MP3 audio extraction from any video."
    },
    {
        question: "Which platforms can I download videos from?",
        answer: "InfinityGrab supports YouTube, Facebook, Instagram, TikTok, Twitter/X, Vimeo, and hundreds of other platforms worldwide."
    },
    {
        question: "Is InfinityGrab free to use?",
        answer: "Yes! InfinityGrab is completely free. No registration, no subscription, no hidden fees. Just paste any video URL and download instantly."
    },
    {
        question: "Is it safe to use InfinityGrab?",
        answer: "Yes, InfinityGrab is 100% safe. We do not store your video files on our servers and do not require any personal information."
    },
    {
        question: "Can I download videos on mobile?",
        answer: "Absolutely! InfinityGrab works perfectly on all mobile browsers (iOS, Android) as well as desktop browsers on Windows and Mac."
    },
];

const FAQ: React.FC = () => {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <section className="faq-section" id="faq" aria-label="Frequently Asked Questions">
            <div className="container">
                <h2 className="section-title">Frequently Asked Questions</h2>
                <p className="section-subtitle">Everything you need to know about downloading videos with InfinityGrab</p>

                <div className="faq-list">
                    {faqs.map((faq, i) => (
                        <div
                            className={`faq-item${openIndex === i ? ' open' : ''}`}
                            key={i}
                            onClick={() => setOpenIndex(openIndex === i ? null : i)}
                            aria-expanded={openIndex === i}
                        >
                            <div className="faq-question">
                                <span>{faq.question}</span>
                                <i className={`bi ${openIndex === i ? 'bi-dash-lg' : 'bi-plus-lg'}`}></i>
                            </div>
                            {openIndex === i && (
                                <div className="faq-answer">
                                    <p>{faq.answer}</p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default FAQ;
