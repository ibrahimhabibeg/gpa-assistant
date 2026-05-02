import React from 'react';
import { motion } from 'framer-motion';

export const Hero: React.FC = () => {
  return (
    <section className="relative pt-32 pb-20 px-6 overflow-hidden">
      <div className="container mx-auto text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tight text-gradient mb-6">
            Master Your Academic <br />
            <span className="text-accent-gradient">Future with Precision.</span>
          </h1>
          <p className="text-lg md:text-xl text-foreground-muted max-w-2xl mx-auto mb-10 leading-relaxed">
            The intelligent GPA assistant for Ibn Al-Haitham transcripts. 
            Analyze your performance, predict outcomes, and reach your goals with cinematic clarity.
          </p>
        </motion.div>
      </div>
    </section>
  );
};
