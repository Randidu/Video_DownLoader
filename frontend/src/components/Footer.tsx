import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-brand">
                    <img src="/logo.png" alt="InfinityGrab" width="36" height="36" className="rounded-circle me-2" />
                    <span>InfinityGrab</span>
                </div>
                <p className="footer-tagline">The fastest free video downloader for YouTube, Facebook, TikTok & more.</p>
                <div className="footer-links">
                    <Link to="/">Home</Link>
                    <Link to="/about">About</Link>
                    <Link to="/privacy">Privacy Policy</Link>
                    <Link to="/terms">Terms of Service</Link>
                    <Link to="/contact">Contact</Link>
                </div>
                <div className="footer-disclaimer">
                    <p>⚠️ InfinityGrab is intended for personal, non-commercial use only. Users are responsible for complying with applicable copyright laws. We do not host or store any video content.</p>
                </div>
                <p className="copyright">
                    &copy; {new Date().getFullYear()} InfinityGrab. All rights reserved. Made with ❤️ by Randidu Damsith
                </p>
            </div>
        </footer>
    );
};

export default Footer;
