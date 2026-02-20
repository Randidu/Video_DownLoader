import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
    const location = useLocation();
    const isActive = (path: string) => location.pathname === path ? 'nav-link active' : 'nav-link';

    return (
        <nav className="navbar navbar-expand-lg navbar-dark sticky-top">
            <div className="container">
                <Link className="navbar-brand d-flex align-items-center" to="/">
                    <img src="/logo.png" alt="InfinityGrab Logo" width="40" height="40" className="d-inline-block align-text-top me-2 rounded-circle" />
                    InfinityGrab
                </Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav mx-auto">
                        <li className="nav-item"><Link className={isActive('/')} to="/">Home</Link></li>
                        <li className="nav-item"><Link className={isActive('/about')} to="/about">About</Link></li>
                        <li className="nav-item"><a className="nav-link" href="/#features">Features</a></li>
                        <li className="nav-item"><a className="nav-link" href="/#faq">FAQ</a></li>
                        <li className="nav-item"><Link className={isActive('/contact')} to="/contact">Contact</Link></li>
                    </ul>
                    <Link to="/" className="btn btn-primary btn-download-header">
                        <i className="bi bi-download me-2"></i>Download Now
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
