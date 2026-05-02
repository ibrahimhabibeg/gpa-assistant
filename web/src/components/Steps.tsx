import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, MousePointer2, Save, Upload, FileText } from 'lucide-react';

export const Steps: React.FC = () => {
  const steps = [
    {
      number: "01",
      title: "Getting the HTML File",
      description: "To get the HTML file of your transcript from Ibn Al-Haitham, follow these steps:",
      items: [
        { icon: <ExternalLink className="w-4 h-4" />, text: "Navigate to https://myu.suez.edu.eg/ and log in." },
        { icon: <MousePointer2 className="w-4 h-4" />, text: "Go to the \"Course Grades\" page." },
        { icon: <Save className="w-4 h-4" />, text: "Click CTRL+S (or CMD+S) to save the page." },
        { icon: <FileText className="w-4 h-4" />, text: "Choose \"Web Page, Complete\" as the format." },
        { icon: <Upload className="w-4 h-4" />, text: "Upload the 'MyU.html' file using the section below." }
      ]
    }
  ];

  return (
    <div className="w-full mb-12">
      {steps.map((step, idx) => (
        <motion.div
          key={idx}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="glass-card rounded-2xl p-8 mb-12"
        >
          <div className="flex items-center gap-4 mb-6">
            <span className="text-4xl font-bold text-accent/20 font-mono leading-none">{step.number}</span>
            <div>
              <h2 className="text-2xl font-semibold text-gradient">{step.title}</h2>
              <p className="text-foreground-muted text-sm mt-1">{step.description}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {step.items.map((item, i) => (
              <div key={i} className="flex items-start gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-white/10 transition-colors group">
                <div className="flex flex-col items-center gap-2">
                  <span className="text-[10px] font-mono font-bold text-accent/40 group-hover:text-accent">0{i + 1}</span>
                  <div className="p-1.5 rounded-md bg-accent/10 text-accent group-hover:bg-accent group-hover:text-white transition-all">
                    {item.icon}
                  </div>
                </div>
                <p className="text-sm text-foreground-muted group-hover:text-foreground transition-colors leading-relaxed pt-1">
                  {item.text}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      ))}

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="mb-8 px-8"
      >
        <div className="flex items-center gap-4 mb-2">
          <span className="text-4xl font-bold text-accent/20 font-mono leading-none">02</span>
          <div>
            <h2 className="text-2xl font-semibold text-gradient">Upload Transcript</h2>
            <p className="text-foreground-muted text-sm mt-1">
              Upload your Ibn Al-Haitham HTML export, then provide program requirements before parsing.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
