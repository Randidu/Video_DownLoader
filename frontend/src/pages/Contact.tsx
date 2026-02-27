import React, { useState } from 'react';
import { useSEO } from '../hooks/useSEO';

const Contact: React.FC = () => {
    useSEO({
        title: "Contact Us - InfinityGrab",
        description: "Have questions or need help with InfinityGrab video downloader? Contact our support team for any inquiries or bug reports.",
        canonical: "https://infinitygrab.xyz/contact"
    });

    const [form, setForm] = useState({ name: '', email: '', message: '' });
    const [submitted, setSubmitted] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // In production, send to backend or use Formspree/EmailJS
        setSubmitted(true);
    };

    return (
        <section className="policy-section" id="contact">
            <div className="container">
                <div className="policy-card" style={{ maxWidth: 700, margin: '0 auto' }}>
                    <h1 className="policy-title">Contact Us</h1>
                    <p className="policy-date">We'd love to hear from you!</p>

                    <div className="policy-body">
                        <div className="contact-info-row">
                            <div className="contact-info-item">
                                <span>📧</span>
                                <div>
                                    <strong>Email</strong>
                                    <p><a href="mailto:hello@infinitygrab.xyz">hello@infinitygrab.xyz</a></p>
                                </div>
                            </div>
                            <div className="contact-info-item">
                                <span>🐛</span>
                                <div>
                                    <strong>Bug Reports</strong>
                                    <p><a href="mailto:support@infinitygrab.xyz">support@infinitygrab.xyz</a></p>
                                </div>
                            </div>
                            <div className="contact-info-item">
                                <span>⚖️</span>
                                <div>
                                    <strong>Legal / DMCA</strong>
                                    <p><a href="mailto:legal@infinitygrab.xyz">legal@infinitygrab.xyz</a></p>
                                </div>
                            </div>
                        </div>

                        {submitted ? (
                            <div className="contact-success">
                                ✅ Thank you! We'll get back to you within 24 hours.
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="contact-form">
                                <div className="mb-3">
                                    <label htmlFor="name" className="form-label">Your Name</label>
                                    <input
                                        type="text" id="name" name="name"
                                        className="form-control url-input"
                                        placeholder="John Doe"
                                        value={form.name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">Email Address</label>
                                    <input
                                        type="email" id="email" name="email"
                                        className="form-control url-input"
                                        placeholder="john@example.com"
                                        value={form.email}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="message" className="form-label">Message</label>
                                    <textarea
                                        id="message" name="message"
                                        className="form-control url-input"
                                        rows={5}
                                        placeholder="Your message..."
                                        value={form.message}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary btn-fetch w-100">
                                    <i className="bi bi-send me-2"></i>Send Message
                                </button>
                            </form>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Contact;
