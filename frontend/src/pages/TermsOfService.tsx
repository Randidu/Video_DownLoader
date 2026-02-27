import React from 'react';
import { useSEO } from '../hooks/useSEO';

const TermsOfService: React.FC = () => {
    useSEO({
        title: "Terms of Service - InfinityGrab",
        description: "Read the Terms of Service for using InfinityGrab video downloader. Information about acceptable use, copyright rules, and liabilities.",
        canonical: "https://infinitygrab.xyz/terms"
    });

    return (
        <section className="policy-section" id="terms">
            <div className="container">
                <div className="policy-card">
                    <h1 className="policy-title">Terms of Service</h1>
                    <p className="policy-date">Last Updated: February 20, 2026</p>

                    <div className="policy-body">
                        <h2>1. Acceptance of Terms</h2>
                        <p>By accessing and using <strong>InfinityGrab</strong> ("Service") at <a href="https://infinitygrab.xyz">infinitygrab.xyz</a>, you accept and agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our service.</p>

                        <h2>2. Description of Service</h2>
                        <p>InfinityGrab is a free online tool that allows users to download publicly available videos from various platforms including YouTube, Facebook, Instagram, TikTok, and others for personal, non-commercial use.</p>

                        <h2>3. Copyright & Intellectual Property Disclaimer</h2>
                        <div className="disclaimer-box">
                            <p>⚠️ <strong>IMPORTANT DISCLAIMER:</strong> InfinityGrab is intended for downloading videos for <strong>personal use only</strong>. You are solely responsible for ensuring that your use of downloaded content complies with applicable copyright laws.</p>
                            <ul>
                                <li>Do NOT download copyrighted content without permission from the copyright holder</li>
                                <li>Do NOT redistribute, sell, or publicly perform downloaded content</li>
                                <li>Only download content you have the right to download (e.g., your own videos, Creative Commons licensed content, or content explicitly allowed for download)</li>
                            </ul>
                        </div>

                        <h2>4. Permitted Use</h2>
                        <p>You may use InfinityGrab to:</p>
                        <ul>
                            <li>Download your own videos for backup purposes</li>
                            <li>Download videos licensed under Creative Commons</li>
                            <li>Download content where you have explicit permission from the copyright holder</li>
                            <li>Download content for personal, offline viewing where permitted by the platform</li>
                        </ul>

                        <h2>5. Prohibited Use</h2>
                        <p>You may NOT use InfinityGrab to:</p>
                        <ul>
                            <li>Download content in violation of any platform's Terms of Service</li>
                            <li>Download, distribute, or use copyrighted material without authorization</li>
                            <li>Use the service for commercial purposes without express written consent</li>
                            <li>Engage in any activity that is illegal or harmful</li>
                        </ul>

                        <h2>6. Limitation of Liability</h2>
                        <p>InfinityGrab is provided "as is" without any warranties. We shall not be liable for:</p>
                        <ul>
                            <li>Any misuse of downloaded content by users</li>
                            <li>Service interruptions or technical issues</li>
                            <li>Any direct, indirect, or consequential damages arising from use of our service</li>
                        </ul>

                        <h2>7. Third-Party Services</h2>
                        <p>Our service uses third-party tools to facilitate downloads. We are not responsible for the availability or reliability of these third-party services.</p>

                        <h2>8. Advertising</h2>
                        <p>InfinityGrab displays advertisements served by Google AdSense. You agree to our use of Google AdSense as part of using our free service. These ads help us maintain and improve the service.</p>

                        <h2>9. Changes to Terms</h2>
                        <p>We reserve the right to modify these Terms of Service at any time. Changes will be effective immediately upon posting. Continued use of the service after changes constitutes acceptance of the new terms.</p>

                        <h2>10. Termination</h2>
                        <p>We reserve the right to terminate or restrict access to our service for any user who violates these Terms of Service.</p>

                        <h2>11. Governing Law</h2>
                        <p>These Terms shall be governed by and construed in accordance with applicable laws.</p>

                        <h2>12. Contact</h2>
                        <p>For questions about these Terms, contact us: <a href="mailto:legal@infinitygrab.xyz">legal@infinitygrab.xyz</a></p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default TermsOfService;
