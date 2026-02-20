import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Preview from './components/Preview';
import Features from './components/Features';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';
import AboutUs from './pages/AboutUs';
import Contact from './pages/Contact';
import type { VideoInfo } from './Types';
import './index.css';

const rawUrl = import.meta.env.VITE_API_URL || 'https://web-production-7877c.up.railway.app';
const API_URL = rawUrl.replace(/\/$/, '');

function HomePage() {
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);
  const [searchedUrl, setSearchedUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleFetch = async (url: string) => {
    setIsLoading(true);
    setError(null);
    setVideoInfo(null);
    setSearchedUrl(url);

    try {
      const response = await fetch(`${API_URL}/video/info`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const text = await response.text();
        try {
          const jsonError = JSON.parse(text);
          throw new Error(jsonError.detail || 'Failed to fetch video info');
        } catch {
          throw new Error(text || 'Failed to fetch video info');
        }
      }

      const data = await response.json();
      if (data.success && data.data) {
        setVideoInfo(data.data);
        setTimeout(() => {
          const preview = document.getElementById('previewSection');
          if (preview) preview.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching video info');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = (url: string, format: string, quality?: string) => {
    setIsDownloading(true);
    const params = new URLSearchParams({ url, format });
    let actualQuality = quality;
    if (actualQuality === 'audio') actualQuality = '';
    if (actualQuality) params.append('quality', actualQuality);
    window.location.href = `${API_URL}/video/download_link?${params.toString()}`;
    setTimeout(() => setIsDownloading(false), 5000);
  };

  return (
    <div className="app-container">
      <Hero onFetch={handleFetch} isLoading={isLoading} error={error} />
      {videoInfo && (
        <Preview
          videoInfo={videoInfo}
          url={searchedUrl}
          onDownload={handleDownload}
          isDownloading={isDownloading}
        />
      )}
      <Features />
      <FAQ />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
