import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-links">
                    <a href="#">About</a>
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">FAQ</a>
                    <a href="#">Contact</a>
                </div>
                <p className="copyright">
                    &copy; {new Date().getFullYear()} InfinityGrab. All rights reserved. Made with Randidu Damsith <i className="bi bi-heart-fill text-danger"></i>
                </p>
            </div>
        </footer>
    );
};

export default Footer;
