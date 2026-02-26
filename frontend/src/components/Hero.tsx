import React, { useState } from 'react';

interface HeroProps {
    onFetch: (url: string) => void;
    isLoading: boolean;
    error: string | null;
}

const Hero: React.FC<HeroProps> = ({ onFetch, isLoading, error }) => {
    const [url, setUrl] = useState('');
    const [showLive, setShowLive] = useState(false);

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

                {/* Live Match Section */}
                {/* <div className="live-match-container mb-5 text-center">
                    {!showLive ? (
                        <button
                            onClick={() => setShowLive(true)}
                            className="btn"
                            style={{
                                backgroundColor: '#ff0000',
                                color: 'white',
                                fontWeight: 'bold',
                                borderRadius: '50px',
                                padding: '12px 30px',
                                fontSize: '1.2rem',
                                boxShadow: '0 0 20px rgba(255, 0, 0, 0.6)',
                                border: '2px solid white',
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '10px',
                                textTransform: 'uppercase',
                                letterSpacing: '1px'
                            }}
                        >
                            <span className="spinner-grow spinner-grow-sm text-light" role="status" aria-hidden="true" style={{ width: '1rem', height: '1rem' }}></span>
                            Watch Live: Star Sports
                        </button>
                    ) : (
                        <div className="live-player-wrapper mb-4" style={{ position: 'relative', width: '100%', maxWidth: '800px', margin: '0 auto', borderRadius: '15px', overflow: 'hidden', boxShadow: '0 10px 40px rgba(0,0,0,0.6)', border: '2px solid #333' }}>
                            <div style={{ padding: '12px 20px', backgroundColor: '#111', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #333' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <span className="spinner-grow spinner-grow-sm text-danger" role="status" aria-hidden="true" style={{ width: '0.8rem', height: '0.8rem' }}></span>
                                    <span style={{ color: 'white', fontWeight: 'bold', fontSize: '1.1rem' }}>Star Sports - Live</span>
                                </div>
                                <button onClick={() => setShowLive(false)} className="btn btn-sm btn-outline-light" style={{ borderRadius: '50px', padding: '5px 15px' }}>
                                    <i className="bi bi-x-lg me-1"></i> Close Player
                                </button>
                            </div>
                            <div style={{ width: '100%', paddingTop: '56.25%', position: 'relative', backgroundColor: 'black' }}>
                                <iframe
                                    src="https://tvlivehub.vercel.app/watch?url=https%3A%2F%2Ftest-streams.mux.dev%2Fx36xhzz%2Fx36xhzz.m3u8&title=Star%20Sports&hls=true"
                                    style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
                                    allowFullScreen
                                    title="Live Match"
                                ></iframe>
                            </div>
                        </div>
                    )}
                </div> */}

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
                    {/* Adult Sites */}
                    <div className="platform-icon" style={{ color: '#FF9900' }} title="Pornhub">
                        <span style={{ fontSize: '1.2rem', fontWeight: 900, fontFamily: 'Arial, sans-serif', letterSpacing: '-1px' }}>PH</span>
                    </div>
                    <div className="platform-icon" style={{ color: '#E52B50' }} title="XVideos">
                        <span style={{ fontSize: '1.2rem', fontWeight: 900, fontFamily: 'Arial, sans-serif', letterSpacing: '-1px' }}>XV</span>
                    </div>
                    <div className="platform-icon" style={{ color: '#E52B50' }} title="xHamster">
                        <span style={{ fontSize: '1.1rem', fontWeight: 900, fontFamily: 'Arial, sans-serif' }}>xH</span>
                    </div>
                    <div className="platform-icon" style={{ color: '#0055A4' }} title="XNXX">
                        <span style={{ fontSize: '0.9rem', fontWeight: 900, fontFamily: 'Arial, sans-serif' }}>XNXX</span>
                    </div>
                    <div className="platform-icon" style={{ color: '#00AFF0' }} title="OnlyFans">
                        <span style={{ fontSize: '1.2rem', fontWeight: 900, fontFamily: 'Arial, sans-serif', letterSpacing: '-1px' }}>OF</span>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
