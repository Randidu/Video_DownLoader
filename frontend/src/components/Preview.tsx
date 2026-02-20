import React, { useState, useEffect } from 'react';
import type { VideoInfo } from '../Types';

interface PreviewProps {
    videoInfo: VideoInfo;
    url: string;
    onDownload: (url: string, format: string, quality?: string) => void;
    isDownloading: boolean;
}

const Preview: React.FC<PreviewProps> = ({ videoInfo, url, onDownload, isDownloading }) => {
    const [quality, setQuality] = useState('720p');
    const [format, setFormat] = useState('mp4');

    useEffect(() => {
        if (format === 'mp3') {
            setQuality('audio');
        } else if (quality === 'audio') {
            setQuality('720p');
        }
    }, [format]);

    useEffect(() => {
        if (quality === 'audio') {
            setFormat('mp3');
        } else if (format === 'mp3') {
            setFormat('mp4');
        }
    }, [quality]);


    const formatDuration = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const getPlatform = (url: string) => {
        if (url.includes('youtube') || url.includes('youtu.be')) return 'YouTube';
        if (url.includes('facebook')) return 'Facebook';
        if (url.includes('instagram')) return 'Instagram';
        if (url.includes('tiktok')) return 'TikTok';
        if (url.includes('twitter') || url.includes('x.com')) return 'X (Twitter)';
        if (url.includes('vimeo')) return 'Vimeo';
        return 'Unknown';
    };

    const platform = getPlatform(url);

    return (
        <section className="preview-section active" id="previewSection">
            <div className="container">
                <div className="preview-card">
                    <div className="row">
                        <div className="col-lg-5">
                            <img
                                src={videoInfo.thumbnail}
                                alt={videoInfo.title}
                                className="video-thumbnail"
                            />
                        </div>
                        <div className="col-lg-7">
                            <div className="video-info">
                                <h4>{videoInfo.title}</h4>
                                <div className="mb-3">
                                    <span className="platform-badge">
                                        <i className="bi bi-play-circle me-1"></i>{platform}
                                    </span>
                                    {videoInfo.duration > 0 && (
                                        <span className="duration-badge">
                                            <i className="bi bi-clock me-1"></i>{formatDuration(videoInfo.duration)}
                                        </span>
                                    )}
                                </div>

                                <div className="download-options">
                                    <div className="row g-3">
                                        <div className="col-md-6">
                                            <label className="form-label">Quality</label>
                                            <select
                                                className="form-select"
                                                value={quality}
                                                onChange={(e) => setQuality(e.target.value)}
                                            >
                                                <option value="1080p">1080p (Full HD)</option>
                                                <option value="720p">720p (HD)</option>
                                                <option value="480p">480p (SD)</option>
                                                <option value="360p">360p</option>
                                                <option value="audio">Audio Only (MP3)</option>
                                            </select>
                                        </div>
                                        <div className="col-md-6">
                                            <label className="form-label">Format</label>
                                            <select
                                                className="form-select"
                                                value={format}
                                                onChange={(e) => setFormat(e.target.value)}
                                            >
                                                <option value="mp4">MP4 (Video)</option>
                                                <option value="mp3">MP3 (Audio)</option>
                                            </select>
                                        </div>
                                    </div>

                                    <button
                                        className="btn btn-success btn-download"
                                        onClick={() => onDownload(url, format, quality)}
                                        disabled={isDownloading}
                                    >
                                        {isDownloading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                                Processing Download...
                                            </>
                                        ) : (
                                            <>
                                                <i className="bi bi-download me-2"></i>Download Video
                                            </>
                                        )}
                                    </button>

                                    {/* Progress Bar placeholder - not implemented in original logic fully besides visual toggle */}
                                    {isDownloading && (
                                        <div className="progress-container active">
                                            <div className="d-flex justify-content-between mb-2">
                                                <span className="text-secondary">Processing...</span>
                                                <span className="text-secondary">Please wait</span>
                                            </div>
                                            <div className="progress">
                                                <div
                                                    className="progress-bar progress-bar-striped progress-bar-animated"
                                                    role="progressbar"
                                                    style={{ width: '100%' }}
                                                ></div>
                                            </div>
                                            <div className="mt-2 text-warning small">
                                                <i className="bi bi-info-circle me-1"></i>
                                                Large videos may take a few minutes. Do not close this tab.
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Preview;
