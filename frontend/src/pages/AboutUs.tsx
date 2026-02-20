import React from 'react';

const AboutUs: React.FC = () => (
    <section className="policy-section" id="about">
        <div className="container">
            <div className="policy-card">
                <h1 className="policy-title">About InfinityGrab</h1>
                <p className="policy-date">Your Trusted Free Video Downloader</p>

                <div className="policy-body">
                    <div className="about-hero-text">
                        <p>InfinityGrab is a free, powerful, and easy-to-use online video downloader that lets you save videos from YouTube, Facebook, Instagram, TikTok, Twitter/X, Vimeo, and hundreds of other platforms — directly to your device.</p>
                    </div>

                    <h2>Our Mission</h2>
                    <p>We believe everyone should have the ability to save and enjoy their favorite online videos offline — whether for travel, studying, or simply accessing content without an internet connection. InfinityGrab was built to make this process simple, fast, and completely free.</p>

                    <h2>What Makes InfinityGrab Different?</h2>

                    <div className="about-features-grid">
                        <div className="about-feature">
                            <span className="about-icon">⚡</span>
                            <h3>Lightning Fast</h3>
                            <p>Our optimized backend processes video downloads in seconds. No waiting, no delays.</p>
                        </div>
                        <div className="about-feature">
                            <span className="about-icon">🆓</span>
                            <h3>Completely Free</h3>
                            <p>No registration required. No subscription. No hidden fees. Download unlimited videos for free.</p>
                        </div>
                        <div className="about-feature">
                            <span className="about-icon">🎬</span>
                            <h3>Multiple Formats</h3>
                            <p>Choose from MP4 video (360p to 4K) or MP3 audio. We support the formats you need.</p>
                        </div>
                        <div className="about-feature">
                            <span className="about-icon">🌐</span>
                            <h3>500+ Platforms</h3>
                            <p>From YouTube to niche video sites — if it's online, InfinityGrab can likely download it.</p>
                        </div>
                        <div className="about-feature">
                            <span className="about-icon">🔒</span>
                            <h3>Safe & Private</h3>
                            <p>We don't store your videos or personal data. Downloads are private and secure.</p>
                        </div>
                        <div className="about-feature">
                            <span className="about-icon">📱</span>
                            <h3>Works Everywhere</h3>
                            <p>Use InfinityGrab on your phone, tablet or desktop. No app installation required.</p>
                        </div>
                    </div>

                    <h2>Technology</h2>
                    <p>InfinityGrab is powered by cutting-edge technology including Python FastAPI backend, React frontend, and the industry-leading yt-dlp library for maximum compatibility with video platforms worldwide.</p>

                    <h2>Responsible Use</h2>
                    <p>We built InfinityGrab for legal, personal use. Please respect copyright laws and only download content you have permission to download. See our <a href="/terms">Terms of Service</a> for more details.</p>

                    <h2>Contact Us</h2>
                    <p>Have a question or feedback? We'd love to hear from you!</p>
                    <p>📧 <a href="mailto:hello@infinitygrab.xyz">hello@infinitygrab.xyz</a></p>
                </div>
            </div>
        </div>
    </section>
);

export default AboutUs;
