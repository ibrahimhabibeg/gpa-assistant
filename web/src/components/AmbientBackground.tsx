import React from 'react';
import { LiquidEther } from './LiquidEther';

export const AmbientBackground: React.FC = () => {
  return (
    <div className="bg-ambient overflow-hidden">
      {/* Dynamic Fluid Simulation Layer */}
      <div className="absolute inset-0 z-0 opacity-40">
        <LiquidEther
          colors={[ '#5E6AD2', '#818CF8', '#2D336B' ]} // Custom palette matching our design
          mouseForce={15}
          cursorSize={80}
          resolution={0.4}
          autoDemo={true}
          autoSpeed={0.3}
          autoIntensity={1.5}
          autoResumeDelay={2000}
        />
      </div>

      {/* Overlays */}
      <div className="bg-ambient-noise" />
      <div className="bg-ambient-grid bg-grid-pattern" />
      
      {/* Subtle depth blobs (reduced opacity since we have liquid ether) */}
      <div className="blob blob-primary opacity-20" />
      <div className="blob blob-secondary opacity-10" />
      <div className="blob blob-tertiary opacity-10" />
    </div>
  );
};
