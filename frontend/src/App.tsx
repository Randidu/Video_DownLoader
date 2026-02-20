import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Preview from './components/Preview';
import Features from './components/Features';
import Footer from './components/Footer';
import type { VideoInfo } from './Types';
import './index.css';

// Determine API URL
const API_URL = import.meta.env.PROD
  ? window.location.origin
  : 'http://localhost:8000';

function App() {
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) {
        const text = await response.text();
        // Try parsing JSON error
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
        // Scroll to preview
        setTimeout(() => {
          const preview = document.getElementById('previewSection');
          if (preview) preview.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      } else {
        throw new Error('Invalid response from server');
      }

    } catch (err: any) {
      console.error(err);
      setError(err.message || 'An error occurred while fetching video info');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = (url: string, format: string, quality?: string) => {
    setIsDownloading(true);

    // Construct Query URL
    const params = new URLSearchParams({
      url: url,
      format: format
    });

    let actualQuality = quality;
    if (actualQuality === 'audio') actualQuality = '';

    if (actualQuality) {
      params.append('quality', actualQuality);
    }

    const downloadUrl = `${API_URL}/video/download_link?${params.toString()}`;

    // Trigger Download
    window.location.href = downloadUrl;

    // Reset UI after a delay
    setTimeout(() => {
      setIsDownloading(false);
    }, 5000);
  };

  return (
    <div className="app-container">
      <Navbar />
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
      <Footer />
    </div>
  );
}

export default App;
