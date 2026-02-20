import React from 'react';

const Navbar: React.FC = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark sticky-top">
            <div className="container">
                <a className="navbar-brand" href="#">InfinityGrab</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav mx-auto">
                        <li className="nav-item"><a className="nav-link" href="#home">Home</a></li>
                        <li className="nav-item"><a className="nav-link" href="#features">Features</a></li>
                        <li className="nav-item"><a className="nav-link" href="#">API</a></li>
                        <li className="nav-item"><a className="nav-link" href="#">Contact</a></li>
                    </ul>
                    <button className="btn btn-primary btn-download-header">
                        <i className="bi bi-download me-2"></i>Download Now
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
