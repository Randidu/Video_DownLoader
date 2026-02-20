import React, { useState } from 'react';

interface HeroProps {
    onFetch: (url: string) => void;
    isLoading: boolean;
    error: string | null;
}

const Hero: React.FC<HeroProps> = ({ onFetch, isLoading, error }) => {
    const [url, setUrl] = useState('');

    const handleFetch = () => {
        if (url.trim()) {
            onFetch(url.trim());
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleFetch();
        }
    };

    return (
        <section className="hero" id="home">
            <div className="container">
                <h1>Best Free Video Downloader: YouTube, Facebook, TikTok</h1>
                <p>Download Videos from YouTube, Facebook, Instagram, TikTok & more in HD/4K</p>

                {/* URL Input */}
                <div className="url-input-container">
                    <input
                        type="text"
                        className="form-control url-input"
                        id="videoUrl"
                        placeholder="Paste your video URL here (YouTube, Facebook, Instagram, TikTok, Vimeo...)"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        onKeyPress={handleKeyPress}
                        disabled={isLoading}
                    />
                    <button
                        className="btn btn-primary btn-fetch"
                        onClick={handleFetch}
                        disabled={isLoading || !url.trim()}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                Fetching...
                            </>
                        ) : (
                            <>
                                <i className="bi bi-search me-2"></i>Fetch Video
                            </>
                        )}
                    </button>
                </div>

                {/* Alert */}
                {error && (
                    <div className="alert alert-danger alert-custom active" role="alert">
                        <i className="bi bi-exclamation-triangle-fill me-2"></i>
                        <span>{error}</span>
                    </div>
                )}

                {/* Platform Icons */}
                <div className="platforms">
                    <div className="platform-icon" style={{ color: '#FF0000' }} title="YouTube">
                        <i className="bi bi-youtube"></i>
                    </div>
                    <div className="platform-icon" style={{ color: '#1877F2' }} title="Facebook">
                        <i className="bi bi-facebook"></i>
                    </div>
                    <div className="platform-icon" style={{ color: '#E4405F' }} title="Instagram">
                        <i className="bi bi-instagram"></i>
                    </div>
                    <div className="platform-icon" style={{ color: '#000000' }} title="TikTok">
                        <i className="bi bi-tiktok"></i>
                    </div>
                    <div className="platform-icon" style={{ color: '#1DA1F2' }} title="X (Twitter)">
                        <i className="bi bi-twitter-x"></i>
                    </div>
                    <div className="platform-icon" style={{ color: '#1AB7EA' }} title="Vimeo">
                        <i className="bi bi-vimeo"></i>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
