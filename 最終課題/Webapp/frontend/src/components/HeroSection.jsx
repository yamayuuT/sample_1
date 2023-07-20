import React from 'react';
import './HeroSection.css';

const HeroSection = () => {
    return (

        <div className="hero">
            <video className="background-video" autoPlay loop muted>
                <source src='/video/video.mp4' type='video/mp4' />
                
            </video>
            <div className="hero-content">
                <h1>Welcome to My App</h1>
                <p>This is a simple app made with React.</p>
            </div>
        </div>

    );
};

export default HeroSection;
