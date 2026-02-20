import React from 'react';

const Features: React.FC = () => {
    return (
        <section className="features" id="features">
            <div className="container">
                <h2 className="section-title">Powerful Features</h2>
                <p className="section-subtitle">Everything you need to download videos from any platform</p>

                <div className="row g-4">
                    <div className="col-lg-3 col-md-6">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <i className="bi bi-lightning-charge-fill"></i>
                            </div>
                            <h4>Fast Downloads</h4>
                            <p>Lightning-fast download speeds with our optimized servers. Get your videos in seconds.</p>
                        </div>
                    </div>

                    <div className="col-lg-3 col-md-6">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <i className="bi bi-grid-3x3-gap-fill"></i>
                            </div>
                            <h4>Multi-Platform</h4>
                            <p>Support for YouTube, Facebook, Instagram, TikTok, Twitter, Vimeo and many more platforms.</p>
                        </div>
                    </div>

                    <div className="col-lg-3 col-md-6">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <i className="bi bi-music-note-beamed"></i>
                            </div>
                            <h4>Audio Extraction</h4>
                            <p>Extract audio from any video and download as MP3 with high quality preservation.</p>
                        </div>
                    </div>

                    <div className="col-lg-3 col-md-6">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <i className="bi bi-badge-hd-fill"></i>
                            </div>
                            <h4>HD Quality</h4>
                            <p>Download videos in up to 4K resolution. Choose from multiple quality options.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Features;
