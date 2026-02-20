export interface VideoInfo {
    title: string;
    thumbnail: string;
    duration: number;
    uploader?: string;
    view_count?: number;
}

export interface DownloadResponse {
    download_id: string;
    filename: string;
    filepath: string;
    filesize: number;
    is_saved_locally: boolean;
    local_path: string;
    warning?: string;
}
