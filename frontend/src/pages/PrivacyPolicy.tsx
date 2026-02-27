import React from 'react';
import { useSEO } from '../hooks/useSEO';

const PrivacyPolicy: React.FC = () => {
    useSEO({
        title: "Privacy Policy - InfinityGrab",
        description: "Read the Privacy Policy of InfinityGrab. Learn how we handle your data, protect your privacy, and ensure a secure video download experience.",
        canonical: "https://infinitygrab.xyz/privacy"
    });

    return (
        <section className="policy-section" id="privacy">
            <div className="container">
                <div className="policy-card">
                    <h1 className="policy-title">Privacy Policy</h1>
                    <p className="policy-date">Last Updated: February 20, 2026</p>

                    <div className="policy-body">
                        <h2>1. Introduction</h2>
                        <p>Welcome to <strong>InfinityGrab</strong> ("we", "our", or "us"). We are committed to protecting your personal information and your right to privacy. This Privacy Policy explains how we collect, use, and share information about you when you use our website at <a href="https://infinitygrab.xyz">infinitygrab.xyz</a>.</p>

                        <h2>2. Information We Collect</h2>
                        <p>We collect minimal information to provide you with the best experience:</p>
                        <ul>
                            <li><strong>Usage Data:</strong> We collect anonymous usage statistics such as pages visited, time spent, and browser type via Google Analytics.</li>
                            <li><strong>Log Data:</strong> Our servers may log your IP address, browser type, and referring URLs for security and performance monitoring.</li>
                            <li><strong>Cookies:</strong> We use cookies and similar tracking technologies to improve your experience and serve relevant advertisements.</li>
                        </ul>

                        <h2>3. How We Use Your Information</h2>
                        <ul>
                            <li>To operate and improve our services</li>
                            <li>To display relevant advertisements via Google AdSense</li>
                            <li>To analyze usage patterns and optimize performance</li>
                            <li>To ensure the security of our platform</li>
                        </ul>

                        <h2>4. Google AdSense & Third-Party Advertising</h2>
                        <p>We use <strong>Google AdSense</strong> to display advertisements on our website. Google uses cookies to serve ads based on your prior visits to our site and other sites on the Internet. You can opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer">Google Ads Settings</a>.</p>
                        <p>Google's use of advertising cookies enables it and its partners to serve ads based on your visit to our site and/or other sites on the Internet. More information on Google's privacy policy can be found at <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">policies.google.com/privacy</a>.</p>

                        <h2>5. Cookies Policy</h2>
                        <p>Our website uses cookies to enhance your experience. Types of cookies we use:</p>
                        <ul>
                            <li><strong>Essential Cookies:</strong> Required for the website to function properly</li>
                            <li><strong>Analytics Cookies:</strong> Help us understand how visitors interact with our site</li>
                            <li><strong>Advertising Cookies:</strong> Used by Google AdSense to serve personalized ads</li>
                        </ul>
                        <p>You can control cookies through your browser settings. Disabling cookies may affect some functionality of our website.</p>

                        <h2>6. Data Retention</h2>
                        <p>We do not store any videos you download through our service. Video files are processed in real-time and streamed directly to your device. We do not retain any video content on our servers.</p>

                        <h2>7. Third-Party Links</h2>
                        <p>Our website may contain links to third-party websites. We are not responsible for the privacy practices of these sites. We encourage you to review their privacy policies.</p>

                        <h2>8. Children's Privacy</h2>
                        <p>Our service is not directed to children under 13 years of age. We do not knowingly collect personal information from children under 13.</p>

                        <h2>9. Your Rights</h2>
                        <p>You have the right to access, update, or delete your personal information. To exercise these rights, please contact us at <a href="mailto:privacy@infinitygrab.xyz">privacy@infinitygrab.xyz</a>.</p>

                        <h2>10. Changes to This Policy</h2>
                        <p>We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page with an updated date.</p>

                        <h2>11. Contact Us</h2>
                        <p>If you have any questions about this Privacy Policy, please contact us at: <a href="mailto:privacy@infinitygrab.xyz">privacy@infinitygrab.xyz</a></p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default PrivacyPolicy;
