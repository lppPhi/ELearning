import React from 'react';
import styled from 'styled-components';

const VideoWrapper = styled.div`
    position: relative;
    padding-bottom: 56.25%; /* Tỉ lệ 16:9 */
    height: 0;
    overflow: hidden;
    margin-bottom: 20px;

    iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
        border-radius: 8px; /* Bo góc video */
    }
`;

const VideoPlayer = ({ youtubeUrl }) => {
    // Hàm để trích xuất ID video từ URL YouTube
    const getYouTubeId = (url) => {
        const regExp = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([A-Za-z0-9_-]{11})(?:[&?][^\s]*)?/;
        const match = url.match(regExp);
        return (match && match[1] && match[1].length === 11) ? match[1] : null;
    };

    const videoId = getYouTubeId(youtubeUrl);
    const embedUrl = videoId ? `https://www.youtube.com/embed/${videoId}?rel=0` : '';

    if (!videoId) {
        return <p>URL YouTube không hợp lệ hoặc không có video.</p>;
    }

    return (
        <VideoWrapper>
            <iframe
                src={embedUrl}
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
            ></iframe>
        </VideoWrapper>
    );
};

export default VideoPlayer;